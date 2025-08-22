import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import joblib

def train_model(feature_path: str):
    # Load features
    df = pd.read_csv(feature_path)
    # Aggregate daily counts for surge prediction
    daily = df.groupby('date_posted').size().reset_index(name='count')
    daily['date_ord'] = pd.to_datetime(daily['date_posted']).map(pd.Timestamp.toordinal)
    
    X = daily[['date_ord']]
    y = daily['count']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    # Train
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Evaluate
    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    print(f"MAE: {mae:.2f}")

    # Save model
    joblib.dump(model, "src/models/job_surge_model.pkl")
    print("Model saved to src/models/job_surge_model.pkl")

if __name__ == "__main__":
    train_model("data/processed/features.csv")
