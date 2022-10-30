import uvicorn
import pandas as pd 
from pydantic import BaseModel
from typing import Literal, List, Union
from fastapi import FastAPI, File, UploadFile
from joblib import dump, load
import json


description = """
Welcome to GetAround pricing API. This app is made for you to predict optimum prices for car owners

## Sample rows

* `/`: **GET** request that display random examples of the data.


## Search model

* `/search_model_key/{model_key}`: **GET** request that retrieve data for a car model


## Machine Learning

This is a Machine Learning endpoint that predict rental price per day. Here is the endpoint:

* `/predict` 

Check out documentation below 👇 for more information on each endpoint. 
"""

tags_metadata = [
    {
        "name": "Sample rows",
        "description": "Simple endpoints to try out!",
    },

    {
        "name": "Search model",
        "description": "Search data for a type of car model"
    },

    {
        "name": "Machine Learning",
        "description": "Prediction Endpoint."
    }
]

app = FastAPI(
    title="GetAround API",
    description=description,
    version="0.1",
    contact={
        "name": "Sylvain Mothes",
        "url" : "https://github.com/Stylomines/GetAround"
    },
    openapi_tags=tags_metadata
)

class PredictionFeatures(BaseModel):
    model_key: object
    mileage: Union[int, float]
    engine_power: Union[int, float]
    fuel:object
    paint_color:object
    car_type:object
    private_parking_available:bool  
    has_gps:bool  
    has_air_conditioning:bool  
    automatic_car:bool  
    has_getaround_connect: bool  
    has_speed_regulator:bool  
    winter_tires:bool  



@app.get("/", tags=["Sample rows"])
async def read_rental_cars_sample():
    """
    display some (5) random examples of the data

    """

    rentals = pd.read_csv("get_around_pricing_project.csv", index_col=0)

    rental = rentals.sample(5)

    return rental.to_dict("index")


@app.get("/Search_model_key/{model_key}", tags=["Search model"])
async def search_model_key(model_key: object):
    """
    Search data by model key :

    Citroën, Peugeot, PGO, Renault, Audi, BMW, Ford,
    Mercedes, Opel, Porsche, Volkswagen, KIA Motors,
    Alfa Romeo, Ferrari, Fiat, Lamborghini, Maserati,
    Lexus, Honda, Mazda, Mini, Mitsubishi, Nissan, SEAT,
    Subaru, Suzuki, Toyota, Yamaha
   
    """

    rentals = pd.read_csv("get_around_pricing_project.csv", index_col=0)

    rental_model = rentals[rentals["model_key"]==model_key]

    return rental_model.to_dict("index")


@app.post("/predict", tags=["Machine Learning"])
async def predict(predictionFeatures: PredictionFeatures):
    """
    predictions of car rental prices based on different information.

    return a dict like this : {'predictions' : rental_price_per_day}

    """
    # Read data 
    
    df = pd.DataFrame(dict(predictionFeatures), index=[0])

    # Load model 
    loaded_model = load('model_lr.joblib')
    prediction = loaded_model.predict(df)
    
    # Format response
    response = {"prediction": prediction.tolist()[0]}
    return response


if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000, debug=True, reload=True)