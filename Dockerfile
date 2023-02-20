FROM python:3.9-alpine3.13
LABEL maintainer="abhaytiwarig"

ENV PYTHONUNBUFFERED 1
#ENV HTTP_PROXY_AUTH=basic:*:django-user:proxy_password
#ENV HTTP_PROXY=http://127.0.0.1:9000
#ENV HTTPS_PROXY=http://10.192.168.4:8000

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install psycopg2-binary && \
    #apk add --update --no-cache postgresql-client && \
    #apk add --update --no-cache --virtual .tmp-build-deps \
    #    build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    #apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

ENV PATH="/py/bin:$PATH"

USER django-user