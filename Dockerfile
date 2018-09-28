FROM datagovsg/python-node

RUN mkdir -p /app/src /app/database
WORKDIR /app/src

RUN apt-get update && apt-get install -y \
    locales

COPY package.json .

RUN npm install

COPY requirements.txt .

RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn

COPY . .

RUN python3 manage.py migrate
RUN python3 manage.py collectstatic --noinput

CMD gunicorn --bind 0.0.0.0:8000 ticker.wsgi:application
