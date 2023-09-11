FROM python:3.11

RUN apt-get update
RUN apt-get install -y ffmpeg libnacl-dev python3-dev

WORKDIR /bot

COPY requirements.txt /bot
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY /src /bot
CMD ["python", "src/main.py"]