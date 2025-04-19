"""Tools for interacting with Gmail API."""

from typing import List, Dict, Any, Annotated
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import os
import base64
from email.mime.text import MIMEText
import pickle
from langchain_core.tools import tool

# If modifying these scopes, delete the token.pickle file.
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.compose",
    "https://www.googleapis.com/auth/gmail.modify",
]


def get_gmail_service() -> Any:
    """
    Gets Gmail API service instance with proper authentication.

    Returns:
        Resource: Gmail API service instance that can be used to make API calls.

    Raises:
        OSError: If credentials.json file is not found
        google.auth.exceptions.RefreshError: If token refresh fails
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens
    if os.path.exists("gmail_token.pickle"):
        with open("gmail_token.pickle", "rb") as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("gmail_token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return build("gmail", "v1", credentials=creds)


def list_recent_emails(
    minutes: Annotated[int, "Number of minutes to look back for fetching emails"] = 10,
) -> List[Dict[str, str]]:
    """
    Lists emails from the last specified minutes from the user's Gmail inbox.

    Args:
        minutes: Number of minutes to look back for emails. Defaults to 10.

    Returns:
        List[Dict[str, str]]: List of email details with the following structure:
            {
                'id': str,           # Gmail message ID
                'subject': str,      # Email subject
                'sender': str,       # Sender's email address
                'date': str,         # Email timestamp
                'body': str          # Full email body in plain text
            }

    Raises:
        googleapiclient.errors.HttpError: If the API request fails
    """
    service = get_gmail_service()

    # Calculate the timestamp for N minutes ago
    now = datetime.now()
    time_n_minutes_ago = now - timedelta(minutes=minutes)
    query = f"after:{int(time_n_minutes_ago.timestamp())}"

    results = (
        service.users()
        .messages()
        .list(userId="me", labelIds=["INBOX"], q=query)
        .execute()
    )

    messages = results.get("messages", [])
    emails = []

    for message in messages:
        msg = (
            service.users()
            .messages()
            .get(userId="me", id=message["id"], format="full")
            .execute()
        )

        headers = msg["payload"]["headers"]
        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "")
        sender = next((h["value"] for h in headers if h["name"] == "From"), "")
        date = next((h["value"] for h in headers if h["name"] == "Date"), "")

        # Get email body
        body = ""
        if "parts" in msg["payload"]:
            parts = msg["payload"]["parts"]
            for part in parts:
                if part["mimeType"] == "text/plain":
                    if "data" in part["body"]:
                        body = base64.urlsafe_b64decode(part["body"]["data"]).decode(
                            "utf-8"
                        )
                    break
        elif "body" in msg["payload"] and "data" in msg["payload"]["body"]:
            body = base64.urlsafe_b64decode(msg["payload"]["body"]["data"]).decode(
                "utf-8"
            )

        emails.append(
            {
                "id": msg["id"],
                "subject": subject,
                "sender": sender,
                "date": date,
                "body": body,
            }
        )

    return emails


@tool
def create_draft(
    body: Annotated[str, "Content of the email to be sent"],
    sender: Annotated[
        str, "Original sender's email address that will be used as reply-to"
    ],
    subject: Annotated[str, "Email subject, will be prefixed with Re: for replies"],
    thread_id: Annotated[str, "Gmail thread ID for maintaining conversation threads"],
    original_message_id: Annotated[
        str, "Original message ID for setting reply headers"
    ],
) -> str:
    """
    Creates a draft email in Gmail, optionally as a reply to an existing message.

    Args:
        body: str - Email body content
        sender: str - Original sender's email address (will be used as 'to' for reply)
        subject: str - Email subject (will be prefixed with 'Re: ' for replies)
        thread_id: str - Gmail thread ID for maintaining conversation threads
        original_message_id: str - Original message ID for reply headers

    Returns:
        str: A confirmation message indicating that the draft has been created

    Raises:
        ValueError: If trying to create a reply without original message details
        googleapiclient.errors.HttpError: If the API request fails
    """
    service = get_gmail_service()

    message = MIMEText(body)

    # Extract original message details
    to = sender.split("<")
    if len(to) > 1:
        to = to[1].rstrip(">")
    else:
        to = sender

    if not subject.startswith("Re: "):
        subject = f"Re: {subject}"

    # Get thread ID and message ID for proper threading
    references = original_message_id

    # Set headers for reply
    message["to"] = to
    message["subject"] = subject
    if references:
        message["In-Reply-To"] = f"<{references}@mail.gmail.com>"
        message["References"] = f"<{references}@mail.gmail.com>"

    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    draft_body = {"message": {"raw": encoded_message, "threadId": thread_id}}

    service.users().drafts().create(userId="me", body=draft_body).execute()

    return "Email draft created successfully"
