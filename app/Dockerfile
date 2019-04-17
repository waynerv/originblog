# MAINTAINER        Waynerv <ampedee@gmail.com>
# DOCKER-VERSION    18.09.5-ce, build e8ff056

FROM python:3.6.7-alpine3.8
LABEL maintainer="ampedee@gmail.com"
# COPY pip.conf /root/.pip/pip.conf

RUN mkdir -p /usr/src/app  && \
    mkdir -p /var/log/gunicorn

WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/requirements.txt

RUN pip install --no-cache-dir gunicorn && \
    pip install --no-cache-dir -r /usr/src/app/requirements.txt && \
    pip install --ignore-installed six

#RUN echo "https://mirror.tuna.tsinghua.edu.cn/alpine/v3.8/main/" > /etc/apk/repositories
#
#RUN apk update \
#    && apk upgrade \
#    && apk add --no-cache bash \
#    bash-doc \
#    bash-completion \
#    && rm -rf /var/cache/apk/* \
#    && /bin/bash

COPY . /usr/src/app

#ENV LC_ALL 'en_US.UTF-8'
#ENV LANG 'en_US.UTF-8'
EXPOSE 8000

CMD ["/usr/local/bin/gunicorn", "-w", "4", "-b", ":8000", "wsgi:app"]