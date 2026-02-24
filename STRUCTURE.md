Recommended project structure

exam-results-main/
- apn/
  - app.py
  - __init__.py
  - models/               # place ML models here (optional)
  - static/
    - css/
    - js/
    - images/
  - templates/
- best_random_forest_model.pkl
- requirements.txt
- run.py                 # simple entrypoint to start the app
- tests/                 # unit / integration tests
- instance/              # instance-specific config (not tracked)
- scripts/               # helper scripts (deploy, manage)
- docs/                  # project documentation

Notes:
- `run.py` imports `apn.app` so you can run the app with `python run.py`.
- Keep large binary model files in `apn/models` or at project root; update `apn/app.py` path accordingly.
