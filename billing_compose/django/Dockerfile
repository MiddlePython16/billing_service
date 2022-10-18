FROM python:3.9-slim

WORKDIR /code

COPY ./requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r /code/requirements.txt

COPY ./entrypoint.sh .
COPY ./src .

ENTRYPOINT ["./entrypoint.sh"]