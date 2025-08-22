import pandas as pd

def build_features(path: str) -> pd.DataFrame:
    """Build ML features from cleaned data."""
    df = pd.read_csv(path, parse_dates=['date_posted'])
    # Date-based features
    df['month'] = df['date_posted'].dt.month
    df['weekday'] = df['date_posted'].dt.weekday
    # One-hot encode job_type
    df = pd.get_dummies(df, columns=['job_type'], prefix='type')
    return df

if __name__ == "__main__":
    features = build_features("data/processed/clean_jobs.csv")
    features.to_csv("data/processed/features.csv", index=False)
    print("Features saved to data/processed/features.csv")
