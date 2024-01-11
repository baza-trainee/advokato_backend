FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

COPY tox.ini ./
COPY custom_dist custom_dist/
COPY dependencies dependencies/
COPY scripts scripts/

RUN pip install -U pip
RUN chmod a+x scripts/*.sh
RUN pip install -r dependencies/requirements_prod.txt

COPY calendarapi calendarapi/
COPY tests tests/

EXPOSE 5000
