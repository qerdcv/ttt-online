FROM python:3 as base
WORKDIR /server
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ttt-online/ .
EXPOSE 4444

FROM base as dev
RUN pip install aiohttp-devtools

FROM base as test
COPY requirements.test.txt .
COPY pytest.ini .
RUN pip install -r requirements.test.txt
