FROM python:3.9

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
COPY ./client_secrets.json /app/client_secrets.json

RUN pip install -r requirements.txt

COPY ./main.py /app/main.py

CMD ["fastapi", "run", "/app/main.py", "--port", "8080", "--proxy-headers"]
