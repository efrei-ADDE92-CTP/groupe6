FROM python:3.7-slim-buster

RUN apt-get update && apt-get install -y python3-dev build-essential

RUN mkdir -p /usr/src/
WORKDIR /usr/src/

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "5000", "main:api_router"]