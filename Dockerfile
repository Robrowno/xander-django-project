FROM python:3.9-alpine3.13

LABEL maintainer = 'christian.brown@xandertalent.com'

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt

COPY ./app /app

WORKDIR /app

EXPOSE 8000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    adduser --disabled-password unknown-user

ENV PATH='/py/bin:$PATH'

USER unknown-user
