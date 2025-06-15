import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix

def evaluate_model(model_path: str, data_path: str, test_size: float = 0.2, random_state: int = 42):
    """
    Loads a trained churn prediction model and evaluates it on a test dataset.

    Args:
        model_path (str): Path to the saved model file (e.g., 'model/churn_model_clean.pkl').
        data_path (str): Path to the original dataset CSV file.
        test_size (float): Proportion of the dataset to include in the test split.
        random_state (int): Controls the shuffling applied to the data before applying the split.
    """
    print(f"Attempting to load model from: {model_path}")
    if not os.path.exists(model_path):
        print(f"Error: Model file not found at {model_path}")
        print("Please ensure the model is trained and saved to this path.")
        return

    print(f"Attempting to load dataset from: {data_path}")
    if not os.path.exists(data_path):
        print(f"Error: Dataset file not found at {data_path}")
        print("Please ensure 'customer_churn_dataset-training-master.csv' is in the correct directory.")
        return

    try:
        # Load the saved model
        model_pipeline = joblib.load(model_path)
        print("✅ Model loaded successfully.")

        # Load the dataset
        df = pd.read_csv(data_path)

        # Replicate preprocessing steps applied during training
        # Drop CustomerID
        if 'CustomerID' in df.columns:
            df.drop(['CustomerID'], axis=1, inplace=True)
            print("🚫 Dropped 'CustomerID'.")
        
        # Drop potential leakage features
        leak_prone = ['Total Spend']
        for feature in leak_prone:
            if feature in df.columns:
                df.drop([feature], axis=1, inplace=True)
                print(f"🚫 Dropped leak-prone feature: '{feature}'.")
            else:
                print(f"Warning: Leak-prone feature '{feature}' not found in dataset. Skipping.")

        # Drop rows with any NaN values
        initial_rows = df.shape[0]
        df.dropna(inplace=True)
        if df.shape[0] < initial_rows:
            print(f"🚫 Dropped {initial_rows - df.shape[0]} rows with NaN values.")
        else:
            print("No NaN values found or dropped.")

        print(f"✅ Dataset prepared. Shape: {df.shape}")

        # Feature separation
        X = df.drop('Churn', axis=1)
        y = df['Churn'].astype(int)

        # Create train/test split with the SAME random_state as training
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, stratify=y, random_state=random_state
        )
        print(f"📊 Test set size: {len(X_test)}")

        # Make predictions
        y_pred = model_pipeline.predict(X_test)
        y_proba = model_pipeline.predict_proba(X_test)[:, 1]

        # Evaluation metrics
        print("\n🔍 Classification Report:")
        print(classification_report(y_test, y_pred))

        print("🎯 ROC AUC Score:", roc_auc_score(y_test, y_proba))

        # Confusion Matrix
        cm = confusion_matrix(y_test, y_pred)
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                    xticklabels=['Predicted No Churn', 'Predicted Churn'],
                    yticklabels=['Actual No Churn', 'Actual Churn'])
        plt.title("Confusion Matrix")
        plt.xlabel("Predicted Label")
        plt.ylabel("True Label")
        plt.show()

    except Exception as e:
        print(f"An error occurred during model evaluation: {e}")

if __name__ == "__main__":
    # Define paths - adjust these if your files are in different locations
    MODEL_FILE_PATH = "../model/churn_model_clean.pkl"
    DATA_FILE_PATH = "../data/customer_churn_dataset-training-master.csv" # Or your actual test dataset

    evaluate_model(MODEL_FILE_PATH, DATA_FILE_PATH)