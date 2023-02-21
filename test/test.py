from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)

def test_new_prediction():
    response = client.post('/v1/prediction', json = {
                                                    "listing_type_id": "silver",
                                                    "price": 6700,
                                                    "buying_mode": "buy_it_now",
                                                    "accepts_mercadopago": True,
                                                    "currency_id": "ARS",
                                                    "automatic_relist": False,
                                                    "status": "active",
                                                    "seller_address_longitude": -58.948749,
                                                    "seller_address_latitude": -34.610683,
                                                    "shipping_local_pick_up": True,
                                                    "shipping_free_shipping": False,
                                                    "shipping_mode": "custom",
                                                    "Month_created": "September",
                                                    "day_name_created": "Tuesday",
                                                    "Hour_created": 21,
                                                    "Min_created": 17,
                                                    "Month_updated": "September",
                                                    "day_name_updated": "Tuesday",
                                                    "Hour_updated": 21,
                                                    "Min_updated": 17,
                                                    "row_size": 500,
                                                    "col_size": 375,
                                                    "row_max_size": 1200,
                                                    "col_max_size": 900
                                                })
    assert response.status_code == 200
    assert response.json()['condition'] == 1 

def test_used_prediction():
    response = client.post('/v1/prediction', json = {
                                                    "listing_type_id": "bronze",
                                                    "price": 100.0,
                                                    "buying_mode": "buy_it_now",
                                                    "accepts_mercadopago": True,
                                                    "currency_id": "ARS",
                                                    "automatic_relist": False,
                                                    "status": "active",
                                                    "seller_address_longitude": -58.439073,
                                                    "seller_address_latitude": -34.611235,
                                                    "shipping_local_pick_up": True,
                                                    "shipping_free_shipping": False,
                                                    "shipping_mode": "me2",
                                                    "Month_created": "October",
                                                    "day_name_created": "Wednesday",
                                                    "Hour_created": 12,
                                                    "Min_created": 54,
                                                    "Month_updated": "October",
                                                    "day_name_updated": "Wednesday",
                                                    "Hour_updated": 12,
                                                    "Min_updated": 54,
                                                    "row_size": 283,
                                                    "col_size": 500,
                                                    "row_max_size": 680,
                                                    "col_max_size": 1200
                                                })
    assert response.status_code == 200
    assert response.json()['condition'] == 0




