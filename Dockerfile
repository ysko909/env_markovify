FROM python:3.8-buster

ENV ACCEPT_EULA=Y

RUN apt-get update \
    && apt-get install -y g++ \
    apt-utils \
    apt-transport-https \
    gcc \
    build-essential \
    && apt-get upgrade -y \
    && apt-get clean \
    && pip install --upgrade pip \
    && pip install --no-cache-dir \
    autopep8 \
    flake8 \
    && rm -rf /var/lib/apt/lists/*

ADD . /home/workdir

WORKDIR /home/workdir

COPY ./requirements.txt ${PWD}

RUN pip install -r requirements.txt

RUN sudachipy link -t full

WORKDIR /home/workdir/src

EXPOSE 8888