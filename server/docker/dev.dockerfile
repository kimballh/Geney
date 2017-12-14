FROM python:3.6-jessie

RUN apt-get update && \
    apt-get install -y gcc

RUN pip install Flask==0.12.2 flask_failsafe fastnumbers h5py gunicorn jsonschema greenlet eventlet redis

WORKDIR /root/


CMD [ "python3", "failsafe-app.py"]