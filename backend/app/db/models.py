# from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
# from sqlalchemy.orm import relationship, declarative_base
# from datetime import datetime

# Base = declarative_base()

# class TestRun(Base):
#     __tablename__ = "test_runs"

#     id = Column(Integer, primary_key=True)
#     timestamp = Column(DateTime, default=datetime.utcnow)
#     spec_filename = Column(String)

#     test_cases = relationship("TestCase", back_populates="test_run", cascade="all, delete-orphan")
#     test_results = relationship("TestResult", back_populates="test_run", cascade="all, delete-orphan")


# class TestCase(Base):
#     __tablename__ = "test_cases"

#     id = Column(Integer, primary_key=True)
#     test_run_id = Column(Integer, ForeignKey("test_runs.id"), nullable=False)
#     endpoint = Column(String)
#     method = Column(String)
#     type = Column(String)
#     payload = Column(String)
#     created_at = Column(DateTime, default=datetime.utcnow)

#     test_run = relationship("TestRun", back_populates="test_cases")


# class TestResult(Base):
#     __tablename__ = "test_results"

#     id = Column(Integer, primary_key=True)
#     test_run_id = Column(Integer, ForeignKey("test_runs.id"), nullable=False)
#     engine = Column(String, nullable=False)  # e.g., "test_case_generation"
#     result = Column(String)  # could store JSON string or summary
#     created_at = Column(DateTime, default=datetime.utcnow)

#     test_run = relationship("TestRun", back_populates="test_results")


from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()


class TestRun(Base):
    __tablename__ = "test_runs"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    spec_filename = Column(String(255))  # specify a length here

    test_cases = relationship("TestCase", back_populates="test_run", cascade="all, delete-orphan")
    test_results = relationship("TestResult", back_populates="test_run", cascade="all, delete-orphan")


class TestCase(Base):
    __tablename__ = "test_cases"

    id = Column(Integer, primary_key=True)
    test_run_id = Column(Integer, ForeignKey("test_runs.id"))
    endpoint = Column(String(255))
    method = Column(String(10))
    type = Column(String(50))
    payload = Column(String(1000))
    created_at = Column(DateTime, default=datetime.utcnow)

    test_run = relationship("TestRun", back_populates="test_cases")


class TestResult(Base):
    __tablename__ = "test_results"

    id = Column(Integer, primary_key=True)
    test_run_id = Column(Integer, ForeignKey("test_runs.id"), nullable=False)
    engine = Column(String(100), nullable=False)  # e.g., "test_case_generation"
    result = Column(String(2000))  # or Text() if large
    created_at = Column(DateTime, default=datetime.utcnow)

    test_run = relationship("TestRun", back_populates="test_results")
