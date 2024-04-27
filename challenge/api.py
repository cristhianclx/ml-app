import os

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import pandas as pd

from .model import DelayModel
from .schemas import PredictData
from .utils import normalize

# load data
DIR_PATH = os.path.dirname(__file__)
model_data = pd.read_csv(
    filepath_or_buffer=os.path.join(DIR_PATH, "../data/data.csv"),
    low_memory=False,
)

# load model
model = DelayModel()
model_features, model_target = model.preprocess(
    data=model_data,
    target_column="delay",
)
model.fit(
    features=model_features,
    target=model_target,
)


app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )



@app.get("/health", status_code=200)
async def get_health() -> dict:
    return {"status": "OK"}


@app.post("/predict", status_code=200)
async def post_predict(data: PredictData) -> dict:
    data = pd.DataFrame([d.model_dump() for d in data.flights])
    features = normalize(data, add_missing_columns=True)
    predictions = model.predict(
        features=features,
    )
    return {"predict": predictions}