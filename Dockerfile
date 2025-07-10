FROM python:3.10-slim

WORKDIR /app

ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main_api:app", "--host", "0.0.0.0", "--port", "8000"]