#!/usr/bin/env bash
VOICEVOX_VERSION=0.14.4
DEVICE_TYPE=cpu

# voicevox coreのダウンロード
curl -L https://github.com/VOICEVOX/voicevox_core/releases/download/${VOICEVOX_VERSION}/download.sh \
  | bash /dev/stdin --device ${DEVICE_TYPE} --version ${VOICEVOX_VERSION} --os linux --output ./voicevox_core
ldconfig

pip install --upgrade pip
pip install -r requirements.txt

python scripts/install-bind.py ${DEVICE_TYPE}