import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.database import Base, engine
from app.routers import auth, users, todos, admin

# -----------------------------
# ✅ Create DB tables
# -----------------------------
Base.metadata.create_all(bind=engine)

# -----------------------------
# ✅ Initialize app
# -----------------------------
app = FastAPI(
    title="Todo List API",
    description="A secure multi-user Todo API with JWT authentication.",
    version="1.0.0",
    redirect_slashes=True  # allow /todos and /todos/
)

# -----------------------------
# ✅ Directories setup
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "..", "templates")
STATIC_DIR = os.path.join(BASE_DIR, "..", "static")

# Ensure folders exist
os.makedirs(TEMPLATE_DIR, exist_ok=True)
os.makedirs(STATIC_DIR, exist_ok=True)

templates = Jinja2Templates(directory=TEMPLATE_DIR)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# -----------------------------
# ✅ Page Routes
# -----------------------------

# Redirect root to login
@app.get("/", response_class=HTMLResponse)
async def root():
    return RedirectResponse(url="/login")

# (Optional) Simple index page if needed
@app.get("/index", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# -----------------------------
# ✅ Routers
# -----------------------------
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(todos.router, tags=["Todos"])  # no prefix needed, router already uses /todos
app.include_router(admin.router, prefix="/admin", tags=["Admin"])

# -----------------------------
# ✅ Custom 404 Page (Optional)
# -----------------------------
@app.exception_handler(404)
async def not_found(request: Request, exc):
    return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
