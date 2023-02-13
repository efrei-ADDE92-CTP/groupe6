from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse
from prometheus_client import Counter, Histogram
import prometheus_client
from starlette.responses import Response
from starlette_exporter import PrometheusMiddleware, handle_metrics
import joblib
import schemas
import numpy as np
import json, time


api_router = FastAPI()
api_router.add_middleware(PrometheusMiddleware)
api_router.add_route("/metrics", handle_metrics)

loaded_model = joblib.load('rf.sav')

counter = Counter('predict_reqs', 'Nb of requests to the predict endpoint')

predict_duration = Histogram(
    'predict_duration_secs', 'Time to handle a predict request', ['method']) 


@api_router.post("/predict", status_code=200)
async def predict(input_data: schemas.Iris):
    """
    Make predictions with the Fraud detection model
    """

    request_start = time.time()
    
    # convert input type schemas.Iris to Json
    data = json.loads(input_data.json())

    # extract only values and convert to numpy 
    raw_data = np.array(list(data.values()))

    # get prediction
    results = loaded_model.predict(raw_data.reshape(1, -1))

    # incrémente le compteur
    counter.inc()

    # obtenir la durée de la requête
    predict_duration.labels(results).observe(
        time.time() - request_start)

    return results.tolist()
 #curl 'http://localhost:5000/predict' -H 'Content-Type: application/json' -d '{"sepal_l": 5, "sepal_w": 2, "petal_l": 3, "petal_w": 4}'
 
 
@api_router.route('/metrics', methods=['GET'])
def get_counter():
    return prometheus_client.generate_latest().decode("utf-8")
 #curl 'http://localhost:5000/metrics'

if __name__ == '__main__':
    api_router.run(host='0.0.0.0', port=5000, debug=False)
