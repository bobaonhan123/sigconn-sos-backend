from pydantic import BaseModel

class SignalRequest(BaseModel):
    latitude: float
    longitude: float
    message: str
    user_id: str
