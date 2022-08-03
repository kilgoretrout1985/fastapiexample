# Fastapi example project

1) 
```
python3 -m venv .env && \
source .env/bin/activate && \
pip install -U pip && \
pip install -e .
```

2) * For development you can also run:
```
pip install -e .[testing] && \
tox
```

3) 
```
cd src/fastapiexample && \
uvicorn main:app --reload
```
