from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import pickle
import json


pickled_model = pickle.load(open('MLPRegressor_trained_model2.obj', 'rb'))

class Item(BaseModel):
    area: float
    num_rooms: int
    floor: int
    year_built: int
    market: int
    finishing_state: int
    building_type: int
    district: int

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Zazwól na dostęp z dowolnej domeny (* oznacza wszystkie)
    allow_credentials=True,
    allow_methods=["*"],  # Zazwól na wszystkie metody HTTP
    allow_headers=["*"],  # Zazwól na wszystkie nagłówki HTTP
)

@app.post("/items/")
async def create_item(item: Item):
    data_to_predict = [
        [
            item.area,
            item.num_rooms,
            item.floor,
            item.year_built,
            item.market,
            item.finishing_state,
            item.building_type,
            item.district
        ]
    ]
    predict = pickled_model.predict(data_to_predict)

    predict_return = {
        'price' : predict[0]
        }

    return predict_return
