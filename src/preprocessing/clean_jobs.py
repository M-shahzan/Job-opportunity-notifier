import pandas as pd

def load_data(path: str) -> pd.DataFrame:
    """Load raw job data from CSV."""
    df = pd.read_csv(path)
    df['date_posted'] = pd.to_datetime(df['date_posted'])
    return df

def clean_jobs(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and normalize raw job postings."""
    # Drop duplicates
    df = df.drop_duplicates(subset=['job_id'])
    # Fill missing skills with “None”
    df['skills_required'] = df['skills_required'].fillna('None')
    # Standardize job_type values
    df['job_type'] = df['job_type'].str.title()
    return df

if __name__ == "__main__":
    raw = load_data("data/raw/sample.csv")
    clean = clean_jobs(raw)
    clean.to_csv("data/processed/clean_jobs.csv", index=False)
    print("Cleaned data saved to data/processed/clean_jobs.csv")
