
import unittest
from datetime import datetime
from unittest.mock import patch

from src.automation import (
    get_due_reminders,
    get_upcoming_reminders,
)


class TestReminderScheduling(unittest.TestCase):

    def setUp(self):
        self.current_time = datetime(2026, 11, 24, 12, 0)

        self.reminders = [
            {
                "reminder_id": "R001",
                "due_datetime": "2026-11-24 10:00",
                "status": "pending",
            },
            {
                "reminder_id": "R002",
                "due_datetime": "2026-11-24 14:00",
                "status": "pending",
            },
            {
                "reminder_id": "R003",
                "due_datetime": "2026-11-24 11:00",
                "status": "completed",
            },
            {
                "reminder_id": "R004",
                "due_datetime": "2026-11-24 12:00",
                "status": "pending",
            },
            {
                "reminder_id": "R005",
                "due_datetime": "2026-11-25 09:00",
                "status": "PENDING",
            },
        ]

    @patch("src.automation.datetime")
    def test_get_due_reminders(self, mock_datetime):
        mock_datetime.now.return_value = self.current_time
        mock_datetime.strptime = datetime.strptime

        result = get_due_reminders(self.reminders)

        reminder_ids = [r["reminder_id"] for r in result]

        self.assertEqual(reminder_ids, ["R001", "R004"])

    @patch("src.automation.datetime")
    def test_get_upcoming_reminders(self, mock_datetime):
        mock_datetime.now.return_value = self.current_time
        mock_datetime.strptime = datetime.strptime

        result = get_upcoming_reminders(self.reminders)

        reminder_ids = [r["reminder_id"] for r in result]

        self.assertEqual(reminder_ids, ["R002", "R005"])

    @patch("src.automation.datetime")
    def test_due_reminders_excludes_completed(self, mock_datetime):
        mock_datetime.now.return_value = self.current_time
        mock_datetime.strptime = datetime.strptime

        result = get_due_reminders(self.reminders)

        self.assertNotIn(
            "R003",
            [r["reminder_id"] for r in result]
        )

    @patch("src.automation.datetime")
    def test_upcoming_reminders_excludes_completed(self, mock_datetime):
        mock_datetime.now.return_value = self.current_time
        mock_datetime.strptime = datetime.strptime

        result = get_upcoming_reminders(self.reminders)

        self.assertNotIn(
            "R003",
            [r["reminder_id"] for r in result]
        )

    @patch("src.automation.datetime")
    def test_due_reminders_returns_empty_list(self, mock_datetime):
        mock_datetime.now.return_value = self.current_time
        mock_datetime.strptime = datetime.strptime

        result = get_due_reminders([])

        self.assertEqual(result, [])

    @patch("src.automation.datetime")
    def test_upcoming_reminders_returns_empty_list(self, mock_datetime):
        mock_datetime.now.return_value = self.current_time
        mock_datetime.strptime = datetime.strptime

        result = get_upcoming_reminders([])

        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
