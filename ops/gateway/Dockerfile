FROM python:3 as base
EXPOSE 8888
WORKDIR /gateway
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY gateway/ .

FROM base as dev
RUN pip install aiohttp-devtools

FROM base as test
COPY requirements.test.txt .
COPY pytest.ini .
RUN pip install -r requirements.test.txt
