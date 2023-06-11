FROM python:3.9

WORKDIR /app
COPY . /app

RUN pip install -e .

CMD ["python", "main.py"]
