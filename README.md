# Fastapi example project

1) 
```
python3 -m venv .env && \
source .env/bin/activate && \
pip install -U pip && \
pip install -r requirements.txt
```

2) * For development you can also run:
```
pip install -r requirements_dev.txt && \
tox
```

3) 
```
cd src/fastapiexample && \
uvicorn main:app --reload
```
