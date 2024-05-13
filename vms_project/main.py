from fastapi import FastAPI, Depends,status,HTTPException
from models import User as UserModel
from schemas import User as UserSchema, UserCreate
from database import get_db
from sqlalchemy.orm import Session
import service

app= FastAPI()

@app.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = await service.existing_user(db,user.username, user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="username or email already exists"

        )
    await service.create_user(db, user)
    access_token = await service.create_access_token(db_user.id, db_user.username)
    
    return{
        "access_token": access_token,
        "token_type": "bearer",
        "username": db_user.username,
    }


'''
@app.post("/users/")
async def create_user(user: User):
    return user


@app.post("/cameras/")
async def create_camera(camera: Camera):
    return camera
'''
