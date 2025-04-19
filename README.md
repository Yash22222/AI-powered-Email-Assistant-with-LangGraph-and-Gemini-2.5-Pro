# Email Assistant

A smart email and calendar management system powered by Gemini Pro that automatically processes incoming emails and manages calendar events.

## Features

- **Automated Email Processing**: Monitors inbox for new emails every minute
- **Smart Email Responses**: Generates contextual email responses using Gemini Pro
- **Calendar Management**: Automatically handles calendar event creation, updates, and deletions
- **Gmail Integration**: Seamlessly works with Gmail for email management
- **Google Calendar Integration**: Direct integration with Google Calendar for event management

## Project Structure

```text
├── main.py              # Main application entry point
├── agents.py            # AI agents configuration and prompts
├── models.py            # AI model configurations
├── tools/
│   ├── gmail_tools.py   # Gmail API integration tools
│   ├── calendar_tools.py # Google Calendar API tools
│   └── logger.py        # Logging utilities
```

## Imp Commands
```text
powershell -ExecutionPolicy Bypass -File .\venv\Scripts\activate 
```
```text
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```
```text
pip install -r requirements.txt 
```
```text
.\venv\Scripts\activate  
```
```text
python.exe -m pip install --upgrade pip
```
```text
pip install colorama 
```
## Prerequisites

- Python 3.x
- Google Cloud Project with Gmail and Calendar APIs enabled
- Google OAuth 2.0 credentials

## Installation

1. Clone the repository
2. Install dependencies:

   ```bash
   # setup a virtual environment
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Generate the API Key and save under `.env`
4. Set up Google OAuth 2.0 credentials and save them appropriately

## Generating & Adding the API Key in the project

1. Go to [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)

2. Click on create API Key

   <img width="1739" alt="image" src="https://github.com/user-attachments/assets/a4a194e7-65c8-4593-8a68-5e0bf8dd6b66" />

3. Select the project from the dropdown

   <img width="514" alt="Screenshot 2025-04-13 at 5 20 47 PM" src="https://github.com/user-attachments/assets/a06b9d61-0ef1-407c-b80f-f91fd52aa6f6" />

   In case you do not have any existing Google Cloud Projects that appear in the dropdown, create a new Google Cloud Project at [https://console.cloud.google.com/projectcreate](https://console.cloud.google.com/projectcreate) with the name of your choice and then resume creating a new API key under this newly created project

4. Copy the generated API Key

5. Open the project in any IDE of your choice (For eg. `VSCode`)

6. Rename the file `.env.example` to `.env`

7. Paste the API Key as

   ```bash
   GOOGLE_API_KEY=AIzaXXXXXXXXXXXXXXXXXXXXXX
   ```

8. Restart the IDE so that it recognizes the API key

## Setting up OAuth 2.0 Credentials

1. Go to [https://console.cloud.google.com/auth/overview](https://console.cloud.google.com/auth/overview). Click on `Get Started`

   <img width="1792" alt="Screenshot 2025-04-13 at 5 10 25 PM" src="https://github.com/user-attachments/assets/0e513e06-31b9-4e1c-8025-858e0b6a2dac" />

2. Under App Information, give any name to your app and select your email id from the drop down under user support email and click next

   <img width="628" alt="Screenshot 2025-04-13 at 5 11 08 PM" src="https://github.com/user-attachments/assets/36698341-178a-450e-b4cd-ace43b42aedc" />

3. Under Audience, select external and click next

   <img width="728" alt="Screenshot 2025-04-13 at 5 11 20 PM" src="https://github.com/user-attachments/assets/5f41c84e-3118-4cd4-a2e2-02a71ae9557e" />

4. Put any email id under contact information and click next

   <img width="694" alt="Screenshot 2025-04-13 at 5 11 28 PM" src="https://github.com/user-attachments/assets/d97c60e5-90b7-4e46-90a6-90fa7ade189d" />

5. Accept the terms and conditions and click continue

   <img width="561" alt="Screenshot 2025-04-13 at 5 11 43 PM" src="https://github.com/user-attachments/assets/1bb1f725-38ec-472f-9c6c-be208e8dfe7c" />

6. Now go the clients section and click on Create Client

   <img width="1106" alt="image" src="https://github.com/user-attachments/assets/8ac8b660-8008-490c-a63c-93b3f98c7732" />

7. Select application type as desktop application and give it any name. Then press Create.

   <img width="1008" alt="Screenshot 2025-04-13 at 5 12 34 PM" src="https://github.com/user-attachments/assets/3bc10864-dd19-4f66-8ddc-a19e8f2d4580" />

8. Click on Download JSON and download the credentials file

   <img width="264" alt="image" src="https://github.com/user-attachments/assets/9a7e9255-577b-4e19-9355-147d81e0face" />

9. Go to the project's root directory and paste the file. Rename it to `credentials.json`. This is an essential step for our backend code to recognize the client

10. Go to the Audience section and click on Publish App

   <img width="1323" alt="Screenshot 2025-04-13 at 5 15 15 PM" src="https://github.com/user-attachments/assets/56820724-d250-469a-8645-0a773a9c8b10" />

11. Now at the top search bar on the Google cloud dashboard, search for calendar and click on Google Calendar API

    <img width="829" alt="image" src="https://github.com/user-attachments/assets/31db53b9-b979-4311-b21a-dcae7d5d46e8" />

12. Click on Enable

    <img width="750" alt="Screenshot 2025-04-13 at 5 17 59 PM" src="https://github.com/user-attachments/assets/480493ec-491e-4327-880e-5c6fd681c666" />

13. Similarly, search for Google Gmail API and enable it

    <img width="750" alt="Screenshot 2025-04-13 at 5 17 59 PM" src="https://github.com/user-attachments/assets/2e0603f1-e41c-4ad4-a027-b2d38f4b1244" />

We are all set!

## Usage

Run the main application:

```bash
python main.py
```

In case you are running the app in a terminal session different from the one in which you activated virtual environment, run the app using:

```bash
source venv/bin/activate && clear && python main.py
```

The assistant will:

1. Check for new emails every minute
2. Process emails using AI to understand context and requirements
3. Generate appropriate responses and create drafts
4. Handle calendar events when scheduling is involved

## Dependencies

Key dependencies include:

- google-api-python-client: Google API client library
- langgraph: For creating reactive AI agents
- schedule: For periodic task scheduling

## Configuration

Ensure proper setup of:

1. Google OAuth 2.0 credentials
2. Gmail API access
3. Google Calendar API access

## Examples

Here are some examples of the Email Assistant in action:

### Inbox Email 1

![Inbox Email Example 1](examples/inbox-mail-1.jpeg)

### Calendar Event Created 1

![Calendar Event Created 1](examples/calendar-event-created-1.jpeg)

### Response Draft 1

![Response Draft Example 1](examples/response-draft-1.jpeg)

### Inbox Email 2

![Inbox Email Example 2](examples/inbox-mail-2.jpeg)

### Response Draft 2

![Response Draft Example 2](examples/response-draft-2.jpeg)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
