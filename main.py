import os
import argparse
from modules.csv_handler import load_csvs, save_csv
from modules.validator import normalize_columns, detect_email_column, detect_name_column, validate_emails
from modules.email_sender import send_bulk_emails
from modules.logger_config import logger

parser = argparse.ArgumentParser(description="Filter and send emails from CSV")
parser.add_argument("-i", "--input", required=True, help="Input folder")
parser.add_argument("-o", "--output", default="output", help="Output folder")
parser.add_argument("-d", "--domain", default="gmail.com", help="Domain filter")
parser.add_argument("--simulate", action="store_true", help="Simulate sending")
parser.add_argument("--send", action="store_true", help="Send real emails")
parser.add_argument(
	"--limit",
	type=int,
	help="Number emails to sender(optional)"
)

args = parser.parse_args()

if args.simulate and args.send:
	logger.error("Cannot use --simulate and --send together")
	exit(1)


os.makedirs(args.output, exist_ok=True)

df = load_csvs(args.input)
df = normalize_columns(df)
email_col = detect_email_column(df)
name_col = detect_name_column(df)

valid_df, invalid_df = validate_emails(df, email_col)
filtered_df = valid_df[valid_df[email_col].str.endswith(args.domain)]

if filtered_df.empty:
	logger.warning("No emails to process after filtering")
	exit(0)

if args.limit:
	filtered_df = filtered_df.head(args.limit)

# Guardar archivos consistentes
save_csv(filtered_df, f"{args.output}/filtered_emails.csv")
save_csv(invalid_df, f"{args.output}/invalid_emails.csv")
save_csv(valid_df, f"{args.output}/valid_emails.csv")

# Enviar emails
if args.simulate:
    logger.info("Running in simulation mode")
    send_bulk_emails(filtered_df, email_col, name_col, simulate=True)
elif args.send:
    logger.info("Sending real emails")
    send_bulk_emails(filtered_df, email_col, name_col, simulate=False)
else:
    logger.info("No sending mode selected. Use --simulate or --send")
