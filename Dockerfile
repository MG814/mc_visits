FROM python:3.12
WORKDIR /app
COPY src/requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app