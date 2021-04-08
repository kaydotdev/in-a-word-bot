import asyncio
import aiohttp
import logging

from lxml import html
from datetime import datetime


class EveripediaExtractor:
    href_prefix = 'https://api.everipedia.org/v2/wiki/extra/lang_en/'

    def __transform__(self, href):
        topic = href.split('/')[-1]
        return self.href_prefix + topic

    async def extract(self, resource: str) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.__transform__(resource)) as response:
                try:
                    resp_body = await response.json()
                    source_text = resp_body['schema']['articleBody']
                except Exception as ex:
                    logging.error(f'[{datetime.now()}@root] {ex}')
                    source_text = ""

        logging.info(f'[{datetime.now()}@root] Collected source from source "everipedia": {source_text}')
        return source_text


class CitizendiumExtractor:
    async def extract(self, resource: str) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(resource) as response:
                try:
                    document = html.fromstring(await response.text())
                    text_containers = document.cssselect("#mw-content-text")

                    if len(text_containers) != 0:
                        source_text = " ".join([container.text_content().replace("\n", "")
                                                .replace("\r", "").replace("\t", "")
                                                for container in text_containers])
                    else:
                        source_text = ""
                except Exception as ex:
                    logging.error(f'[{datetime.now()}@root] {ex}')
                    source_text = ""

        logging.info(f'[{datetime.now()}@root] Collected source from source "citizendium": {source_text}')
        return source_text


class OxfordreExtractor:
    async def extract(self, resource: str) -> str:
        return ""


async def parse_corpus_from_sources(resources: list) -> str:
    extractors = {
        'everipedia': EveripediaExtractor(),
        'citizendium': CitizendiumExtractor(),
        'oxfordre': OxfordreExtractor()
    }

    tasks = [extractors[resource[2]].extract(resource[1])
             for resource in resources]

    return '\n'.join(list(await asyncio.gather(*tasks)))
