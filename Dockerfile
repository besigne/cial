FROM python:3.12.2
LABEL authors="besigne"

WORKDIR /module
COPY . /module

RUN \
    if [ -f requirements ]; then pip install -r requirements; \
    else echo "Requirements files not found. Aborting" && exit 1; \
    fi

COPY . .