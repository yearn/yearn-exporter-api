FROM python:3.9-bullseye

RUN mkdir -p /app
WORKDIR /app
ADD requirements.txt  ./
RUN pip install -r requirements.txt
ADD . /app

ENTRYPOINT ["flask", "run", "--host=0.0.0.0"]