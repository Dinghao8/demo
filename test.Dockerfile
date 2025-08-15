ARG PYTHON_VERSION=3.9
ARG FLASK_VERESION=3.0.3


FROM python:3.9-slim AS base
RUN  pip install flask==3.0.3  -i https://mirrors.aliyun.com/pypi/simple
WORKDIR /demo_project
COPY /hello.py /demo_project
ENV FLASK_APP=hello
EXPOSE 8000
CMD flask run --host 0.0.0.0 --port 8000

