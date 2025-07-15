from app.db.models import Base
from app.db.session import engine

print("🛠️ Creating all tables in the database...")
Base.metadata.create_all(bind=engine)
print("✅ Done.")
