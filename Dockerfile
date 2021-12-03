FROM python:3.6

USER root
WORKDIR /root
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./EasyPOS/
RUN pip install -r EasyPOS/requirements.txt
COPY . ./EasyPOS/

EXPOSE 5432:5432
# RUN /bin/bash run.sh