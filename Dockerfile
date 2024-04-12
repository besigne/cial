FROM python:3.12.2
LABEL authors="besigne"

ENV CONTAINER_NAME moudle

WORKDIR /module
COPY . /module

RUN \
    if [ -f requirements ]; then pip install -r requirements; \
    else echo "Requirements files not found. Aborting" && exit 1; \
    fi

COPY . .

ENTRYPOINT ["python", "-u", "-m", "module"]