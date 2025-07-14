from fastapi import APIRouter, UploadFile, Form
from pathlib import Path
from app.services import test_case_generation, anomaly_detection, security_analysis

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "ISFRAT backend is running."}


# @router.post("/upload-spec")
# async def upload_spec(file: UploadFile):
#     contents = await file.read()
#     # resolve path relative to project root
#     project_root = Path(__file__).resolve().parent.parent.parent
#     spec_dir = project_root / "test_case_generator" / "specs"
#     spec_dir.mkdir(parents=True, exist_ok=True)
#     with open(spec_dir / "api_spec.yaml", "wb") as f:
#         f.write(contents)
#     return {"message": "API specification uploaded successfully."}

# @router.post("/upload-spec")
# async def upload_spec(file: UploadFile):
#     contents = await file.read()
#     # Always resolve to ISFRAT/test_case_generator/specs
#     backend_dir = Path(__file__).resolve().parent.parent  # ISFRAT/backend
#     project_root = backend_dir.parent                     # ISFRAT/

#     return project_root
#     spec_dir = project_root / "test_case_generator" / "specs"
#     spec_dir.mkdir(parents=True, exist_ok=True)
#     with open(spec_dir / "api_spec.yaml", "wb") as f:
#         f.write(contents)
#     return {"message": f"API specification saved to {spec_dir}/api_spec.yaml"}


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
    results = {}
    if tcg:
        results["test_case_generation"] = test_case_generation.run()
    if adm:
        results["anomaly_detection"] = anomaly_detection.run()
    if sam:
        results["security_analysis"] = security_analysis.run()
    return results
