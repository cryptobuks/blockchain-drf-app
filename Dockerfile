FROM python:3.7-alpine
MAINTAINER André Gustavo Castro - Web Apps Agency
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /blockchain_drf
WORKDIR /blockchain_drf
COPY ./blockchain_drf /blockchain_drf

RUN adduser -D blockchain
USER blockchain



