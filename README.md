Diet and Fitness Planner (NutriSense)

Project Title and Brief Description

Diet and Fitness Planner (NutriSense) is a two-part application (backend + frontend) that provides personalized diet and fitness recommendations using rule-based services and trained ML models for meal adherence and goal achievement.

The repository contains:
- `DietAndFitnessPlanner-BE/` — FastAPI backend, ML models, data and utilities
- `DietAndFitnessPlanner-FE/` — React + TypeScript frontend (Vite)

Technology Stack and Tools Used

- Backend: Python, FastAPI
- ML: scikit-learn / joblib (pretrained models in `DietAndFitnessPlanner-BE/models/`)
- Database: MongoDB (connections in `DietAndFitnessPlanner-BE/app/db/`)
- Frontend: React, TypeScript, Vite, MUI
- Packaging & Scripts: `npm` (frontend), Python `venv` and `pip` (backend)

Features and Functionalities Implemented

- User details intake and plan generation
- Exercise and diet recommendation services
- ML models for meal adherence and goal achievement (pretrained `.joblib` files in backend `models/`)
- REST API implemented with FastAPI
- Frontend UI with React + TypeScript and MUI components

Installation / Execution Steps

Notes: these commands assume Windows PowerShell and that you are executing them from the workspace root (`Mini Project`). Adjust paths or activate shells as needed for other OSes.

1) Backend (FastAPI)

```
cd "DietAndFitnessPlanner-BE"
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
# If uvicorn isn't in requirements, install it:
pip install "uvicorn[standard]"
# Run the server (from BE folder):
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

API will be available at `http://127.0.0.1:8000` and OpenAPI docs at `http://127.0.0.1:8000/docs`.

2) Frontend (Vite + React)

```
cd "DietAndFitnessPlanner-FE"
npm install
npm run dev
```

The frontend dev server opens in your browser (default host 127.0.0.1). If the frontend needs the backend, ensure the backend is running first.

Project Files & Where To Look

- Backend main: `DietAndFitnessPlanner-BE/app/main.py`
- Backend API routes: `DietAndFitnessPlanner-BE/app/api/apiRouter.py`
- ML models: `DietAndFitnessPlanner-BE/models/` (contains `.joblib` and metrics JSON)
- Frontend entry: `DietAndFitnessPlanner-FE/src/main.tsx`
- Frontend pages/components: `DietAndFitnessPlanner-FE/src/pages/`, `DietAndFitnessPlanner-FE/src/components/`

Project Report and Screenshots

Placeholder report and screenshots are included in `project_report/` and `screenshots/`. Replace the placeholder files with the final report (PDF/DOCX) and image screenshots before submission.

Notes and Next Steps

- If the backend fails to start, check Python version (recommended 3.10+) and that `requirements.txt` is installed into the activated venv.
- If the frontend dev server fails, ensure Node.js and npm are installed (Node 18+ recommended) and run `npm install` inside `DietAndFitnessPlanner-FE`.
- To run or retrain the ML models, see `DietAndFitnessPlanner-BE/tools/` for training scripts and `DietAndFitnessPlanner-BE/data/training/` for datasets.

---
Generated placeholders:
- `project_report/REPORT.md` — replace with final report
- `screenshots/placeholder.txt` — replace with screenshot image files
