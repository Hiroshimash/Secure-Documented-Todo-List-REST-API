from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from app import models
from app.database import get_db

router = APIRouter(prefix="/todos")
templates = Jinja2Templates(directory="templates")

SECRET_KEY = "mysecret"
ALGORITHM = "HS256"


# ------------------------------
# 🔹 Helper: Get user from JWT
# ------------------------------
def get_user_from_cookie(request: Request, db: Session):
    token = request.cookies.get("access_token")
    if not token:
        return None
    try:
        payload = jwt.decode(token.replace("Bearer ", ""), SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
        return db.query(models.User).filter(models.User.id == user_id).first()
    except JWTError:
        return None


# ------------------------------
# 🔹 Web Routes (HTML)
# ------------------------------
@router.get("/", response_class=HTMLResponse)
async def todos_page(request: Request, db: Session = Depends(get_db)):
    user = get_user_from_cookie(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=302)

    todos = db.query(models.Todo).filter(models.Todo.owner_id == user.id).all()
    return templates.TemplateResponse(
        "todos.html",
        {"request": request, "todos": todos, "user": user}
    )


@router.post("/add", response_class=RedirectResponse)
async def add_todo(
    request: Request,
    title: str = Form(...),
    description: str = Form(""),
    db: Session = Depends(get_db)
):
    user = get_user_from_cookie(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=302)

    new_todo = models.Todo(title=title, description=description, owner_id=user.id)
    db.add(new_todo)
    db.commit()
    return RedirectResponse(url="/todos", status_code=302)


@router.post("/update/{todo_id}", response_class=RedirectResponse)
async def update_todo(
    request: Request,
    todo_id: int,
    title: str = Form(...),
    description: str = Form(""),
    db: Session = Depends(get_db)
):
    user = get_user_from_cookie(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=302)

    todo = db.query(models.Todo).filter(models.Todo.id == todo_id, models.Todo.owner_id == user.id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo.title = title
    todo.description = description
    db.commit()
    return RedirectResponse(url="/todos", status_code=302)


@router.get("/delete/{todo_id}", response_class=RedirectResponse)
async def delete_todo(request: Request, todo_id: int, db: Session = Depends(get_db)):
    user = get_user_from_cookie(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=302)

    todo = db.query(models.Todo).filter(models.Todo.id == todo_id, models.Todo.owner_id == user.id).first()
    if todo:
        db.delete(todo)
        db.commit()

    return RedirectResponse(url="/todos", status_code=302)
