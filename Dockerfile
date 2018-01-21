FROM fedora:latest

WORKDIR /usr/src/app

COPY . .

RUN dnf install npm -y
RUN npm install
RUN dnf install gcc redhat-rpm-config python3-devel libffi-devel cairo pango -y
RUN pip3 install -r requirements.txt
RUN mkdir -p ../database
RUN python3 manage.py migrate
RUN python3 manage.py collectstatic --noinput

CMD python3 manage.py runserver 0.0.0.0:8000
