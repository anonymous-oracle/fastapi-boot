from fastapi import FastAPI
from enum import Enum


class ModelName(str, Enum):
    alexnet = "alexnet"
    lenet = "lenet"
    resnet = "resnet"


app = FastAPI()


@app.get("/model/{model_name}")
async def get_model(model_name):
    if ModelName.alexnet.value == model_name:
        return {"model_name": model_name, "message": "A deep model"}
    if ModelName.resnet.value == model_name:
        return {"model_name": model_name, "message": "A residual model"}
    return {"model_name": model_name, "message": "A convoluted model"}
