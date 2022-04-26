FROM python:3.9
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /src

ADD / /src/

RUN apt-get update && apt-get install -y cron

RUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN crontab /src/crontab
