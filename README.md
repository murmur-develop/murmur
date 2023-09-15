# murmur
_囁き声のように優しいbot_  
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
#### setup enviroment(venv)
```bash
python -m venv env
```
#### activate env
```bash
source env/bin/activate
```
#### install python packages
```bash
pip install -r requirements.txt
```
#### start voicevox engine(docker)
```bash
docker pull voicevox/voicevox_engine:cpu-ubuntu20.04-latest
docker run --rm -it -p '127.0.0.1:50021:50021' voicevox/voicevox_engine:cpu-ubuntu20.04-latest
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
