import asyncio
from processing.indexers import *


def flatten(array: tuple) -> list:
    return [item for sublist in array for item in sublist]


async def collect_hrefs(topic: str) -> list:
    indexers = [CitizendiumIndexer(),
                EveripediaIndexer(),
                OxfordreIndexer()]

    tasks = [indexer.index(topic) for indexer in indexers]
    return flatten(await asyncio.gather(*tasks))
