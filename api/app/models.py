from pydantic import BaseModel, Field

class PredictionRequest(BaseModel):
    listing_type_id: str = Field(min_length=3, max_length=12)
    price: float = Field(ge=1)
    buying_mode: str = Field(min_length=3, max_length=15)
    accepts_mercadopago: bool
    currency_id: str = Field(min_length=2, max_length=6)
    automatic_relist: bool
    status: str = Field(min_length=4, max_length=9)
    seller_address_longitude: float = Field(ge=-100, le=100)
    seller_address_latitude: float = Field(ge=-100, le=100)
    shipping_local_pick_up: bool 
    shipping_free_shipping: bool
    shipping_mode: str = Field(min_length=3, max_length=16)
    Month_created: str = Field(min_length=3, max_length=10)
    day_name_created: str = Field(min_length=5, max_length=9)
    Hour_created: int = Field(ge=0, le=23)
    Min_created: int = Field(ge=0, le=59)
    Month_updated: str = Field(min_length=3, max_length=16)
    day_name_updated: str = Field(min_length=5, max_length=9)
    Hour_updated: int = Field(ge=0, le=23)
    Min_updated: int = Field(ge=0, le=59)
    row_size: int = Field(ge=2)
    col_size: int = Field(ge=2)
    row_max_size: int = Field(ge=2)
    col_max_size: int = Field(ge=2)

    class Config:
        schema_extra = {
            "example": {
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
            }
        }

class PredictionResponse(BaseModel):
    condition: int