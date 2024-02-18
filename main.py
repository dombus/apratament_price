from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import pickle
import json


pickled_model = pickle.load(open('MLPRegressor_trained_model.obj', 'rb'))

class Item(BaseModel):
    seller_price: int
    area: float
    num_rooms: int
    floor: int
    year_built: int
    market: int
    finishing_state: int
    building_type: int
    district: int
    seller_price: int

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Zazwól na dostęp z dowolnej domeny (* oznacza wszystkie)
    allow_credentials=True,
    allow_methods=["*"],  # Zazwól na wszystkie metody HTTP
    allow_headers=["*"],  # Zazwól na wszystkie nagłówki HTTP
)

@app.post("/api/price")
#async
def create_item(item: Item):
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


    comment = None
    if item.seller_price > int(predict[0]):
        comment = 'Nie opłaca się kupić.'

    else:
        comment = 'Opłaca się kupić.'

    predict_return = {
        'seller_price' : item.seller_price,
        'predicted_price' : int(predict[0]),
        'comment' : comment
     }

    return predict_return
