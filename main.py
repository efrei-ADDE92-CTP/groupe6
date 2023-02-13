from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
import uvicorn
from starlette.responses import JSONResponse, Response
from starlette.middleware import Middleware
from starlette_exporter import PrometheusMiddleware, handle_metrics
from prometheus_client import Counter, Histogram, Info, Summary, generate_latest
import prometheus_client
import joblib
import schemas
import pandas as pd
import numpy as np
import json
import time


api_router = FastAPI() # APIRouter()
api_router.add_middleware(PrometheusMiddleware)
api_router.add_route("/metrics", handle_metrics)

with open('rf.sav', 'rb') as file :
    loaded_model = joblib.load(file)

# Define the metric variables
predict_calls_counter = Counter('total_predict_calls', 'Number of predict requests to the API endpoint')
predict_call_duration = Histogram('predict_latency_seconds', 'Latency time of the API for a predict call')
# api_info = Info('api_info', 'Information about the API')
# api_summary = Summary('api_request_size_bytes', 'The size of the API request')


@api_router.post("/predict", status_code=200)
async def predict(input_data: schemas.Iris) :
    """
    Make predictions with the Fraud detection model
    """

    # Labels
    iris_labels = ['iris setosa', 'iris versicolor', 'iris virginica']

    start_time = time.time()
    
    # Convert input type schemas.Iris to JSON object and then into a Python object
    data = json.loads(input_data.json())

    # Extract only values and convert them to numpy 
    X = np.array(list(data.values())).reshape(1, -1)

    # Get prediction
    pred = loaded_model.predict(X)

    # Convert Python object into a string in JSON object format
    # json_pred = json.dumps(pred.tolist())

    # Get the prediction label
    iris_pred = iris_labels[pred[0]]
    result = {'prediction': iris_pred}

    # Increment the counter
    predict_calls_counter.inc()

    # Get the request time duration
    predict_call_duration.labels(pred).observe(time.time() - start_time)

    return result # pred.tolist()
    # curl 'http://localhost:8080/predict' -H 'Content-Type: application/json' -d '{"sepal_l": 5, "sepal_w": 2, "petal_l": 3, "petal_w": 4}'


# Define the metrics endpoint
@api_router.post("/metrics") # @api_router.get("/metrics")
def get_counter() :
    return generate_latest(predict_calls_counter).decode("utf-8") # return generate_latest().decode("utf-8")
    # curl 'http://localhost:8080/metrics' -H 'Content-Type: application/json' -d '{"sepal_l": 5, "sepal_w": 2, "petal_l": 3, "petal_w": 4}'


@api_router.post('/metrics/duration')
def get_duration() :
    return generate_latest(predict_call_duration).decode("utf-8")
    # curl 'http://localhost:8080/metrics/duration' -H 'Content-Type: application/json' -d '{"sepal_l": 5, "sepal_w": 2, "petal_l": 3, "petal_w": 4}'


if __name__ == '__main__' :
    uvicorn.run(api_router, host="0.0.0.0", port=8080) # api_router.run(host='0.0.0.0', port=8080, debug=False)
