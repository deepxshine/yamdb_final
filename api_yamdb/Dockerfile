FROM python:3.7-slim

WORKDIR /app

RUN apt update && apt -y install libpq-dev


COPY requirements.txt .

RUN pip3 install -r /app/requirements.txt --no-cache-dir

COPY . .


CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000" ]