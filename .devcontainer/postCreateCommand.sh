#!/usr/bin/env bash
VOICEVOX_VERSION=0.14.4
DEVICE_TYPE=cpu

# voicevox coreのダウンロード
# すでに存在する場合はスキップする
VERSION_FILE="./voicevox_core/VERSION"
VERSION_FILE_CONTENT=$(cat "$VERSION_FILE")
if [ "$VERSION_FILE_CONTENT" != "$VOICEVOX_VERSION" ]; then
  rm -rf ./voicevox_core
  curl -L https://github.com/VOICEVOX/voicevox_core/releases/download/${VOICEVOX_VERSION}/download.sh \
    | bash /dev/stdin --device ${DEVICE_TYPE} --version ${VOICEVOX_VERSION} --os linux --output ./voicevox_core
  ldconfig
else
  echo '[skip] voicevox_core download'
fi

pip install --upgrade pip
pip install -r requirements.txt

python scripts/install-bind.py ${DEVICE_TYPE}