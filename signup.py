from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse
from database import users_collection

router = APIRouter()

@router.post("/signup")
async def signup(name: str = Form(...), email: str = Form(...), password: str = Form(...)):
    if users_collection.find_one({"email": email}):
        return JSONResponse(content={"error": "User already exists"}, status_code=400)

    users_collection.insert_one({
        "name": name,
        "email": email,
        "password": password
    })

    return JSONResponse(content={"message": "User created successfully"}, status_code=201)
