FROM ubuntu:20.04
# FROM python:3.6

USER root
WORKDIR /root

RUN apt-get update && apt-get install -y software-properties-common gcc && \
    add-apt-repository -y ppa:deadsnakes/ppa

RUN apt-get update && apt-get install -y python3.6 python3-distutils python3-pip python3-apt
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client usbutils \
    && rm -rf /var/lib/apt/lists/*



COPY requirements.txt ./EasyPOS/
RUN python3.6 -m pip install --upgrade pip
RUN python3.6 -m pip install -r EasyPOS/requirements.txt
COPY . ./EasyPOS/

EXPOSE 5432:5432
# RUN /bin/bash run.sh