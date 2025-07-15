from app.db.models import Base
from app.db.session import engine

print("🛠️ Creating database tables (if not exist)...")
Base.metadata.create_all(bind=engine)
print("✅ Database tables ready.")
