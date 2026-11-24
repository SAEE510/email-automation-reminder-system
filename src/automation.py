from datetime import datetime

from src.data_loader import load_reminders


def get_due_reminders(reminders=None):
    """Return reminders that are due and still pending."""

    if reminders is None:
        reminders = load_reminders()

    current_time = datetime.now()
    due_reminders = []

    for reminder in reminders:
        if reminder["status"].lower() != "pending":
            continue

        due_time = datetime.strptime(
            reminder["due_datetime"],
            "%Y-%m-%d %H:%M"
        )

        if due_time <= current_time:
            due_reminders.append(reminder)

    return due_reminders


def get_upcoming_reminders(reminders=None):
    """Return pending reminders scheduled for the future."""

    if reminders is None:
        reminders = load_reminders()

    current_time = datetime.now()
    upcoming_reminders = []

    for reminder in reminders:
        if reminder["status"].lower() != "pending":
            continue

        due_time = datetime.strptime(
            reminder["due_datetime"],
            "%Y-%m-%d %H:%M"
        )

        if due_time > current_time:
            upcoming_reminders.append(reminder)

    return upcoming_reminders