from sqlalchemy import Column, Integer, String, JSON
from database import Base

class User(Base):
    __tablename__ = "Users"
  
    user_id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, nullable=False)
    user_email = Column(String, unique=True, nullable=False)
    age = Column(Integer, nullable=True)
    recommendations = Column(JSON, nullable=False)   
    zip = Column(String, nullable=True)