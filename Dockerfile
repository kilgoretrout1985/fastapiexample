# This config uses external postgres to connect to.
# If you are using postgres on local dev-machine, do not forget to
# setup it to accept incoming connections not only from localhost,
# but from private network addresses.
# 
# 1) Find `postgresql.conf` and change to `listen_addresses = '*'`
# 
# 2) Append this to `pg_hba.conf`:
# host    all             all             10.0.0.0/8              md5
# host    all             all             172.16.0.0/12           md5
# host    all             all             192.168.0.0/16          md5


FROM python:3.10

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./src/fastapiexample /app/fastapiexample

# For standart Docker for Linux, IP-address of the host will always be 172.17.0.1 
# The easiest way to get it is `ifconfig docker0`.
ENV DB_DSN postgresql+asyncpg://fastapiexamplepguser:pass@172.17.0.1/fastapiexample

CMD ["sh", "-c", "uvicorn fastapiexample.main:app --host 0.0.0.0 --port 80"]


# docker build -t fastapiexampleimage .
# docker run -d -p 80:80 fastapiexampleimage