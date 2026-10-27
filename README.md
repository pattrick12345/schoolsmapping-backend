# Thai Schools API

A REST API built with **FastAPI** and **SQLite** for retrieving school information in Thailand. This backend powers the Thai Schools Mapping frontend.

## Features

- Retrieve a list of schools.
- Search and paginate school records.
- Retrieve detailed information about a specific school.
- Retrieve school location coordinates.
- Retrieve province information.
- Store school records in an SQLite database.

## Tech Stack

- Python
- FastAPI
- Uvicorn
- SQLite
- Git and GitHub


## Getting Started

### 1. Clone the repository

```bash
git clone YOUR_BACKEND_REPOSITORY_URL
cd schoolbackend
```

Replace `YOUR_BACKEND_REPOSITORY_URL` with the URL of this repository.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r backend/requirements.txt
```

### 4. Run the API

```bash
cd backend
uvicorn main:app --reload
```

The API will be available at:

- API: http://127.0.0.1:8000
- Interactive API documentation: http://127.0.0.1:8000/docs

## Database

The API uses SQLite to store school information in `school_directory.db`.

By default, the database file is expected to be in the same directory as `main.py`. You can override its location using the `SCHOOLS_DB` environment variable.

## Frontend

This API is designed to work with the Thai Schools Mapping frontend. Configure the frontend to use the URL of the running backend.
