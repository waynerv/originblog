# MAINTAINER        Waynerv <ampedee@gmail.com>
# DOCKER-VERSION    18.09.5-ce, build e8ff056

FROM python:3.6.7-alpine3.8
LABEL maintainer="ampedee@gmail.com"

RUN mkdir -p /usr/src/app  && \
    mkdir -p /var/log/gunicorn

WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/requirements.txt

RUN pip install --no-cache-dir gunicorn && \
    pip install --no-cache-dir -r /usr/src/app/requirements.txt && \
    pip install --ignore-installed six

COPY . /usr/src/app

EXPOSE 8000

CMD ["/usr/local/bin/gunicorn", "-w", "4", "-b", ":8000", "wsgi:app"]