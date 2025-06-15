from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd
import os
import numpy as np
from dotenv import load_dotenv # Import load_dotenv

# Load environment variables from .env file (if it exists)
load_dotenv()

# --- Configuration ---
MODEL_PATH = 'model/churn_model_clean.pkl' # Ensure this points to your latest model

# --- FastAPI App Initialization ---
app = FastAPI(
    title="Customer Churn Prediction API",
    description="API for predicting customer churn and suggesting retention strategies for service providers in India.",
    version="1.0.0"
)
origins = [
    "http://localhost:3000", # For local frontend development
    "https://customer-churn-prediction-two.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods (GET, POST, etc.)
    allow_headers=["*"], # Allows all headers
)


# --- Load Trained Model ---
model_pipeline = None
try:
    # Adjust MODEL_PATH for execution from backend/ directory if your model is in backend/model/
    # If main.py is directly in 'backend/', and model is in 'backend/model/', then 'model/churn_model_clean.pkl' is correct.
    # If main.py is in 'backend/app/' and model is in 'backend/model/', it would be '../model/churn_model_clean.pkl'
    # Assuming main.py is in 'backend/' for now based on your structure screenshot.
    
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model not found at {MODEL_PATH}")
    model_pipeline = joblib.load(MODEL_PATH)
    print("✅ Model loaded successfully.")
except Exception as e:
    raise RuntimeError(f"❌ Failed to load model: {e}")

# --- Request Model ---
class ChurnPredictionRequest(BaseModel):
    Age: float
    Gender: str
    Tenure: float
    Usage_Frequency: float
    Support_Calls: float
    Payment_Delay: float
    Subscription_Type: str
    Contract_Length: str
    Last_Interaction: float

class ChurnPredictionResponse(BaseModel):
    predicted_churn: int
    churn_probability: float
    retention_strategy: str
    message: str
    churn_risk_level: str

class RecommendationResponse(BaseModel):
    retention_strategy: str
    predicted_churn_status: str
    message: str
    churn_risk_level: str

def get_churn_risk_level(probability: float) -> str:
    bins = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    labels = ['Very Low', 'Low', 'Medium', 'High', 'Very High']
    idx = np.clip(np.digitize(probability, bins) - 1, 0, len(labels) - 1)
    return labels[idx]

# --- Retention Strategy Logic ---
def get_retention_strategy(data: ChurnPredictionRequest, predicted_churn: int, churn_risk_level: str) -> str:
    if predicted_churn == 1:
        if churn_risk_level == "Very High":
            return "Urgent, multi-channel proactive intervention with high-value offers."
        elif churn_risk_level == "High":
            if data.Support_Calls >= 5 or data.Payment_Delay >= 10:
                return "Proactive support outreach and payment flexibility offers."
            elif data.Contract_Length == "Monthly":
                return "Offer discounts for longer contract (e.g., Annual) or premium features."
            else:
                return "Reinforce overall value proposition with personalized offers."
        elif churn_risk_level == "Medium":
            return "Targeted engagement campaigns and satisfaction surveys."
        else: # Covers Low and Very Low churn predicted as 1 (shouldn't happen often)
            return "Investigate model discrepancy; monitor closely and address minor issues."
    else: # Predicted not to churn (0)
        if churn_risk_level in ["High", "Very High"]: # If model predicts 0 but probability is high (borderline)
            return "Monitor customer satisfaction and consider proactive loyalty programs."
        elif churn_risk_level == "Medium":
            return "General loyalty programs and check-ins."
        else: # Low or Very Low risk
            return "Monitor customer satisfaction and reward loyalty."

# --- Root ---
@app.get("/")
async def root():
    return {"message": "Welcome to the Customer Churn Prediction API!", "docs": "/docs"}

