## Salon Aggregator (Full‑Stack)

### Tech
- **Backend**: FastAPI + SQLAlchemy + SQLite
- **Frontend**: React + TypeScript + Vite

---

## Run backend (FastAPI)

From the repo root:

```bash
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Backend will be at `http://localhost:8000`  
Swagger docs at `http://localhost:8000/docs`

---

## Run frontend (React)

In a second terminal from the repo root:

```bash
cd frontend
npm install
npm run dev
```

Frontend will be at `http://localhost:5173`

---

## Notes
- SQLite DB file: `backend/app.db`
- Default CORS allows the Vite dev server origin.
- On first run, the backend seeds a small set of sample salons/services for browsing.

