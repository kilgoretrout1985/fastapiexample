# Fastapi example project

1) 
    ```
    python3 -m venv .env && \
    source .env/bin/activate && \
    pip install -U pip && \
    pip install -e .
    ```

2)  Configure Postgres connect dsn by editing `config.py`.

    If you want github to run and pass tests on your push to repositary please also supply correct postgres login, password, test db name and port into `.github/workflows/tests.yaml` file.

3)  For development you should also run:
    ```
    pip install -e .[testing] && tox
    ```
    Everything should be green at this point.

4) 
    ```
    cd src/fastapiexample && python main.py && uvicorn main:app --reload
    ```

    `python main.py` is used to create initial db tables before first run. 
    
    Use `python main.py --drop-all` to drop (delete all!) and recreate db in case you need it.

5)  Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for interactive docs.
