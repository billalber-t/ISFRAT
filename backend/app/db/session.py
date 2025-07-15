# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from .models import Base

# engine = create_engine("sqlite:///../isfrat.db", connect_args={"check_same_thread": False})
# SessionLocal = sessionmaker(bind=engine)

# def init_db():
#     Base.metadata.create_all(bind=engine)


# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"

# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# MySQL connection URL (SQLAlchemy uses pymysql driver)
SQLALCHEMY_DATABASE_URL = (
    "mysql+pymysql://isfrat_user:isfrat_pw@localhost:3307/isfrat_db"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
