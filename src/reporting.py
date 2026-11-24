import csv
from datetime import datetime
from pathlib import Path


LOG_FILE = Path("logs/email_log.csv")


def log_email_activity(
    reminder_id,
    recipient,
    status,
    details=""
):
    """Record email activity in a CSV log."""

    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    file_exists = LOG_FILE.exists()

    with LOG_FILE.open(
        "a", newline="", encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "timestamp",
                "reminder_id",
                "recipient",
                "status",
                "details"
            ])

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            reminder_id,
            recipient,
            status,
            details
        ])


def generate_report():
    """Display a summary of recorded email activities."""

    if not LOG_FILE.exists():
        print("No email activity recorded yet.")
        return

    with LOG_FILE.open(
        "r", newline="", encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)
        records = list(reader)

    print("\nEMAIL ACTIVITY REPORT")
    print("=" * 35)
    print("Total activities:", len(records))

    for record in records:
        print(
            record["reminder_id"],
            "|",
            record["recipient"],
            "|",
            record["status"]
        )
def was_reminder_processed(reminder_id):
    """Check whether a reminder was already processed."""

    if not LOG_FILE.exists():
        return False

    with LOG_FILE.open(
        "r", newline="", encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for record in reader:
            if (
                record["reminder_id"] == reminder_id
                and record["status"] in ("SIMULATED", "SENT")
            ):
                return True

    return False