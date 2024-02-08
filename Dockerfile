FROM python:3.10.6

ENV NVIDIA_VISIBLE_DEVICES all

RUN apt-get update

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY src/ ./app/src/
COPY ./app.py ./app/

ENV WORKDIR=/app
WORKDIR $WORKDIR

CMD ["python", "app.py"]