# Fastapi example project

1) 
```
python3 -m venv .env && \
source .env/bin/activate && \
pip install -U pip && \
pip install -e .
```

2) For development you should also run:
```
pip install -e .[testing] && tox
```

3) 
```
cd src/fastapiexample && uvicorn main:app --reload
```

4) Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for interactive docs.
