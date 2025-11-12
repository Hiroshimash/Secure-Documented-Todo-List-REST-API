# scripts/seed_admin.py
from app.database import SessionLocal
from app.models import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

db = SessionLocal()

admin = User(
    name="Admin",
    email="admin@example.com",
    hashed_password=pwd_context.hash("admin123"),
    phone_number="1234567890",
    role="admin"
)

db.add(admin)
db.commit()
db.close()

print("✅ Admin created: admin@example.com / admin123")
