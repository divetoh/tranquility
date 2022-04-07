FROM python:3.9
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /src

ADD / /src/

RUN pip install --no-cache-dir --upgrade -r requirements.txt
