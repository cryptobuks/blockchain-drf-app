FROM python:3.7-alpine
MAINTAINER André Gustavo Castro - Web Apps Agency
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
      gcc libc-dev linux-headers postgresql-dev
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

RUN mkdir /blockchain_drf
WORKDIR /blockchain_drf
COPY ./blockchain_drf /blockchain_drf

RUN adduser -D blockchain
USER blockchain
