import pandas as pd
import numpy as np
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline
from sklearn.ensemble import RandomForestClassifier

def train_churn_model(data_path: str, model_save_path: str, test_size: float = 0.2, random_state: int = 42):
    """
    Trains a customer churn prediction model and saves it.

    Args:
        data_path (str): Path to the original dataset CSV file.
        model_save_path (str): Directory and filename to save the trained model (e.g., 'model/churn_model_clean.pkl').
        test_size (float): Proportion of the dataset to reserve for testing (used to define X_train for training).
        random_state (int): Controls the shuffling applied to the data before splitting for reproducibility.
    """
    print(f"Attempting to load dataset from: {data_path}")
    if not os.path.exists(data_path):
        print(f"Error: Dataset file not found at {data_path}")
        print("Please ensure your CSV dataset is in the correct relative path.")
        return

    try:
        # Step 3: Load dataset
        df = pd.read_csv(data_path)
        df.drop(['CustomerID'], axis=1, inplace=True)
        df.dropna(inplace=True)
        print(f"✅ Dataset loaded. Shape: {df.shape}")

        # Step 4: Drop potential leakage features
        leak_prone = ['Total Spend']
        for feature in leak_prone:
            if feature in df.columns:
                df.drop([feature], axis=1, inplace=True)
                print(f"🚫 Dropped leak-prone feature: '{feature}'.")
            else:
                print(f"Warning: Leak-prone feature '{feature}' not found in dataset. Skipping.")
        print(f"✅ Dataset after dropping leakage features. Shape: {df.shape}")

        # Step 5: Feature separation
        X = df.drop('Churn', axis=1)
        y = df['Churn'].astype(int)

        num_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
        cat_features = X.select_dtypes(include='object').columns.tolist()

        print("🧮 Numerical features:", num_features)
        print("🔤 Categorical features:", cat_features)

        # Step 6: Preprocessor setup
        preprocessor = ColumnTransformer(transformers=[
            ('num', StandardScaler(), num_features),
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), cat_features)
        ])

        # Step 7: Train/Test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, stratify=y, random_state=random_state
        )
        print(f"📊 Train set size: {len(X_train)}")
        print("📊 Train class distribution:\n", y_train.value_counts(normalize=True))

        # Step 8: Full pipeline with SMOTE and Random Forest
        model_pipeline = ImbPipeline(steps=[
            ('preprocessor', preprocessor),
            ('smote', SMOTE(random_state=random_state)),
            ('classifier', RandomForestClassifier(n_estimators=100, max_depth=10, random_state=random_state))
        ])

        # Step 9: Model training
        model_pipeline.fit(X_train, y_train)
        print("✅ Model training complete.")

        # Step 12: Save the model
        model_dir = os.path.dirname(model_save_path)
        if model_dir and not os.path.exists(model_dir):
            os.makedirs(model_dir)
            print(f"Created directory: {model_dir}")

        joblib.dump(model_pipeline, model_save_path)
        print(f"✅ Model saved as '{model_save_path}'")

    except Exception as e:
        print(f"An error occurred during model training: {e}")

if __name__ == "__main__":
    # Define paths using relative paths for execution from the 'scripts/' directory
    DATA_FILE_PATH = "../data/customer_churn_dataset-training-master.csv"
    MODEL_SAVE_PATH = "../model/churn_model_clean.pkl" # Save location for the trained model

    # Run the model training process
    train_churn_model(DATA_FILE_PATH, MODEL_SAVE_PATH)