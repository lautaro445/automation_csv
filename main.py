import os
import argparse
from modules.csv_handler import load_csvs, save_csv
from modules.validator import normalize_columns, detect_email_column, detect_name_column, validate_emails
from modules.email_sender import send_bulk_emails
from modules.logger_config import logger

# --------------------------
# Argument parsing
# --------------------------
parser = argparse.ArgumentParser(description="CSV Email Automation Tool")
parser.add_argument("-i", "--input", required=True, help="Input folder containing CSV files")
parser.add_argument("-o", "--output", default="output", help="Output folder for processed CSVs")
parser.add_argument("-d", "--domain", default="gmail.com", help="Domain filter for emails")
parser.add_argument("--simulate", action="store_true", help="Simulate email sending (default mode)")
parser.add_argument("--send", action="store_true", help="Send real emails via SMTP")
parser.add_argument("--limit", type=int, help="Limit the number of emails to process")
args = parser.parse_args()

# --------------------------
# Default to simulation mode if no flag is provided
# --------------------------
if not args.simulate and not args.send:
    print("No sending mode specified. Running in simulation mode by default.")
    args.simulate = True

# --------------------------
# Validate flags
# --------------------------
if args.simulate and args.send:
    logger.error("Cannot use --simulate and --send at the same time")
    raise ValueError("Cannot use --simulate and --send at the same time")

# --------------------------
# Ensure output folder exists
# --------------------------
os.makedirs(args.output, exist_ok=True)

# --------------------------
# Load CSVs
# --------------------------
df = load_csvs(args.input)
df = normalize_columns(df)

# --------------------------
# Column validation - required: email, optional: name
# --------------------------
if "email" not in df.columns:
    error_msg = "CSV is missing required 'email' column"
    logger.error(error_msg)
    raise ValueError(error_msg)

if "name" not in df.columns:
    logger.warning("CSV is missing optional 'name' column. Emails will use 'User' as fallback.")

# --------------------------
# Detect columns
# --------------------------
email_col = detect_email_column(df)
name_col = detect_name_column(df)

# --------------------------
# Validate and filter emails
# --------------------------
valid_df, invalid_df = validate_emails(df, email_col)
filtered_df = valid_df[valid_df[email_col].str.endswith(args.domain)]

if filtered_df.empty:
    logger.warning("No emails to process after filtering")
    print("No emails matched the domain filter. Exiting.")
    exit(0)

if args.limit:
    filtered_df = filtered_df.head(args.limit)

# --------------------------
# Save CSV outputs
# --------------------------
save_csv(filtered_df, f"{args.output}/filtered_emails.csv")
save_csv(invalid_df, f"{args.output}/invalid_emails.csv")
save_csv(valid_df, f"{args.output}/valid_emails.csv")

# --------------------------
# Send emails with error handling
# --------------------------
emails_sent = 0
emails_failed = 0

try:
    if args.simulate:
        logger.info("Running in simulation mode")
        emails_sent, emails_failed, _ = send_bulk_emails(filtered_df, email_col, name_col, simulate=True)
    elif args.send:
        logger.info("Sending real emails")
        emails_sent, emails_failed, _ = send_bulk_emails(filtered_df, email_col, name_col, simulate=False)
except Exception as e:
    logger.error(f"Failed to send emails: {e}")
    print("Some emails could not be sent. Check logs/app.log for details.")

# --------------------------
# Final summary
# --------------------------
total_processed = len(df)
valid_emails = len(valid_df)
invalid_emails = len(invalid_df)

print(f"""
====== SUMMARY ======
Total processed: {total_processed}
Valid emails: {valid_emails}
Invalid emails: {invalid_emails}
Emails sent: {emails_sent}
====================
""")
