FROM python:3.7
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt

COPY ./manage.py /code/manage.py
COPY ./gateway /code/gateway

ENTRYPOINT ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]