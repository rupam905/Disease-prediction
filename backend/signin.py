from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse
from database import users_collection

router = APIRouter()

@router.post("/login")
async def login(email: str = Form(...), password: str = Form(...)):
    user = users_collection.find_one({"email": email, "password": password})
    if user:
        return JSONResponse(content={"message": "Login successful"}, status_code=200)
    return JSONResponse(content={"error": "Invalid credentials"}, status_code=401)
