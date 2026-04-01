import os
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def load_csvs(input_folder):
	all_dfs = []
	for file in os.listdir(input_folder):
		if file.endswith(".csv"):
			path = f"{input_folder}/{file}"
			try:
				df = pd.read_csv(path)
				all_dfs.append(df)
				logger.info(f"Loaded file: {file}")
			except Exception as e:
				logger.error(f"Error reading {file}: {e}")
	if not all_dfs:
		logger.error("No valid CSV files found")
		raise FileNotFoundError("No csv Files found")
	df = pd.concat(all_dfs,ignore_index=True)
	return df

def save_csv(df, output_path):
	df.to_csv(output_path, index=False, encoding="utf-8")
	logger.info(f"Saved CSV: {output_path}")
