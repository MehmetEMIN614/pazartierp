FROM python:3.10-slim-buster
LABEL authors="PAZARTI"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update -yq

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip
RUN pip install -r base.txt

CMD ["bash","/app/docker-entrypoint.sh"]