FROM python:3.9-slim-buster

WORKDIR /app

ADD geo-indexer.py .

RUN pip install --no-cache-dir pyzabbix
RUN pip install --no-cache-dir elasticsearch[async]

CMD [ "python", "./geo-indexer.py"]