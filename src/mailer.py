from pathlib import Path


TEMPLATE_DIR = Path("templates")


def load_template(template_file):
    """Read an email template."""

    template_path = TEMPLATE_DIR / template_file

    if not template_path.exists():
        raise FileNotFoundError(
            f"Template not found: {template_file}"
        )

    return template_path.read_text(encoding="utf-8")


def generate_email(template_file, data):
    """Replace template placeholders with actual values."""

    template = load_template(template_file)

    try:
        return template.format(**data)
    except KeyError as error:
        raise ValueError(
            f"Missing template value: {error}"
        )
def personalize_reminder(reminder, contacts):
    """Generate a personalized email for a reminder."""

    contact = next(
        (
            person for person in contacts
            if person["contact_id"] == reminder["contact_id"]
        ),
        None
    )

    if contact is None:
        raise ValueError(
            f"Contact not found: {reminder['contact_id']}"
        )

    email_data = {
        "name": contact["name"],
        "email": contact["email"],
        "department": contact["department"],
        "reminder_type": reminder["reminder_type"],
        "due_datetime": reminder["due_datetime"]
    }

    return generate_email(
        reminder["template_file"],
        email_data
    )
def send_email_simulation(to_email, email_content):
    """Simulate sending an email without actually sending it."""

    print("\n" + "=" * 50)
    print("EMAIL SENDING SIMULATION")
    print("=" * 50)

    print(f"Recipient: {to_email}")
    print("\nEmail Content:")
    print("-" * 50)
    print(email_content)
    print("-" * 50)

    print("Status: SIMULATED - No email was sent.")
    print("=" * 50)

    return "SIMULATED"
import smtplib
import ssl
from email.message import EmailMessage

from src.config import (
    SMTP_SERVER,
    SMTP_PORT,
    SENDER_EMAIL,
    SENDER_PASSWORD,
    EMAIL_ENABLED
)


def send_email_smtp(to_email, email_content):
    """Send an email through SMTP when explicitly enabled."""

    if not EMAIL_ENABLED:
        raise RuntimeError("SMTP sending is disabled.")

    if not SENDER_EMAIL or not SENDER_PASSWORD:
        raise ValueError("SMTP credentials are not configured.")

    message = EmailMessage()

    lines = email_content.splitlines()
    subject = "Reminder Notification"

    if lines and lines[0].startswith("Subject:"):
        subject = lines[0].replace("Subject:", "", 1).strip()
        email_content = "\n".join(lines[1:]).strip()

    message["Subject"] = subject
    message["From"] = SENDER_EMAIL
    message["To"] = to_email
    message.set_content(email_content)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(
        SMTP_SERVER, SMTP_PORT, context=context
    ) as server:
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(message)

    return "SENT"