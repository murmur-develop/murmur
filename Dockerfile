FROM python:3.11

ARG VOICEVOX_VERSION=0.14.4
ARG DEVICE_TYPE=cpu

ENV LD_LIBRARY_PATH=/bot/voicevox_core/:$LD_LIBRARY_PATH

RUN apt-get update
RUN apt-get install -y ffmpeg libnacl-dev python3-dev

WORKDIR /bot

# voicevox coreのダウンロード
RUN curl -L https://github.com/VOICEVOX/voicevox_core/releases/download/${VOICEVOX_VERSION}/download.sh \
  | bash /dev/stdin --device ${DEVICE_TYPE} --version ${VOICEVOX_VERSION} --os linux --output ./voicevox_core
RUN ldconfig

COPY requirements.txt /bot
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Python用のラッパーをダウンロードしてインストールする
COPY /scripts /bot/scripts
RUN python scripts/install-bind.py ${DEVICE_TYPE}

COPY /src /bot/src
CMD ["python", "src/main.py"]