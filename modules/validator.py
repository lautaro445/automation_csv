import re

from modules.logger_config import logger

EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+$'

def normalize_columns(df):
    df.columns = [col.strip().lower() for col in df.columns]
    return df

def detect_email_column(df):
    for col in df.columns:
        if "mail" in col:
            return col
    logger.error("No email column found")
    raise ValueError("No email column found")

def detect_name_column(df):
    for col in df.columns:
        if "name" in col or "cliente" in col:
            return col
    return None


def validate_emails(df, email_col):
    df[email_col] = df[email_col].astype(str).str.strip().str.lower()

    valid_mask = df[email_col].astype(str).str.match(EMAIL_REGEX)
    valid_df = df[valid_mask].copy()
    invalid_df = df[~valid_mask].copy()
    logger.info(f"Valid emails: {len(valid_df)}")
    logger.info(f"Invalid emails: {len(invalid_df)}")
    return valid_df, invalid_df
