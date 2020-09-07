FROM python:3.8.5-slim-buster

RUN mkdir /backend
WORKDIR /backend
ENV PYTHONPATH /backend:$PYTHONPATH

COPY . /backend/
RUN pip config set global.index-url https://pypi.doubanio.com/simple \
    && pip install --no-cache-dir -r /backend/requirements.txt