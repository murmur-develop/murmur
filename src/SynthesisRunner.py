from voicevox_core import VoicevoxCore, AudioQuery
import psutil

from dataclasses import dataclass
from typing import Callable, Coroutine
from concurrent.futures import ThreadPoolExecutor
import asyncio
from asyncio import AbstractEventLoop, Task


@dataclass
class SynthesisTask:
    query: AudioQuery
    speaker: int
    callback: Callable[[bytes | None], None]


# CPU使用率を見て、適度に休憩しながら音声の生成を行う
class SynthesisRunner:
    tasks: list[SynthesisTask] = []
    async_tasks: set[Task] = set()

    core: VoicevoxCore
    loop: AbstractEventLoop

    threshold: float
    thread_pool: ThreadPoolExecutor

    def __init__(
        self,
        core: VoicevoxCore,
        loop: AbstractEventLoop,
        threshold=65,
        thread_pool=ThreadPoolExecutor(max_workers=50),
    ):
        self.core = core
        self.threshold = threshold
        self.thread_pool = thread_pool
        self.loop = loop

    def synthesis(
        self, query: AudioQuery, spaker: int, callback: Callable[[bytes | None], None]
    ):
        self.tasks.append(SynthesisTask(query, spaker, callback))

    def create_task(self, co: Coroutine):
        task = self.loop.create_task(co)
        self.async_tasks.add(task)
        task.add_done_callback(self.async_tasks.discard)

        return task

    def run(self):
        self.create_task(self._run())

    async def _run(self):
        while True:
            if len(self.tasks):
                perc = psutil.cpu_percent()
                await asyncio.sleep(perc / self.threshold * 5)

                task = self.tasks.pop(0)

                def _fn():
                    task.callback(self.core.synthesis(task.query, task.speaker))

                self.thread_pool.submit(_fn)

            else:
                await asyncio.sleep(0.1)
