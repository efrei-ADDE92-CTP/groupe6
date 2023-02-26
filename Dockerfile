FROM python:3.7-slim-buster

# RUN apt-get update && apt-get install -y python3-dev build-essential

RUN mkdir -p /groupe6/
WORKDIR /groupe6/

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# CMD ["bash", "-c", "uvicorn main:api_router --host 0.0.0.0 --port 5000"] on Windows
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "5000", "main:api_router"]
