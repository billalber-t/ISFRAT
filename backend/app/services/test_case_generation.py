# def run():
#     from test_case_generator.src.main import main
#     main()
#     return "Test case generation completed."


import sys
from pathlib import Path

# Add ISFRAT root to sys.path
ISFRAT_ROOT = Path(__file__).resolve().parents[3]  # go up: services → app → backend → ISFRAT
if str(ISFRAT_ROOT) not in sys.path:
    sys.path.insert(0, str(ISFRAT_ROOT))


def run():
    from test_case_generator.src.main import main
    main()
    return "Test case generation completed."
