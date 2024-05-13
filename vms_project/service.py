from fastapi import Depends
from sqlalchemy.orm import Session
from models import User as UserModel
from schemas import User as UserSchema, UserCreate
from datetime import timedelta,datetime,timezone
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext


SECRET_KEY = "mysecretkey"
EXPIRE_MINUTES = 60 * 24
ALGORITHM = "HS256"

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token") #running as /token on localhost8000
bcrypt_context = CryptContext(schemes=["bcrypt"])


# check existing user with same username or email
async def existing_user(db: Session, username: str, email: str):
    db_user = db.query(UserModel).filter(UserModel.username == username).first()
    if db_user:
        return db_user
    db_user = db.query(UserModel).filter(UserModel.email == email).first()
    if db_user:
        return db_user
    return None

# create token, JWT{encoded data, secret key, algorithm}
async def create_access_token(id: int, username: str):
    encode = {"sub":username, "id": id}
    expires = datetime.now(timezone.utc) + timedelta(minutes=EXPIRE_MINUTES)
    encode.update({"exp":expires})
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)

# get current user from token
async def get_current_user(db: Session, token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        id: int = payload.get("id")
        expires: datetime = payload.get("exp")
        if username is None or id is None:
            return None
        db_user = db.query(UserModel).filter(UserModel.id ==id).first()
        return db_user
    except JWTError :
        return None


# create user
async def create_user(db: Session, user: UserCreate):
    db_user = UserModel(
        username = user.username,
        email = user.email,
        hashed_password = bcrypt_context.hash(user.password),

    )
    db.add(db_user)
    db.commit()
    return db_user

