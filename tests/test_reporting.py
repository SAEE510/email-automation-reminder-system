
import csv
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from contextlib import redirect_stdout
from io import StringIO

from src.reporting import (
    log_email_activity,
    generate_report,
    was_reminder_processed,
)


class TestReporting(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_log = Path(self.temp_dir.name) / "email_log.csv"

        self.log_patcher = patch(
            "src.reporting.LOG_FILE",
            self.test_log
        )
        self.log_patcher.start()

    def tearDown(self):
        self.log_patcher.stop()
        self.temp_dir.cleanup()

    def test_log_email_activity_creates_file(self):
        log_email_activity(
            "R001",
            "student@example.com",
            "SIMULATED",
            "Test activity"
        )

        self.assertTrue(self.test_log.exists())

    def test_log_email_activity_writes_correct_data(self):
        log_email_activity(
            "R001",
            "student@example.com",
            "SIMULATED",
            "Test activity"
        )

        with self.test_log.open(
            "r", newline="", encoding="utf-8"
        ) as file:
            records = list(csv.DictReader(file))

        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["reminder_id"], "R001")
        self.assertEqual(
            records[0]["recipient"],
            "student@example.com"
        )
        self.assertEqual(records[0]["status"], "SIMULATED")
        self.assertEqual(records[0]["details"], "Test activity")

    def test_log_email_activity_appends_records(self):
        log_email_activity(
            "R001",
            "student@example.com",
            "SIMULATED"
        )

        log_email_activity(
            "R002",
            "teacher@example.com",
            "SENT"
        )

        with self.test_log.open(
            "r", newline="", encoding="utf-8"
        ) as file:
            records = list(csv.DictReader(file))

        self.assertEqual(len(records), 2)

    def test_processed_simulated_reminder(self):
        log_email_activity(
            "R001",
            "student@example.com",
            "SIMULATED"
        )

        self.assertTrue(was_reminder_processed("R001"))

    def test_processed_sent_reminder(self):
        log_email_activity(
            "R002",
            "teacher@example.com",
            "SENT"
        )

        self.assertTrue(was_reminder_processed("R002"))

    def test_unprocessed_reminder(self):
        self.assertFalse(was_reminder_processed("R999"))

    def test_failed_reminder_is_not_processed(self):
        log_email_activity(
            "R003",
            "student@example.com",
            "FAILED"
        )

        self.assertFalse(was_reminder_processed("R003"))

    def test_generate_report_without_log(self):
        output = StringIO()

        with redirect_stdout(output):
            generate_report()

        self.assertIn(
            "No email activity recorded yet.",
            output.getvalue()
        )

    def test_generate_report_with_records(self):
        log_email_activity(
            "R001",
            "student@example.com",
            "SIMULATED"
        )

        output = StringIO()

        with redirect_stdout(output):
            generate_report()

        report = output.getvalue()

        self.assertIn("EMAIL ACTIVITY REPORT", report)
        self.assertIn("Total activities: 1", report)
        self.assertIn("R001", report)
        self.assertIn("student@example.com", report)


if __name__ == "__main__":
    unittest.main()
