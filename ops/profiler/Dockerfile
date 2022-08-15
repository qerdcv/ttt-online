FROM python:3 as base
EXPOSE 50051
WORKDIR /profiler
COPY profiler/requirements.txt .
RUN pip install -r requirements.txt
COPY profiler/ .

FROM base as dev
RUN pip install jurigged
CMD pgrate -p src/db/migrations -d postgres://$DB_USERNAME:$DB_PASSWORD@$DB_HOST:$DB_PORT/$DB_DATABASE && jurigged -v main.py

FROM base as test
COPY profiler/requirements.test.txt .
COPY pytest.ini .
RUN pip install -r requirements.test.txt
