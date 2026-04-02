import smtplib
from email.message import EmailMessage
from modules.logger_config import logger
from tqdm import tqdm
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

def send_email(to_email, to_name, simulate=True):
    try:
        msg = EmailMessage()
        msg['Subject'] = "Automated message"
        msg['From'] = EMAIL_USER
        msg['To'] = to_email
        msg.set_content(f"Hello {to_name},\n\nThis is a custom automated message.\n\nBest regards,\nYour Company")
        
        if simulate:
            logger.info(f"[SIMULATE] Sending email to {to_email}")
            return True
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
        
        logger.info(f"[OK] Email sent to {to_email}")
        return True
    except Exception as e:
        logger.error(f"[FAIL] Email to {to_email} failed: {e}")
        return False

def send_bulk_emails(df, email_col, name_col, simulate=True):
    results = []
    failed_emails = []
    for _, row in tqdm(df.iterrows(), total=len(df), desc="Sending emails"):
        try:
            success = send_email(row[email_col], row[name_col] if name_col else "User", simulate)
            results.append((row[email_col], success))
            if not success:
                failed_emails.append(row[email_col])
        except Exception as e:
            logger.error(f"[CRITICAL] Unexpected error for {row[email_col]}: {e}")
            results.append((row[email_col], False))
            failed_emails.append(row[email_col])
    
    # Final report
    sent = sum(1 for _, ok in results if ok)
    failed = len(results) - sent
    logger.info(f"Bulk send completed: {len(results)} processed, {sent} sent, {failed} failed")
    
    # Return tuple for detailed tracking in main.py
    return sent, failed, results
