from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse
import joblib
import schemas
import pandas as pd
import numpy as np
import json


api_router = APIRouter()
loaded_model = joblib.load('rf.sav')
    

@api_router.post("/predict", status_code=200)
async def predict(input_data: schemas.Iris):
    """
    Make predictions with the Fraud detection model
    """
    
    # convert input type schemas.Iris to Json
    data = json.loads(input_data.json())

    # extract only values and convert to numpy 
    raw_data = np.array(list(data.values()))

    # get prediction
    results = loaded_model.predict(raw_data.reshape(1, -1))
    return results.tolist()


 #curl 'http://localhost:8000/predict' -H 'Content-Type: application/json' -d '{"sepal_l": 5, "sepal_w": 2, "petal_l": 3, "petal_w": 4}'
