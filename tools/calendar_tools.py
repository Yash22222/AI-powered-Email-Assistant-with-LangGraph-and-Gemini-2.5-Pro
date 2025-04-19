"""Google Calendar API tools for managing calendar events."""

import os
import datetime
from typing import Dict, List, Union, Annotated
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pickle
from langchain_core.tools import tool
from tools.logger import logger

SCOPES = ["https://www.googleapis.com/auth/calendar"]
token_path = "calendar_token.pickle"
credentials_path = "credentials.json"
creds = None
service = None

def ensure_valid_creds() -> None:
    global creds, service
    if os.path.exists(token_path):
        with open(token_path, "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(credentials_path):
                raise FileNotFoundError(
                    f"Google credentials file not found at {credentials_path}. "
                    "Please download it from Google Cloud Console."
                )
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for future use
        with open(token_path, "wb") as token:
            pickle.dump(creds, token)

    service = build("calendar", "v3", credentials=creds)


@tool
def create_calendar_event(
    summary: Annotated[str, "Title of the event"],
    start_time: Annotated[
        Union[str, datetime.datetime], "Start time (ISO format or datetime)"
    ],
    end_time: Annotated[
        Union[str, datetime.datetime], "End time (ISO format or datetime)"
    ],
    description: Annotated[str, "Description of the event"] = None,
    location: Annotated[str, "Location of the event"] = None,
    attendees: Annotated[List[str], "List of attendee email addresses"] = None,
    recurrence: Annotated[List[str], "List of recurrence rules (RRULE)"] = None,
    timezone: Annotated[str, "Timezone for the event"] = "Asia/Kolkata",
) -> str:
    """
    Create a new calendar event.

    Args:
        summary: Title of the event
        start_time: Start time (ISO format or datetime)
        end_time: End time (ISO format or datetime)
        description: Description of the event (optional)
        location: Location of the event (optional)
        attendees: List of attendee email addresses (optional)
        recurrence: List of recurrence rules (optional)
        timezone: Timezone for the event (default: Asia/Kolkata)

    Returns:
        str: "Calendar event created successfully" or error message
    """
    ensure_valid_creds()
    # Convert datetime objects to ISO format if needed
    if isinstance(start_time, datetime.datetime):
        start_time = start_time.isoformat()
    if isinstance(end_time, datetime.datetime):
        end_time = end_time.isoformat()

    event = {
        "summary": summary,
        "start": {
            "dateTime": start_time,
            "timeZone": timezone,
        },
        "end": {
            "dateTime": end_time,
            "timeZone": timezone,
        },
    }

    if description:
        event["description"] = description
    if location:
        event["location"] = location
    if attendees:
        event["attendees"] = [{"email": email} for email in attendees]
    if recurrence:
        event["recurrence"] = recurrence

    try:
        event = service.events().insert(calendarId="primary", body=event).execute()
        logger.info("calendar_event_created", event_id=event['id'])
        return "Calendar event created successfully"
    except HttpError as error:
        logger.error("calendar_event_creation_error", error=str(error))
        return f"Error creating calendar event: {str(error)}"


@tool
def get_calendar_events(
    start_time: Annotated[
        str, "Start time for fetching events in UTC format. For eg. 2025-03-05T00:00:00.0000+00:00"
    ],
    end_time: Annotated[
        str, "End time for fetching events in UTC format. For eg. 2025-03-05T23:59:59.0000+00:00"
    ],
    max_results: Annotated[int, "Maximum number of events to return"] = 50,
    timezone: Annotated[str, "Timezone for the events"] = "Asia/Kolkata",
) ->  List[Dict] | str:
    """
    Get a list of calendar events.

    Args:
        max_results: Maximum number of events to return (default: 10)
        time_min: Start time for fetching events (optional)
        time_max: End time for fetching events (optional)
        query: Free text search terms (optional)
        timezone: Timezone for the events (default: Asia/Kolkata)

    Returns:
        List of events or error message
    """
    ensure_valid_creds()
    # If no time_min specified, use current time
    if not start_time:
        start_time = datetime.datetime.now(datetime.timezone.utc).isoformat()
    elif isinstance(start_time, datetime.datetime):
        start_time = start_time.isoformat()

    # Convert time_max to ISO format if it's a datetime
    if end_time and isinstance(end_time, datetime.datetime):
        end_time = end_time.isoformat()

    try:
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=start_time,
                timeMax=end_time,
                maxResults=max_results,
                singleEvents=True,
                orderBy="startTime",
                timeZone=timezone,
            )
            .execute()
        )
        results = events_result.get("items", "No events found")
        return results
    except HttpError as error:
        logger.error("calendar_events_fetch_error", error=str(error))
        return "Error fetching calendar events"


@tool
def update_calendar_event(
    event_id: Annotated[str, "ID of the event to update"],
    summary: Annotated[str, "New title of the event"] = None,
    start_time: Annotated[Union[str, datetime.datetime], "New start time"] = None,
    end_time: Annotated[Union[str, datetime.datetime], "New end time"] = None,
    description: Annotated[str, "New description"] = None,
    location: Annotated[str, "New location"] = None,
    attendees: Annotated[List[str], "New list of attendee email addresses"] = None,
    timezone: Annotated[str, "Timezone for the event"] = "Asia/Kolkata",
) -> str:
    """
    Update an existing calendar event.

    Args:
        event_id: ID of the event to update
        summary: New title of the event (optional)
        start_time: New start time (optional)
        end_time: New end time (optional)
        description: New description (optional)
        location: New location (optional)
        attendees: New list of attendee email addresses (optional)
        timezone: Timezone for the event (default: Asia/Kolkata)

    Returns:
        str: "Calendar event updated successfully" or error message
    """
    ensure_valid_creds()
    try:
        # First get the existing event
        event = (
            service.events().get(calendarId="primary", eventId=event_id).execute()
        )

        # Update the fields that are provided
        if summary:
            event["summary"] = summary
        if description:
            event["description"] = description
        if location:
            event["location"] = location
        if attendees:
            event["attendees"] = [{"email": email} for email in attendees]
        if start_time:
            if isinstance(start_time, datetime.datetime):
                start_time = start_time.isoformat()
            event["start"] = {"dateTime": start_time, "timeZone": timezone}
        if end_time:
            if isinstance(end_time, datetime.datetime):
                end_time = end_time.isoformat()
            event["end"] = {"dateTime": end_time, "timeZone": timezone}

        service.events().update(calendarId="primary", eventId=event_id, body=event).execute()
        logger.info("calendar_event_updated", event_id=event_id)
        return "Calendar event updated successfully"
    except HttpError as error:
        logger.error("calendar_event_update_error", event_id=event_id, error=str(error))
        return f"Error updating calendar event: {str(error)}"


@tool
def delete_calendar_event(
    event_id: Annotated[str, "ID of the event to delete"]
) -> str:
    """
    Delete a calendar event.

    Args:
        event_id: ID of the event to delete

    Returns:
        str: "Calendar event deleted successfully" or error message
    """
    ensure_valid_creds()
    try:
        service.events().delete(calendarId="primary", eventId=event_id).execute()
        logger.info("calendar_event_deleted", event_id=event_id)
        return "Calendar event deleted successfully"
    except HttpError as error:
        logger.error("calendar_event_deletion_error", event_id=event_id, error=str(error))
        return f"Error deleting calendar event: {str(error)}"
