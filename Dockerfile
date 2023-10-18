FROM python:3.11

RUN mkdir /code
WORKDIR /code

COPY requirements.txt setup.py tox.ini ./
COPY custom_dist custom_dist/

RUN pip install -U pip
RUN pip install -r requirements.txt
RUN pip install -e .

COPY calendarapi calendarapi/
COPY tests tests/

EXPOSE 5000
