FROM python:3.11

RUN mkdir /code
WORKDIR /code

COPY requirements.txt requirements_tests.txt setup.py tox.ini ./
COPY custom_dist custom_dist/
COPY tests tests/

RUN pip install -U pip
RUN pip install -r requirements.txt
RUN pip install -e .

COPY calendarapi calendarapi/
COPY tests tests/

EXPOSE 5000
