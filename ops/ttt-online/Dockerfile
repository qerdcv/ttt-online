FROM python:3 as base
EXPOSE 4444
WORKDIR /server
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ttt-online/ .


FROM base as dev
RUN pip install aiohttp-devtools
ADD ops/ttt-online/adev.py .
CMD pgrate -p src/db/migrations -d postgres://$DB_USERNAME:$DB_PASSWORD@$DB_HOST:$DB_PORT/$DB_DATABASE && adev runserver .

FROM base as test-integration
COPY requirements.test.txt .
COPY pytest.ini .
RUN pip install -r requirements.test.txt
CMD pgrate -p src/db/migrations -d postgres://$DB_USERNAME:$DB_PASSWORD@$DB_HOST:$DB_PORT/$DB_DATABASE && python -m pytest -vv test/integration
