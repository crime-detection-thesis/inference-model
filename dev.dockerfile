FROM python:3.13

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/


EXPOSE 8003

CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8003"]
