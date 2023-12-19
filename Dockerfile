FROM python:3.11

RUN mkdir /code
WORKDIR /code

COPY tox.ini ./
COPY custom_dist custom_dist/
COPY dependencies dependencies/
COPY tests tests/

RUN pip install -U pip
RUN pip install -r dependencies/requirements_prod.txt

COPY calendarapi calendarapi/
COPY tests tests/

EXPOSE 5000
