import csv
import re

CONTACTS_FILE = "data/contacts.csv"


def load_contacts(file_path=CONTACTS_FILE):
    """Load contacts from a CSV file and validate their details."""

    required_columns = {"contact_id", "name", "email", "department"}

    with open(file_path, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames or not required_columns.issubset(reader.fieldnames):
            raise ValueError("The contacts CSV is missing required columns.")

        contacts = []
        contact_ids = set()
        emails = set()

        for row_number, row in enumerate(reader, start=2):
            contact = {
                key: (row.get(key) or "").strip()
                for key in required_columns
            }

            if not all(contact.values()):
                raise ValueError(f"Missing information on CSV row {row_number}.")

            if contact["contact_id"] in contact_ids:
                raise ValueError(f"Duplicate contact ID on row {row_number}.")

            if contact["email"].lower() in emails:
                raise ValueError(f"Duplicate email on row {row_number}.")

            email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
            if not re.match(email_pattern, contact["email"]):
                raise ValueError(f"Invalid email on row {row_number}.")

            contact_ids.add(contact["contact_id"])
            emails.add(contact["email"].lower())
            contacts.append(contact)

    return contacts
from datetime import datetime


def load_reminders(file_path="data/reminders.csv"):
    """Load and validate reminder records."""

    required_columns = {
        "reminder_id",
        "contact_id",
        "reminder_type",
        "due_datetime",
        "template_file",
        "status"
    }

    with open(file_path, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames or not required_columns.issubset(reader.fieldnames):
            raise ValueError("Reminder CSV is missing required columns.")

        reminders = []
        reminder_ids = set()

        for row_number, row in enumerate(reader, start=2):
            reminder = {
                key: (row.get(key) or "").strip()
                for key in required_columns
            }

            if not all(reminder.values()):
                raise ValueError(f"Missing information on row {row_number}.")

            if reminder["reminder_id"] in reminder_ids:
                raise ValueError(f"Duplicate reminder ID on row {row_number}.")

            try:
                datetime.strptime(
                    reminder["due_datetime"], "%Y-%m-%d %H:%M"
                )
            except ValueError:
                raise ValueError(f"Invalid date on row {row_number}.")

            reminder_ids.add(reminder["reminder_id"])
            reminders.append(reminder)

    return reminders
