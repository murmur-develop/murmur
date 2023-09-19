# murmur
_囁き声のように優しい読み上げbot_  
discordのボイスチャットをvoicevoxで読み上げるためのbotです。  
## development

### create .env file
```bash
touch .env
```
`.env_sample`を参考にDiscord botのTokenを書いてください。  
### use docker-compose
#### build
```bash
docker compose build
```
#### run
```bash
docker compose up
```

## commands
`/join [voice_channel_name]`  
ボイスチャンネルに接続します。  
引数が無い場合はコマンドを入力したチャンネルに接続します。  
`/bye`  
ボイスチャンネルから退出します。

## クレジット
VOICEVOX  
[VOICEVOX 公式ページ](https://voicevox.hiroshiba.jp/)
