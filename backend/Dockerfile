FROM python:3.12-slim

WORKDIR /app

# Install dependencies first (Docker layer caching — this layer only rebuilds
# when requirements.txt changes, not when your code changes)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# uvicorn serves the FastAPI app
# --host 0.0.0.0 makes it accessible from outside the container
# --reload watches for file changes (dev only — we'll disable this in production)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
