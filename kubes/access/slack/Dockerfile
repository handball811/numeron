FROM python:3.7
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt

COPY ./run.py /code/run.py
COPY ./slackbot_settings.py /code/slackbot_settings.py
COPY ./plugins /code/plugins


ENTRYPOINT ["python","run.py"]

