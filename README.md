# voicevox_discord_bot
discordのチャットをvoicevoxで読み上げるためのdiscord botです。
ffmpegのインストールが必要です。
## development
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
python main.py
```
## クレジット
VOICEVOX  
[VOICEVOX 公式ページ](https://voicevox.hiroshiba.jp/)