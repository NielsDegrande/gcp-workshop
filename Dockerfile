FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

LABEL NAME=server

WORKDIR /app/

COPY setup.py setup.py
COPY README.md README.md
COPY requirements.txt requirements.txt
COPY requirements.txt requirements-dev.txt
COPY model/ model/
RUN pip install .

COPY ./server ./server

ENTRYPOINT [ "server" ]
