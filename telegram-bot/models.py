from pydantic import BaseModel

class User(BaseModel):
    telegram_id: str
    city: str
    gender: str
    age: int
