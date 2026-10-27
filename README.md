# Lab 8 — Thai School Directory

Contents:

- `school_directory.db`: complete SQLite DB (77 provinces, 930 districts, 7,452 subdistricts, 28,840 schools).
- `backend/main.py`: working, read-only FastAPI endpoints.
- `backend/requirements.txt`: Python dependencies.
- `source_data/`: CSV + JSON originals for rerunning import.

## WSL Ubuntu setup

```bash
sudo apt update
sudo apt install -y sqlite3 python3-venv python3-pip
cd backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
uvicorn main:app --reload
```

From `backend`, the API finds `../school_directory.db` automatically. Open http://127.0.0.1:8000/docs. Frontend Vite runs on http://localhost:5173.

## Rebuild database (optional)

From the package root:

```bash
python3 import_schools.py --data-dir source_data --output school_directory.db
sqlite3 school_directory.db 'SELECT COUNT(*) FROM schools;'
```

## Endpoint contract

- `GET /provinces` => array of ID and names
- `GET /districts?province_id=1` => array
- `GET /subdistricts?district_id=1001` => array
- `GET /schools?keyword=วิทยา&province_id=1&district_id=1001&subdistrict_id=100107&limit=20&offset=0` => **object** `{items, total, limit, offset}`
- `GET /schools/1` => school record, HTTP 404 if missing

**Important Lab 7 difference:** this API uses `keyword` (not `search`), and `/schools` returns `{items, total, limit, offset}` (not a plain array).
You should adapt the Vue state accordingly.

The school `id` is the row sequence starting at 1, not its SMIS code.
