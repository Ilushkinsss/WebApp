from fastapi import APIRouter, HTTPException
from models import User
from pydantic import ValidationError
from database.db import add_user

router = APIRouter()

@router.post("/register")
async def register(user: User):
    try:
        await add_user(user.telegram_id, user.city, user.gender, user.age)
        return {"success": "true"}
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
