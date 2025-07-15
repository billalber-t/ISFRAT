from fastapi import APIRouter, UploadFile, Form, Query
from pathlib import Path
from datetime import datetime

from app.services import test_case_generation, anomaly_detection, security_analysis
from app.db.session import SessionLocal
from app.db.models import TestRun, TestResult, TestCase

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "ISFRAT backend is running."}


@router.post("/upload-spec")
async def upload_spec(file: UploadFile):
    contents = await file.read()

    # resolve ISFRAT project root properly
    isfrat_root = Path(__file__).resolve().parent.parent.parent.parent

    spec_dir = isfrat_root / "test_case_generator" / "specs"
    spec_dir.mkdir(parents=True, exist_ok=True)

    with open(spec_dir / "api_spec.yaml", "wb") as f:
        f.write(contents)

    return {"message": f"API specification saved to {spec_dir}/api_spec.yaml"}


@router.post("/run-tests")
async def run_tests(
    tcg: bool = Form(...), adm: bool = Form(...), sam: bool = Form(...)
):
    session = SessionLocal()
    run = TestRun(
        timestamp=datetime.utcnow(),
        spec_filename="api_spec.yaml"
    )
    session.add(run)
    session.commit()

    run_id = run.id  # ✅ capture here before session.close()

    results = {}

    if tcg:
        results["test_case_generation"] = test_case_generation.run(test_run_id=run_id)
        session.add(TestResult(
            test_run_id=run_id,
            engine="test_case_generation",
            result="COMPLETED"
        ))

    if adm:
        results["anomaly_detection"] = anomaly_detection.run()
        session.add(TestResult(
            test_run_id=run_id,
            engine="anomaly_detection",
            result="COMPLETED"
        ))

    if sam:
        results["security_analysis"] = security_analysis.run()
        session.add(TestResult(
            test_run_id=run_id,
            engine="security_analysis",
            result="COMPLETED"
        ))

    session.commit()
    session.close()

    return {"run_id": run_id, "results": results}



@router.get("/history")
async def history():
    session = SessionLocal()
    runs = session.query(TestRun).order_by(TestRun.timestamp.desc()).all()
    session.close()
    return [
        {
            "run_id": run.id,
            "timestamp": run.timestamp,
            "spec_filename": run.spec_filename
        } for run in runs
    ]

@router.get("/results/{run_id}")
async def get_results(run_id: int):
    session = SessionLocal()
    results = session.query(TestResult).filter(TestResult.test_run_id == run_id).all()
    session.close()
    return {
        "run_id": run_id,
        "results": [
            {
                "engine": res.engine,
                "result": res.result,
                "created_at": res.created_at.strftime("%Y-%m-%d %H:%M:%S")
            }
            for res in results
        ]
    }


@router.get("/test-cases/{run_id}")
async def get_test_cases_grouped_by_engine(run_id: int):
    session = SessionLocal()

    # Check if the run exists
    run = session.query(TestRun).filter_by(id=run_id).first()
    if not run:
        session.close()
        raise HTTPException(status_code=404, detail=f"TestRun with id {run_id} not found")

    # Get all test results for the run
    results = session.query(TestResult).filter_by(test_run_id=run_id).all()
    if not results:
        session.close()
        raise HTTPException(status_code=404, detail=f"No test results found for run_id {run_id}")

    # Prepare mapping engine -> list of test_cases
    data = {}

    for result in results:
        engine = result.engine
        test_cases = (
            session.query(TestCase)
            .filter_by(test_run_id=run_id)
            .all()
        )
        # Since test_cases table does not have engine info, associate all to each engine
        # (you might want to add engine info to test_cases table in the future)
        data[engine] = [
            {
                "endpoint": tc.endpoint,
                "method": tc.method,
                "type": tc.type,
                "payload": tc.payload,
                "created_at": tc.created_at,
            }
            for tc in test_cases
        ]

    session.close()
    return {"run_id": run_id, "test_cases_by_engine": data}
