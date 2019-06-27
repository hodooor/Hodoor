FROM node:12-alpine AS build

RUN mkdir -p /src
WORKDIR /src

COPY package.json .

RUN npm install

FROM python:3.6-alpine

RUN mkdir -p /app/src /app/database
WORKDIR /app/src

RUN apk add build-base
RUN apk add python3-dev
RUN apk add --update --no-cache g++ gcc libxslt-dev musl-dev jpeg-dev zlib-dev libffi-dev cairo-dev pango-dev gdk-pixbuf

COPY --from=build /src .
COPY requirements.txt .

RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn

COPY . .

RUN python3 manage.py migrate

RUN python3 manage.py collectstatic --noinput


CMD gunicorn --bind 0.0.0.0:8000 ticker.wsgi:application
