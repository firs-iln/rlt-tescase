FROM python:3.11

WORKDIR /src

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY src/. .

RUN chmod +x main.py