
import csv
import os
import tempfile
import unittest

from src.data_loader import load_contacts, load_reminders


class TestContactLoader(unittest.TestCase):

    def create_csv(self, headers, rows):
        temp = tempfile.NamedTemporaryFile(
            mode="w",
            newline="",
            encoding="utf-8",
            suffix=".csv",
            delete=False
        )

        writer = csv.writer(temp)
        writer.writerow(headers)
        writer.writerows(rows)
        temp.close()

        self.addCleanup(
            lambda: os.path.exists(temp.name)
            and os.remove(temp.name)
        )

        return temp.name

    def test_load_valid_contacts(self):
        path = self.create_csv(
            ["contact_id", "name", "email", "department"],
            [
                ["C001", "Aarav Sharma", "aarav@example.com", "HR"],
                ["C002", "Priya Patel", "priya@example.com", "Training"]
            ]
        )

        contacts = load_contacts(path)

        self.assertEqual(len(contacts), 2)
        self.assertEqual(contacts[0]["name"], "Aarav Sharma")

    def test_missing_required_column(self):
        path = self.create_csv(
            ["contact_id", "name", "email"],
            [["C001", "Aarav", "aarav@example.com"]]
        )

        with self.assertRaises(ValueError):
            load_contacts(path)

    def test_missing_contact_information(self):
        path = self.create_csv(
            ["contact_id", "name", "email", "department"],
            [["C001", "", "aarav@example.com", "HR"]]
        )

        with self.assertRaises(ValueError):
            load_contacts(path)

    def test_duplicate_contact_id(self):
        path = self.create_csv(
            ["contact_id", "name", "email", "department"],
            [
                ["C001", "Aarav", "aarav@example.com", "HR"],
                ["C001", "Priya", "priya@example.com", "IT"]
            ]
        )

        with self.assertRaises(ValueError):
            load_contacts(path)

    def test_duplicate_email(self):
        path = self.create_csv(
            ["contact_id", "name", "email", "department"],
            [
                ["C001", "Aarav", "aarav@example.com", "HR"],
                ["C002", "Priya", "AARAV@example.com", "IT"]
            ]
        )

        with self.assertRaises(ValueError):
            load_contacts(path)

    def test_invalid_email(self):
        path = self.create_csv(
            ["contact_id", "name", "email", "department"],
            [["C001", "Aarav", "invalid-email", "HR"]]
        )

        with self.assertRaises(ValueError):
            load_contacts(path)


class TestReminderLoader(unittest.TestCase):

    def create_csv(self, headers, rows):
        temp = tempfile.NamedTemporaryFile(
            mode="w",
            newline="",
            encoding="utf-8",
            suffix=".csv",
            delete=False
        )

        writer = csv.writer(temp)
        writer.writerow(headers)
        writer.writerows(rows)
        temp.close()

        self.addCleanup(
            lambda: os.path.exists(temp.name)
            and os.remove(temp.name)
        )

        return temp.name

    def test_load_valid_reminders(self):
        path = self.create_csv(
            [
                "reminder_id",
                "contact_id",
                "reminder_type",
                "due_datetime",
                "template_file",
                "status"
            ],
            [
                [
                    "R001", "C001", "Document Submission",
                    "2026-11-20 09:00",
                    "task_reminder.txt", "pending"
                ]
            ]
        )

        reminders = load_reminders(path)

        self.assertEqual(len(reminders), 1)
        self.assertEqual(reminders[0]["reminder_id"], "R001")

    def test_missing_required_column(self):
        path = self.create_csv(
            ["reminder_id", "contact_id"],
            [["R001", "C001"]]
        )

        with self.assertRaises(ValueError):
            load_reminders(path)

    def test_duplicate_reminder_id(self):
        path = self.create_csv(
            [
                "reminder_id", "contact_id", "reminder_type",
                "due_datetime", "template_file", "status"
            ],
            [
                ["R001", "C001", "Task", "2026-11-20 09:00",
                 "task_reminder.txt", "pending"],
                ["R001", "C002", "Task", "2026-11-21 09:00",
                 "task_reminder.txt", "pending"]
            ]
        )

        with self.assertRaises(ValueError):
            load_reminders(path)

    def test_invalid_reminder_date(self):
        path = self.create_csv(
            [
                "reminder_id", "contact_id", "reminder_type",
                "due_datetime", "template_file", "status"
            ],
            [
                ["R001", "C001", "Task", "invalid-date",
                 "task_reminder.txt", "pending"]
            ]
        )

        with self.assertRaises(ValueError):
            load_reminders(path)


if __name__ == "__main__":
    unittest.main()
