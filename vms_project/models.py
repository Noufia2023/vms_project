import datetime
from sqlalchemy import Column, Integer, String, DateTime, func
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())
    
class Camera(Base):
    __tablename__ = "cameras"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    location = Column(String)
    status = Column(String)
    created_at = Column(DateTime, default=func.now())