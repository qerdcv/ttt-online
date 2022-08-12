FROM python:3 as base
EXPOSE 8888
WORKDIR /gateway
COPY gateway/requirements.txt .
RUN pip install -r requirements.txt
COPY gateway/ .

FROM base as dev
RUN pip install aiohttp-devtools

FROM base as test
COPY gateway/requirements.test.txt .
COPY pytest.ini .
RUN pip install -r requirements.test.txt
