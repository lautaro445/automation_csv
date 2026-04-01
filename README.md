Automation CSV Email Sender
Description

This project processes CSV files with customer data, validates email addresses, filters them by domain, and sends automated messages. It can run in simulation mode or real sending mode via SMTP (Gmail or any other server).

Installation
Clone the repository:
git clone <your-repo-url>
cd automation_csv
Create and activate a virtual environment:
python3 -m venv my_env
source my_env/bin/activate
Install dependencies:
pip install -r requirements.txt
Create a .env file with SMTP credentials:
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=generated_app_password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

Do not commit .env to the repository. Add it to .gitignore.

Usage
Simulation Mode

Does not send emails, only generates logs:

python3 main.py -i data --simulate
Real Sending Mode

Sends actual emails using SMTP:

python3 main.py -i data --send
Limit Emails for Testing
python3 main.py -i data --send --limit 5
Flag Validation
You cannot use --simulate and --send at the same time.
If no emails remain after filtering, the script will warn and exit without error.
Output

Generated files are saved in the output folder:

filtered_emails.csv – emails filtered by domain
valid_emails.csv – all valid emails
invalid_emails.csv – invalid emails

Logs are saved in logs/app.log:

File loading info
Validation results
Email sending (simulated or real)
Errors per email if any
Example Log
2026-04-01 14:09:44 - INFO - Loaded file: clientes.csv
2026-04-01 14:09:44 - INFO - Valid emails: 3
2026-04-01 14:09:44 - INFO - Invalid emails: 1
2026-04-01 14:10:00 - INFO - Running in simulation mode
[SEND] Email to jairo@gmail.com (simulated)
[SEND] Email to fausto@gmail.com (simulated)
Recommendations
Generate a Gmail App Password and use it in .env.
Always test first with --simulate before sending real emails.
For client demos, use --limit 5 or another low number.
