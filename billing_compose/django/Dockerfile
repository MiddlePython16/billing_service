FROM python:3.9-slim

WORKDIR /code

COPY ./requirements.txt .
COPY ./entrypoint.sh .

RUN pip install --upgrade pip
RUN pip install -r /code/requirements.txt

COPY ./src .

ENTRYPOINT ["./entrypoint.sh"]