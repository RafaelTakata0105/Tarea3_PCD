import os
from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field, EmailStr
from sqlalchemy.orm import Session
from dotenv import load_dotenv

import models
from database import engine, SessionLocal

# ----- Cargar variables de entorno (.env) -----
load_dotenv()
API_KEY = os.getenv("API_KEY")

# ----- Iniciar app -----
app = FastAPI(title="Users API", version="1.0.0")

# ----- Crear tablas -----
models.Base.metadata.create_all(bind=engine)

# ----- Dependencia DB -----
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# ----- Seguridad por header -----
api_key_header = APIKeyHeader(name="X-API-Key", description="API key by header", auto_error=True)

async def get_api_key(api_key: str = Security(api_key_header)) -> str:
    if API_KEY and api_key == API_KEY:
        return api_key
    raise HTTPException(status_code=403, detail="Could not validate credentials")

# ----- Esquema Pydantic -----
class User(BaseModel):
    user_name: str = Field(..., min_length=1)
    user_email: EmailStr
    age: int | None = Field(default=None, gt=18, lt=101)  
    recommendations: list[str] = Field(default_factory=list)  
    zip: str | None = Field(default=None, min_length=1, max_length=6) 

 


# ----- Endpoints -----
@app.get("/")
def root():
    return {"message": "Users API up. See /docs"}

@app.get("/api/v1/users/", tags=["users"])
def list_users(db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    return db.query(models.User).all()

@app.post("/api/v1/users/", tags=["users"])
def create_book(user: User, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    existing_user = db.query(models.User).filter(models.User.user_email == user.user_email).first()
    if existing_user:
        raise HTTPException(status_code=409,
                            detail=f"El correo {user.user_email} ya está registrado" )
    
    user_model = models.User(
        user_name = user.user_name,
        user_email = user.user_email,
        age = user.age,
        recommendations = user.recommendations,
        zip = user.zip
    )
    db.add(user_model)
    db.commit()
    db.refresh(user_model)
    return user_model

@app.put("/api/v1/users/{user_id}", tags=["users"])
def update_user(user_id: int, user: User, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    user_model = db.query(models.User).filter(models.User.user_id == user_id).first()

    if user_model is None:
        raise HTTPException(status_code=404, detail=f"ID {user_id} : Does not exist")
    
    existing_user = db.query(models.User).filter(models.User.user_email == user.user_email).first()
    if existing_user:
        raise HTTPException(status_code=409,
                            detail=f"El correo {user.user_email} ya está registrado" )
    
    user_model.user_name = user.user_name
    user_model.user_email = user.user_email
    user_model.age = user.age
    user_model.recommendations = user.recommendations
    user_model.zip = user.zip

    db.add(user_model)
    db.commit()
    db.refresh(user_model)
    return user_model

@app.delete("/api/v1/users/{user_id}", tags=["users"])
def delete_user(user_id: int, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    user_model = db.query(models.User).filter(models.User.user_id == user_id).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail=f"ID {user_id} : Does not exist")

    db.query(models.User).filter(models.User.user_id == user_id).delete()
    db.commit()
    return {"deleted_id": user_id}