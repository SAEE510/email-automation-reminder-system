\# Email Automation \& Reminder System



A Python-based project that automates reminder management and generates personalized email notifications using CSV data, reusable templates, and scheduled reminders.



\## Features



\- Contact management using CSV files

\- Reminder data management

\- Contact and reminder validation

\- Reusable email templates

\- Automatic email personalization

\- Due and upcoming reminder detection

\- Email sending simulation

\- Optional SMTP integration

\- Activity logging and reporting

\- Duplicate reminder protection



\## Technologies Used



\- Python 3

\- CSV

\- SMTP

\- Pandas

\- Schedule

\- Git and GitHub



\## Project Structure



```text

Email-Automation-Reminder-System/

│

├── data/

│   ├── contacts.csv

│   └── reminders.csv

│

├── docs/

│   └── PROJECT\_NOTES.md

│

├── images/

├── logs/

├── outputs/

├── src/

│   ├── automation.py

│   ├── config.py

│   ├── data\_loader.py

│   ├── mailer.py

│   └── reporting.py

│

├── templates/

│   ├── class\_reminder.txt

│   └── task\_reminder.txt

│

├── main.py

├── requirements.txt

├── .gitignore

└── README.md

```



\## Installation



1\. Clone the repository:



```bash

git clone https://github.com/YOUR\_USERNAME/email-automation-reminder-system.git

```



2\. Open the project directory:



```bash

cd email-automation-reminder-system

```



3\. Create a virtual environment:



```bash

python -m venv .venv

```



4\. Activate it on Windows:



```cmd

.venv\\Scripts\\activate

```



5\. Install dependencies:



```bash

pip install -r requirements.txt

```



\## Usage



Run the project:



```bash

python main.py

```



The program loads contacts and reminders, identifies due reminders, generates personalized email content, simulates sending, and records activity.



\## Email Safety



\- Email simulation is the default mode.

\- No real emails are sent by the default program.

\- SMTP integration is optional and disabled by default.

\- Credentials are read from environment variables.

\- Never commit passwords or private contact information.



\## Testing



The project has been tested for:



\- Contact loading and validation

\- Reminder loading and validation

\- Email template generation

\- Email personalization

\- Due reminder detection

\- Email simulation

\- SMTP safety protection

\- Activity logging

\- Duplicate reminder protection



\## Future Improvements



\- SQLite database integration

\- Web-based dashboard

\- Advanced scheduling

\- Automated reporting

\- Improved error handling



\## Project Purpose



This project was developed as a Python learning and portfolio project to demonstrate file handling, modular programming, automation logic, email templates, scheduling, and logging.



\*\*Note:\*\* This is a local student prototype, not a deployed enterprise email automation service.

