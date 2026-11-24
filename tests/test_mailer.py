
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from contextlib import redirect_stdout
from io import StringIO

from src.mailer import (
    load_template,
    generate_email,
    personalize_reminder,
    send_email_simulation,
    send_email_smtp
)


class TestEmailFunctions(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)

        self.template_dir = Path(self.temp_dir.name)

        self.patcher = patch(
            "src.mailer.TEMPLATE_DIR",
            self.template_dir
        )
        self.patcher.start()
        self.addCleanup(self.patcher.stop)

        self.template = (
            "Subject: Reminder for {name}\n"
            "Hello {name},\n"
            "Your {reminder_type} is due on {due_datetime}."
        )

        (self.template_dir / "test_template.txt").write_text(
            self.template,
            encoding="utf-8"
        )

        self.contact = {
            "contact_id": "C001",
            "name": "Aarav Sharma",
            "email": "aarav@example.com",
            "department": "HR"
        }

        self.reminder = {
            "reminder_id": "R001",
            "contact_id": "C001",
            "reminder_type": "Document Submission",
            "due_datetime": "2026-11-20 09:00",
            "template_file": "test_template.txt",
            "status": "pending"
        }

    def test_load_template(self):
        result = load_template("test_template.txt")

        self.assertIn("Hello {name}", result)

    def test_missing_template(self):
        with self.assertRaises(FileNotFoundError):
            load_template("missing_template.txt")

    def test_generate_email(self):
        result = generate_email(
            "test_template.txt",
            {
                "name": "Aarav",
                "reminder_type": "Document Submission",
                "due_datetime": "2026-11-20 09:00"
            }
        )

        self.assertIn("Hello Aarav", result)
        self.assertIn("Document Submission", result)

    def test_missing_template_value(self):
        with self.assertRaises(ValueError):
            generate_email(
                "test_template.txt",
                {"name": "Aarav"}
            )

    def test_personalize_reminder(self):
        result = personalize_reminder(
            self.reminder,
            [self.contact]
        )

        self.assertIn("Aarav Sharma", result)
        self.assertIn("Document Submission", result)

    def test_contact_not_found(self):
        with self.assertRaises(ValueError):
            personalize_reminder(
                self.reminder,
                []
            )

    def test_email_simulation(self):
        output = StringIO()

        with redirect_stdout(output):
            status = send_email_simulation(
                "aarav@example.com",
                "Test reminder message"
            )

        self.assertEqual(status, "SIMULATED")
        self.assertIn("SIMULATED", output.getvalue())
        self.assertIn("No email was sent", output.getvalue())

    def test_smtp_disabled(self):
        with self.assertRaises(RuntimeError):
            send_email_smtp(
                "aarav@example.com",
                "Test reminder message"
            )


if __name__ == "__main__":
    unittest.main()
