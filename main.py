import schedule
import time
from tools.gmail_tools import list_recent_emails, get_gmail_service
from tools.calendar_tools import ensure_valid_creds
from agents import email_assistant_with_scheduling
from tools.logger import logger

get_gmail_service()
ensure_valid_creds()


def check_recent_emails():
    """
    Check for new emails in the last 10 minutes and process them.
    This function will be called every 10 minutes.
    """
    try:
        # Get emails from last 10 minutes
        recent_emails = list_recent_emails(minutes=10)

        if not recent_emails:
            logger.info("no_new_emails", minutes=10)
            return

        logger.info("found_new_emails", count=len(recent_emails))

        # Process each email
        for email in recent_emails:
            logger.info(
                "processing_email",
                sender=email.get("sender"),
                subject=email.get("subject"),
            )
            for update in email_assistant_with_scheduling.stream(
                {"messages": [{"role": "user", "content": f"Email Content: {email}"}]},
                stream_mode="updates",
            ):
                # update will be a dict with node name as key and its output as value
                for node_name, node_output in update.items():
                    logger.info(
                        "ai_step",
                        node=node_name,
                        output=node_output["messages"][-1].content,
                    )

    except Exception as e:
        logger.exception("email_check_error", error=str(e))


def main():
    # Schedule the email checking function to run every 10 minutes
    schedule.every(10).minutes.do(check_recent_emails)

    logger.info("assistant_started", check_interval_minutes=10)

    # Run the first check immediately
    check_recent_emails()

    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
