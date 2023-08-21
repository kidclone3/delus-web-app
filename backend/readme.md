# FastAPI for backend

Run:

1. Environment variables:
Windows:
```bash
    set PYTHONPATH=%cd%
```
Linux:
```bash
    export PYTHONPATH=$PWD
```

2. Setup virtual environment:
Windows:
```bash
    python -m venv venv
    venv\Scripts\activate.bat
    pip install -r requirements.txt
```
Linux:
```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
```
3. Run:
```
    uvicorn src.main:app --reload
```

Note update: Maybe use docker in the future.