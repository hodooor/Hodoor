FROM datagovsg/python-node

RUN mkdir /app
WORKDIR /app

RUN apt-get update
RUN apt-get install locales -y
COPY package.json .
RUN npm install
COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .
RUN mkdir ../database
RUN python3 manage.py migrate
RUN python3 manage.py collectstatic --noinput

CMD python manage.py runserver 0.0.0.0:8000
