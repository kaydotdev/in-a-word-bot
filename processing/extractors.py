import aiohttp
from lxml import html


class CitizendiumParser:
    domain = 'https://en.citizendium.org'
    weight = 0.05

    def __query_scheme__(self, topic) -> str:
        query_topic = topic.replace(' ', '+')
        return f"{self.domain}/wiki?title=Special%3ASearch&profile=default&search={query_topic}&fulltext=Search"

    def __extract__(self, document: html.HtmlElement) -> list:
        search_results = document.cssselect('ul.mw-search-results li')
        return [{
            'title': result.cssselect('div.mw-search-result-heading a')[0].text_content(),
            'href': self.domain + result.cssselect('div.mw-search-result-heading a')[0].attrib['href']
        } for result in search_results]

    async def parse(self, topic) -> list:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.__query_scheme__(topic)) as response:
                document = html.fromstring(await response.text())
                links = self.__extract__(document)

        return links
