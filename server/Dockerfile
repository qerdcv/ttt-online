FROM python:3 as base
WORKDIR server
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 4444

FROM base as dev
RUN pip install aiohttp-devtools
