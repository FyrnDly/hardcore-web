FROM python:3.11-bullseye

WORKDIR /app
COPY requirements.txt /app

RUN pip install -r /app/requirements.txt
COPY . /app

CMD python app.py