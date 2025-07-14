from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class TestRun(Base):
    __tablename__ = "test_runs"

    id = Column(Integer, primary_key=True)
    test_run_id = Column(Integer, ForeignKey("test_runs.id"))
    endpoint = Column(String)
    method = Column(String)
    type = Column(String)  # valid / invalid
    payload = Column(String)  # store JSON string
    created_at = Column(DateTime, default=datetime.utcnow)

    test_run = relationship("TestRun", back_populates="test_cases")

class TestResult(Base):
    __tablename__ = "test_results"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    spec_filename = Column(String)

    results = relationship("TestResult", back_populates="test_run")
    test_cases = relationship("TestCase", back_populates="test_run")
