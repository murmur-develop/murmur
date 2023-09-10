# voicevox_discord_bot
discordのチャットをvoicevoxで読み上げるためのdiscord botです。
ffmpegのインストールが必要です。
## development

### create .env file
```bash
touch .env
```
.env_sampleを参考にDiscord botのTokenを書いてください。
### setup enviroment(venv)
```bash
python -m venv env
```
### activate env
```bash
source env/bin/activate
```
### install python packages
```bash
pip install -r requirements.txt
```
### deactivate env
```bash
deactivate
```
### start voicevox engine(docker)
```bash
docker pull voicevox/voicevox_engine:cpu-ubuntu20.04-latest
docker run --rm -it -p '127.0.0.1:50021:50021' voicevox/voicevox_engine:cpu-ubuntu20.04-latest
```
### start bot
```bash
python src/main.py
```

## docker
### build
```bash
docker image build -t voicevox_discord_bot .
```
### container run
```bash
docker container run --rm -it --env-file ".env" voicevox_discord_bot
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
