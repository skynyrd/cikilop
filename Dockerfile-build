FROM python:3.6.4-alpine3.7

ADD ./ /app
WORKDIR /app

RUN pip install -r ./requirements.txt
ENV PYTHONPATH /app

CMD [ "/bin/sh", "./build-scripts/test_and_publish.sh" ]