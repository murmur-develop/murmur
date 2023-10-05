from io import BytesIO
from dataclasses import dataclass
import re
from discord.message import Guild
import os
from os import path
import asyncio
from concurrent.futures import ThreadPoolExecutor

voicevox_path = (
    os.environ["VOICEVOX_PATH"]
    if "VOICEVOX_PATH" in os.environ
    else path.join(path.dirname(__file__), "../voicevox_core/")
)

from voicevox_core import VoicevoxCore


class Voicevox:
    core: VoicevoxCore
    thread_pool: ThreadPoolExecutor

    def __init__(
        self,
        dict_dir=path.join(voicevox_path, "open_jtalk_dic_utf_8-1.11"),
        thread_pool=ThreadPoolExecutor(max_workers=8),
    ) -> None:
        self.core = VoicevoxCore(open_jtalk_dict_dir=dict_dir, load_all_models=True)
        self.thread_pool = thread_pool

    async def genarete_sound(
        self, text: str, guild: Guild, speaker=1, speed=100, pitch=0
    ) -> BytesIO | None:
        # Mention先のUserID取得
        mention_id = re.search("[0-9]+", text)
        if mention_id is not None:
            member = guild.get_member(int(mention_id.group()))
            if member is not None:
                user_name = member.display_name
                # @{user_id} を @{display_name}さん に置き換える
                text = text.replace(mention_id.group(), user_name + "さん")

        query = self.core.audio_query(text, speaker)
        query.speed_scale = speed / 100
        query.pitch_scale = pitch / 100

        if len(text) < 25:
            return BytesIO(self.core.synthesis(query, speaker))
        else:

            def _fn():
                return BytesIO(self.core.synthesis(query, speaker))

            try:
                return await asyncio.wait_for(
                    asyncio.wrap_future(self.thread_pool.submit(_fn)), timeout=120
                )
            except:
                return None
