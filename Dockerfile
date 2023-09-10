FROM voicevox/voicevox_engine:cpu-ubuntu20.04-latest

RUN apt-get update
RUN apt-get install -y ffmpeg libnacl-dev python3-dev

RUN mkdir /myapp
COPY /src /myapp
COPY requirements.txt /myapp

RUN /opt/python/bin/pip3 install install -r /myapp/requirements.txt

COPY start.sh start.sh

CMD ./start.sh