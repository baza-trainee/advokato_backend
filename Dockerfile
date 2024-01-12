FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

COPY . .

RUN chmod a+x scripts/*.sh && \
    pip install -U pip && \
    pip install -r dependencies/requirements_prod.txt

