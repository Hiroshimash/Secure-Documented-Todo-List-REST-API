from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# Users
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate, role: str = "user"):
    hashed = get_password_hash(user.password)
    db_user = models.User(name=user.name, email=user.email, hashed_password=hashed, phone_number=user.phone_number, role=role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def list_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def delete_user(db: Session, user: models.User):
    db.delete(user)
    db.commit()

# Todos
def create_todo(db: Session, owner: models.User, todo: schemas.TodoCreate):
    db_todo = models.Todo(title=todo.title, description=todo.description, owner=owner)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def get_todo(db: Session, todo_id: int):
    return db.query(models.Todo).filter(models.Todo.id == todo_id).first()

def list_todos_for_user(db: Session, owner_id: int):
    return db.query(models.Todo).filter(models.Todo.owner_id == owner_id).all()

def list_all_todos(db: Session):
    return db.query(models.Todo).all()

def update_todo(db: Session, todo: models.Todo, **kwargs):
    for key, value in kwargs.items():
        setattr(todo, key, value)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo

def delete_todo(db: Session, todo: models.Todo):
    db.delete(todo)
    db.commit()
