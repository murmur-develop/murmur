import aiohttp
import json
from io import BytesIO
from dataclasses import dataclass
import re
from discord.message import Guild

@dataclass
class Voicevox:
    host: str
    port: int

    async def genarete_sound(self, text: str, guild: Guild, speaker=1, speed=100, pitch=0) -> BytesIO | None:
        # Mention先のUserID取得
        mention_id = re.search('[0-9]+', text)
        if mention_id is not None:
            member = guild.get_member(int(mention_id.group()))
            if member is not None:
                user_name = member.display_name
                # @{user_id} を @{display_name}さん に置き換える
                text = text.replace(mention_id.group(), user_name + 'さん')

        params = (
            ('text', text),
            ('speaker', speaker),
        )
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(f'http://{self.host}:{self.port}/audio_query', params=params, timeout=30) as query_res:
                    if query_res.status != 200:
                        return None
                    headers = {'Content-Type': 'application/json'}
                    query_json = await query_res.json()
                    query_json["outputSamplingRate"] = 24000
                    query_json["speedScale"] = speed / 100
                    query_json["pitchScale"] = pitch / 100
                async with session.post(f'http://{self.host}:{self.port}/synthesis', headers=headers, params=params, data=json.dumps(query_json), timeout=30) as response:
                    if response.status != 200:
                        return None
                    try:
                        return BytesIO(await response.read())
                    except Exception as e:
                        print(f'error in synthesis : {e}')
                        return None
        except Exception as e:
            print(f'error in session: {e}')
            return None
