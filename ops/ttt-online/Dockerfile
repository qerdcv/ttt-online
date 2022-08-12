FROM python:3 as base
EXPOSE 4444
WORKDIR /server
COPY ttt-online/requirements.txt .
RUN pip install -r requirements.txt

FROM base as dev
RUN pip install aiohttp-devtools

FROM base as test
COPY ttt-online/requirements.test.txt .
COPY pytest.ini .
RUN pip install -r requirements.test.txt
