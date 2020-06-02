FROM python:3.8.1-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./Pipfile ./Pipfile.lock ./
RUN pip install pipenv
RUN pipenv install --system

COPY . .

CMD python manage.py run -h 0.0.0.0
