from pydantic import BaseModel, Field

class PredictionRequest(BaseModel):
    DIA: int = Field(default=1, ge=1, le=31)
    MES: int = Field(default=1, ge=1, le=12)
    HORA: int = Field(default=0, ge=0, le=23)
    MIN: int = Field(default=15, ge=0, le=59)
    SEG: int = Field(default=15, ge=0, le=59)
    DIANOM: str = Field(min_length=5, max_length=9)
    MESNOM: str = Field(min_length=3)

    class Config:
        schema_extra = {
            "example": {
                "DIA": 1,
                "MES": 1,
                "HORA": 0,
                "MIN": 15,
                "SEG": 15,
                "DIANOM": "Domingo",
                "MESNOM": "Ene"
            }
        }

class PredictionResponse(BaseModel):
    your_y_variable: int