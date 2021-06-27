FROM python

RUN useradd -ms /bin/bash fastapi

USER fastapi
WORKDIR /backend

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY ./requirements.txt /backend/requirements.txt

RUN pip install --upgrade pip && pip install -r requirements.txt --user

COPY . /backend/