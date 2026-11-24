from src.data_loader import load_contacts, load_reminders
from src.mailer import (
    personalize_reminder,
    send_email_simulation
)
from src.automation import get_due_reminders
from src.reporting import (
    log_email_activity,
    generate_report,
    was_reminder_processed
)

def main():
    print("\nEMAIL AUTOMATION & REMINDER SYSTEM")
    print("=" * 40)

    contacts = load_contacts()
    reminders = load_reminders()

    print(f"Contacts loaded: {len(contacts)}")
    print(f"Reminders loaded: {len(reminders)}")

    due_reminders = get_due_reminders(reminders)

    print(f"Due reminders: {len(due_reminders)}")

    for reminder in due_reminders:
        if was_reminder_processed(reminder["reminder_id"]):
            print(
                f"Skipping {reminder['reminder_id']}: "
                "Already processed."
            )
            continue
        contact = next(
            (
                c for c in contacts
                if c["contact_id"] == reminder["contact_id"]
            ),
            None
        )

        if contact is None:
            print(f"Contact missing: {reminder['contact_id']}")
            continue

        try:
            email_content = personalize_reminder(
                reminder, contacts
            )

            status = send_email_simulation(
                contact["email"],
                email_content
            )

            log_email_activity(
                reminder["reminder_id"],
                contact["email"],
                status,
                reminder["reminder_type"]
            )

        except Exception as error:
            print("Error:", error)

            log_email_activity(
                reminder["reminder_id"],
                contact["email"],
                "FAILED",
                str(error)
            )

    generate_report()


if __name__ == "__main__":
    main()