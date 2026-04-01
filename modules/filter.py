def filter_by_domain(df, email_col, domain):
	return df[df[email_col].str.endswith(f"@{domain}")]
