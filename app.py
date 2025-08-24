import pickle 
import numpy as np
import pandas as pd
import signin,signup
# from signin import signin
# from signup import signup
from typing import List
from pydantic import BaseModel
from backend.middleware import setup_cors
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from sklearn.preprocessing import LabelEncoder
from fastapi import FastAPI, HTTPException, Query       #new added

# Load your trained ML model
model = pickle.load(open("backend/models/randomforest.pkl", "+rb"))

# ------------------------------------------- MEDICINE DATA  ---------------------------------------------------
MED_CSV = "backend/data/med_dataset/disease2med.csv"     
_med_df = pd.read_csv(MED_CSV).fillna("")
_med_df.columns = [c.strip() for c in _med_df.columns]

def _norm(s: str) -> str:
    return str(s).strip().lower()

def get_medicines_for_disease(disease: str, limit: int = 5):

    d = _norm(disease)
    df = _med_df
    mask = (df["prognosis"].str.lower() == d) | (df["disease_name"].str.lower() == d)
    subset = df.loc[mask]

    meds = (
        subset["med_name"]
        .astype(str).str.strip()
        .replace("", pd.NA).dropna().unique().tolist()
    )

    url = None
    if "disease_url" in subset.columns and not subset.empty:
        urls = subset["disease_url"].astype(str).str.strip()
        urls = urls[urls != ""]
        if not urls.empty:
            url = urls.iloc[0]

    return {
        "disease": disease,
        "medicines": meds[:limit],
        "count": min(len(meds), limit),
        "disease_url": url,
    }
# -----------------------------------------------


# List of symptoms (can come from a file or database)
train_df = pd.read_csv('backend/data/disease_prediction_dataset/Training.csv')
train_df.columns = train_df.columns.str.replace('_',' ')
all_symptoms = train_df.drop(columns=['prognosis']).columns.tolist()

le = LabelEncoder()
le.fit(train_df['prognosis'])
# SYMPTOMS = ["itching","skin rash","nodal skin eruptions","continuous sneezing","shivering","chills","joint pain","stomach pain","acidity","ulcers on tongue","muscle wasting","vomiting","burning micturition","spotting  urination","fatigue","weight gain","anxiety","cold hands and feets","mood swings","weight loss","restlessness","lethargy","patches in throat","irregular sugar level","cough","high fever","sunken eyes","breathlessness","sweating","dehydration","indigestion","headache","yellowish skin","dark urine","nausea","loss of appetite","pain behind the eyes","back pain","constipation","abdominal pain","diarrhoea","mild fever","yellow urine","yellowing of eyes","acute liver failure","fluid overload","swelling of stomach","swelled lymph nodes","malaise","blurred and distorted vision","phlegm","throat irritation","redness of eyes","sinus pressure","runny nose","congestion","chest pain","weakness in limbs","fast heart rate","pain during bowel movements","pain in anal region","bloody stool","irritation in anus","neck pain","dizziness","cramps","bruising","obesity","swollen legs","swollen blood vessels","puffy face and eyes","enlarged thyroid","brittle nails","swollen extremeties","excessive hunger","extra marital contacts","drying and tingling lips","slurred speech","knee pain","hip joint pain","muscle weakness","stiff neck","swelling joints","movement stiffness","spinning movements","loss of balance","unsteadiness","weakness of one body side","loss of smell","bladder discomfort","foul smell of urine","continuous feel of urine","passage of gases","internal itching","toxic look (typhos)","depression","irritability","muscle pain","altered sensorium","red spots over body","belly pain","abnormal menstruation","dischromic  patches","watering from eyes","increased appetite","polyuria","family history","mucoid sputum","rusty sputum","lack of concentration","visual disturbances","receiving blood transfusion","receiving unsterile injections","coma","stomach bleeding","distention of abdomen","history of alcohol consumption","fluid overload.1","blood in sputum","prominent veins on calf","palpitations","painful walking","pus filled pimples","blackheads","scurring","skin peeling","silver like dusting","small dents in nails","inflammatory nails","blister","red sore around nose","yellow crust ooze"]
# "continuous sneezing","shivering","chills","joint pain","stomach pain"

# FastAPI app
app = FastAPI()

app.mount("/static", StaticFiles(directory="static", html=True), name="static")

app.include_router(signup.router)
app.include_router(signin.router)

setup_cors(app)

# Request body model
class SymptomsRequest(BaseModel):
    symptoms: List[str]


@app.get("/symptoms")
def get_symptoms():
    return {"symptoms": all_symptoms}


@app.post("/predict")
def predict_disease(data: SymptomsRequest):
    selected = data.symptoms

    # Validate: at least 4 symptoms
    if len(selected) < 4:
        raise HTTPException(status_code=400, detail="Select at least 4 symptoms")

    # Convert symptoms to model input format (example: binary encoding)
    # # Get prediction from model
    user_input = np.zeros((1, len(all_symptoms)), dtype=int)
    for idx, s in enumerate(all_symptoms):
        if s in selected:
            user_input[0, idx] = 1
    best_class = model.predict(user_input)[0]
    disease = le.inverse_transform([best_class])[0]
    return f"Predicted disease: {disease}"

@app.get("/medicines/{disease}")
def medicines_endpoint(
    disease: str,
    limit: int = Query(5, ge=1, le=10, description="Max medicines to return"),
):
    
    try:
        result = get_medicines_for_disease(disease, limit)
        if result["count"] == 0:
            result["message"] = "No medicines found. Check disease spelling or update CSV."
        else:
            result["message"] = "Success"
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
