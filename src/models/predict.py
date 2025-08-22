import pandas as pd
import joblib
from datetime import timedelta

def predict_next_days(days: int = 7):
    # Load model
    model = joblib.load("src/models/job_surge_model.pkl")
    
    # Prepare future dates
    last_date = pd.read_csv("data/processed/features.csv", parse_dates=['date_posted'])['date_posted'].max()
    future = [last_date + timedelta(days=i) for i in range(1, days+1)]
    X_future = pd.DataFrame({'date_ord': [d.toordinal() for d in future]})
    
    # Predict
    preds = model.predict(X_future)
    for d, p in zip(future, preds):
        print(f"{d.date()}: {max(0, int(p))} predicted postings")

if __name__ == "__main__":
    predict_next_days(7)
