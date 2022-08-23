FROM python:3 as base
EXPOSE 8000
WORKDIR /server
COPY ttt-online-django/requirements.txt .
RUN pip install -r requirements.txt
COPY ttt-online-django/ .
