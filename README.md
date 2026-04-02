Automation CSV Email Sender
What it does

This project processes CSV files with customer data:

Validates email addresses
Filters emails by domain (default: gmail.com)
Generates output CSV files: valid, invalid, and filtered emails
Optionally sends emails (simulation or real)
Quick Start
Linux / Mac
Open terminal in the project folder
Run simulation:
./run.sh simulate
Send real emails:
./run.sh send
Windows
Open Command Prompt in the project folder
Run simulation:
run.bat simulate
Send real emails:
run.bat send
Input / Output
Place CSV files in the data/ folder
Outputs are saved in output/:
valid_emails.csv → all valid emails
invalid_emails.csv → invalid emails
filtered_emails.csv → emails filtered by domain
Logs are saved in logs/app.log
Email Setup
Create a .env file (do not commit it):
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_app_password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
Generate a Gmail App Password if using Gmail
Test first with simulation before sending real emails
Notes
Simulation mode does not send emails, just logs the process
Real mode sends emails according to the CSV and filters
For demos, limit emails using --limit (see manual)
