FROM python:3.8-slim-buster

ENV TZ Europe/Moscow

RUN mkdir -p /app

WORKDIR /app

# copy the code
COPY . /app

RUN pip install -r requirements.txt

CMD ["python", "vsratoslav_jr_bot.py"]
