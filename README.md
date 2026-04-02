Automation CSV Email Sender

What it does
Automation CSV Email Sender is a tool that processes CSV files with customer data, validates email addresses, filters them by domain, and sends automated messages. It can run in simulation mode (no emails sent) or real sending mode via SMTP (Gmail or any other server).

It is Dockerized and comes with ready-to-use scripts for Linux/Mac (run.sh) and Windows (run.bat).

Installation
Clone the repository:
git clone https://github.com/lautaro445/automation_csv.git
cd automation_csv

(Optional) Using virtual environment:
python3 -m venv my_env
source my_env/bin/activate  # Linux/Mac
my_env\Scripts\activate     # Windows

Install dependencies:
pip install -r requirements.txt

Set SMTP credentials (create a .env file):
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_app_password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

Important: Do not commit .env to Git. It's included in .gitignore.

Usage
Linux / Mac
./run.sh simulate          # Run in simulation mode (default)
./run.sh send [LIMIT]      # Send real emails, optional LIMIT

Note: You may need sudo if you get permission errors:
sudo ./run.sh simulate

Windows
run.bat simulate           # Run in simulation mode (default)
run.bat send [LIMIT]       # Send real emails, optional LIMIT

Examples
Simulation mode (no emails sent):
./run.sh simulate
Send actual emails with limit of 5:
./run.sh send 5
Simulation mode with limit:
./run.sh simulate 10

Features
Validates CSV columns (email required, name optional)
Normalizes column names automatically
Filters emails by domain (default: gmail.com)
CLI flags:
--simulate → simulate sending
--send → send real emails
--limit N → process only N emails
Logging to logs/app.log (loading, validation, sending)
Multiple outputs in output/:
filtered_emails.csv → filtered by domain
valid_emails.csv → all valid emails
invalid_emails.csv → invalid emails
Final summary after execution:
====== SUMMARY ======
Total processed: X
Valid emails: X
Invalid emails: X
Emails sent: X
====================

Recommendations
Always test first with --simulate.
For demos or testing, use --limit 5 or a low number.
Generate a Gmail App Password for real sending.
Keep .env private.

Output & Logs
output/ → CSV files
logs/app.log → detailed processing and sending logs

Notes for Users
Works on Linux, Windows, and Mac (with Docker installed).
Scripts (run.sh / run.bat) simplify execution: no need to touch Python code.
If errors occur, check logs/app.log for detailed messages.