# --- Predict Churn ---
@app.post("/predict_churn/", response_model=ChurnPredictionResponse)
async def predict_churn(data: ChurnPredictionRequest):
    if model_pipeline is None:
        raise HTTPException(status_code=500, detail="Model not loaded.")
    try:
        rename_map = {
            "Usage_Frequency": "Usage Frequency",
            "Support_Calls": "Support Calls", 
            "Payment_Delay": "Payment Delay", 
            "Subscription_Type": "Subscription Type",
            "Contract_Length": "Contract Length",
            "Last_Interaction": "Last Interaction"
        }

        # Create DataFrame from request data and rename columns
        input_df = pd.DataFrame([data.model_dump()]).rename(columns=rename_map) # Use model_dump() for Pydantic v2

        # Ensure correct column order as expected by the trained pipeline
        expected_columns_order = [
            'Age', 'Gender', 'Tenure', 'Usage Frequency', 'Support Calls',
            'Payment Delay', 'Subscription Type', 'Contract Length', 'Last Interaction'
        ]
        input_df = input_df[expected_columns_order]

        # Ensure categorical columns are of 'str' dtype before passing to pipeline
        for col in ['Gender', 'Subscription Type', 'Contract Length']:
            input_df[col] = input_df[col].astype(str)

        prob = model_pipeline.predict_proba(input_df)[:, 1][0]
        pred = int(model_pipeline.predict(input_df)[0])
        
        churn_risk_level = get_churn_risk_level(prob) # Calculate risk level
        strategy = get_retention_strategy(data, pred, churn_risk_level) # Pass risk level to strategy logic
        
        msg = "Customer is predicted to churn." if pred == 1 else "Customer is predicted not to churn."

        return ChurnPredictionResponse(
            predicted_churn=pred,
            churn_probability=prob,
            retention_strategy=strategy,
            message=msg,
            churn_risk_level=churn_risk_level # Include in response
        )

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Prediction error: {e}")



# --- Recommend Only ---
@app.post("/recommend/", response_model=RecommendationResponse)
async def recommend_strategy(data: ChurnPredictionRequest):
    if model_pipeline is None:
        raise HTTPException(status_code=500, detail="Model not loaded.")
    try:
        rename_map = {
            "Usage_Frequency": "Usage Frequency",
            "Support_Calls": "Support Calls", # Fixed from Support_Calls to "Support Calls" to match training data
            "Payment_Delay": "Payment Delay", # Fixed from Payment_Delay to "Payment Delay" to match training data
            "Subscription_Type": "Subscription Type",
            "Contract_Length": "Contract Length",
            "Last_Interaction": "Last Interaction"
        }

        # Create DataFrame from request data and rename columns
        input_df = pd.DataFrame([data.model_dump()]).rename(columns=rename_map) # Use model_dump() for Pydantic v2

        # Ensure correct column order as expected by the trained pipeline
        expected_columns_order = [
            'Age', 'Gender', 'Tenure', 'Usage Frequency', 'Support Calls',
            'Payment Delay', 'Subscription Type', 'Contract Length', 'Last Interaction'
        ]
        input_df = input_df[expected_columns_order]

        # Ensure categorical columns are of 'str' dtype before passing to pipeline
        for col in ['Gender', 'Subscription Type', 'Contract Length']:
            input_df[col] = input_df[col].astype(str)
        
        # We need the probability to determine risk level for recommendation
        prob = model_pipeline.predict_proba(input_df)[:, 1][0] 
        pred = int(model_pipeline.predict(input_df)[0])
        
        churn_risk_level = get_churn_risk_level(prob) # Calculate risk level
        strategy = get_retention_strategy(data, pred, churn_risk_level) # Pass risk level to strategy logic
        churn_status = "Customer predicted to churn" if pred == 1 else "Customer predicted not to churn"

        return RecommendationResponse(
            retention_strategy=strategy,
            predicted_churn_status=churn_status,
            message="Recommendation generated successfully.",
            churn_risk_level=churn_risk_level # Include in response
        )

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Recommendation error: {e}")


# --- Uvicorn Server Startup ---
if __name__ == "__main__":
    import uvicorn
    # Get port from environment variable, default to 8080 for local development
    # This ensures compatibility with hosting platforms that set the PORT env var
    PORT = int(os.getenv("PORT", 8080))
    print(f"🚀 Starting FastAPI server on http://0.0.0.0:{PORT}")
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)