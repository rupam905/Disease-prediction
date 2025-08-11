from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle  # or pickle
from typing import List

# Load your trained ML model
model = pickle.load("disease_model.pkl")

# List of symptoms (can come from a file or database)
SYMPTOMS = [
    "fever", "headache", "cough", "fatigue", "nausea", 
    "shortness of breath", "sore throat", "chest pain"
]

# FastAPI app
app = FastAPI()

# Request body model
class SymptomsRequest(BaseModel):
    symptoms: List[str]

@app.get("/symptoms")
def get_symptoms():
    return {"symptoms": SYMPTOMS}

@app.post("/predict")
def predict_disease(data: SymptomsRequest):
    selected = data.symptoms

    # Validate: at least 4 symptoms
    if len(selected) < 4:
        raise HTTPException(status_code=400, detail="Select at least 4 symptoms")

    # Convert symptoms to model input format (example: binary encoding)
    input_vector = [1 if s in selected else 0 for s in SYMPTOMS]

    # Get prediction from model
    prediction = model.predict([input_vector])[0]

    return {"prediction": prediction}
