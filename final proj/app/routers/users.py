from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas, database
from app.core.security import get_current_user

router = APIRouter()

@router.get("/me")
def read_me(current_user: models.User = Depends(get_current_user)):
    return current_user


@router.put("/me")
def update_me(
    update: schemas.UserBase,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    current_user.name = update.name
    current_user.phone_number = update.phone_number
    db.commit()
    db.refresh(current_user)
    return current_user


@router.post("/me/change-password")
def change_password(
    current_password: str,
    new_password: str,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    if not pwd_context.verify(current_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect current password")

    current_user.hashed_password = pwd_context.hash(new_password)
    db.commit()
    return {"message": "Password updated successfully"}
