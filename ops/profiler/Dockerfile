FROM python:3 as base
EXPOSE 50051
WORKDIR /profiler
COPY profiler/requirements.txt .
RUN pip install -r requirements.txt
COPY profiler/ .

FROM base as dev
RUN pip install jurigged

FROM base as test
COPY profiler/requirements.test.txt .
COPY pytest.ini .
RUN pip install -r requirements.test.txt
