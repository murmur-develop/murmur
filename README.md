# murmur
_囁き声のように優しい読み上げbot_  
discordのボイスチャットをvoicevoxで読み上げるためのbotです。  
## development

### create .env file
```bash
touch .env
```
`.env_sample`を参考にDiscord botのTokenを書いてください。  
外部のVOICEVOXサーバーを使用する場合は`VOICEVOX_HOST=`で設定してください。
### use docker-compose
#### build
```bash
docker compose build
```
#### run
```bash
docker compose up
```
### use venv and VOICEVOX docker image
ffmpegのインストールが必要です。
#### setup environment(venv)
```bash
python -m venv env
```
#### activate env
```bash
source env/bin/activate
```
#### download voicevox core
```bash
curl -OL https://github.com/VOICEVOX/voicevox_core/releases/download/0.14.4/download.sh
sh ./download.sh --version 0.14.4 --os <linux|windows|osx>
```
#### install python library for voicevox core
```bash
$whl_file=voicevox_core-0.14.4+cpu-cp38-abi3-<linux|windows|osx>_<arch>.whl
curl -OL https://github.com/VOICEVOX/voicevox_core/releases/download/0.14.4/$whl_file
pip install ./$whl_file
```
#### install python packages
```bash
pip install -r requirements.txt
```
#### start bot
```bash
python src/main.py
```
#### deactivate env
```bash
deactivate
```

## commands
`$join [voice_channel_name]`  
ボイスチャンネルに接続します。  
引数が無い場合はコマンドを入力したチャンネルに接続します。  
`$bye`  
ボイスチャンネルから退出します。

## クレジット
VOICEVOX  
[VOICEVOX 公式ページ](https://voicevox.hiroshiba.jp/)
