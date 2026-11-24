import os

# Email server configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465

# Read credentials from environment variables
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "")

# Safe default: email sending is disabled
EMAIL_ENABLED = False