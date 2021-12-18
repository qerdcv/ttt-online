FROM python:3
WORKDIR server
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 4444