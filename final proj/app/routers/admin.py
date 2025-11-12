# app/routers/admin.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, deps
from app.core.security import get_current_user


router = APIRouter()

@router.get("/todos", response_model=list[schemas.TodoOut])
def get_all_todos(db: Session = Depends(deps.get_db), admin: models.User = Depends(deps.get_current_admin)):
    return db.query(models.Todo).all()

@router.delete("/todos/{todo_id}")
def delete_any_todo(todo_id: int, db: Session = Depends(deps.get_db), admin: models.User = Depends(deps.get_current_admin)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted by admin"}

@router.get("/users", response_model=list[schemas.UserOut])
def get_all_users(db: Session = Depends(deps.get_db), admin: models.User = Depends(deps.get_current_admin)):
    return db.query(models.User).all()

@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(deps.get_db), admin: models.User = Depends(deps.get_current_admin)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted by admin"}
