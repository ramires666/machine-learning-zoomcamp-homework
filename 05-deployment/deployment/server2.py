from fastapi import FastAPI
from pydantic import BaseModel
import pickle

app = FastAPI()

class Client(BaseModel):
    lead_source: str
    number_of_courses_viewed: int
    annual_income: float

pipeline_file = 'pipeline_v2.bin'
with open(pipeline_file, 'rb') as f_in:
    dict_vectorizer, model = pickle.load(f_in)

@app.post("/predict")
async def root(client_data: Client):
    client_dict = client_data.dict()
    X = dict_vectorizer.transform([client_dict])
    result = model.predict_proba(X)[0, 1]
    return result