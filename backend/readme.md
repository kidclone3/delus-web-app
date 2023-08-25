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

# Simulator microservice

1. Setup python path:

```bash
    export PYTHONPATH=$PWD:$PWD/simulation:$PWD/simulation/zeromq
```

2. Run all services, require xterm installed

```bash
    bash run_script.sh
```

4. Final run simulator

```bash
    python simulation/simulation_customer_destination.py
```

Note update: Maybe use docker in the future.