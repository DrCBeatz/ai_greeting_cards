# Dockerfile

FROM python:3.10.4-slim-bullseye
ENV PIP_DISABLE_VERSION_CHCK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput