import sys
import feedparser
import requests

from loguru import logger

from typing import Optional, List
from dataclasses import dataclass, asdict

from unidecode import unidecode
from urllib.request import ProxyHandler
from tenacity import retry, stop_after_attempt

try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote

from bs4 import BeautifulSoup


HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:27.0) Gecko/20100101 Firefox/27.0'}


@dataclass
class ArxivMeta:
    _id: str = None
    abs_url: Optional[str] = None
    pdf_url: Optional[str] = None
    title: Optional[str] = None
    authors: Optional[List[str]] = None
    updated: Optional[str] = None
    published: Optional[str] = None
    journal: str = "arxiv"

    def factory(self, data):
        new_data = []
        for x in data:
            if x[1] is None:
                continue
            new_data.append(x)
        return dict(new_data)

    def todict(self):
        return asdict(self, dict_factory=self.factory)

    def __str__(self):
        return f'{self.abs_url} - {self.title}'

    def __repr__(self):
        return f'ArxivMeta(_id={self._id}, title={self.title}, authors={self.authors}, updated={self.updated}, published={self.published})'


def _set_proxy_handler(proxy):
    proxy_handler = ProxyHandler({"http": f"http://{proxy}", "https": f"https://{proxy}"})
    return proxy_handler

@retry(stop=stop_after_attempt(3))
def fetch(abs_url, proxy=None):
    _id = abs_url.split('/')[-1]
    url = f"http://export.arxiv.org/api/query?search_query=id:{quote(unidecode(_id))}"
    logger.info(f'fetching <{_id}>: {url} ...')
    try:
        if proxy:
            result = feedparser.parse(url, handlers=[_set_proxy_handler(proxy)], request_headers=HEADERS)
        else:
            result = feedparser.parse(url, request_headers=HEADERS)
        items = result.entries
        item = items[0]
        item['id'] = _id

        arxiv_meta = ArxivMeta(
            _id=item.id,
            abs_url=abs_url,
            pdf_url=item.links[1].href,
            title=item.title.strip().replace('\n', ''),
            authors=[author["name"] for author in item.authors],
            updated=item.updated.split("T")[0],
            published=item.published.split("T")[0]
        )

        return arxiv_meta
    except Exception as e:
        logger.error(f'Failed: {e}')

def _get_html_node(url, tag, attrs=None):
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, features='lxml')
    node = soup.findAll(tag, attrs=attrs)
    return node

@retry(stop=stop_after_attempt(3))
def search(key_words, serchtype='title', abstracts='hide', order='-announced_date_first', size=100):
    ori_key_words = key_words
    key_words = key_words.split(',')
    query = "+".join([f"%22{'+'.join(word.split())}%22" for word in key_words])
    url = f"https://arxiv.org/search/?query={query}&searchtype={serchtype}&abstracts={abstracts}&order={order}&size={size}"
    logger.info(f'searching <{ori_key_words}>: {url} ...')

    node = _get_html_node(url, 'ol', {'class': 'breathe-horizontal'})[0]

    arxiv_meta_list = []
    for i, li in enumerate(node.findAll('li')):
        arxiv_meta = ArxivMeta(
            _id=li.find('p', attrs={'class': 'list-title'}).findAll('a')[0].text.split(':')[-1],
            abs_url=li.find('p', attrs={'class': 'list-title'}).findAll('a')[0].get('href'),
            pdf_url=li.find('p', attrs={'class': 'list-title'}).findAll('a')[1].get('href'),
            title=li.find('p', attrs={'class': 'title'}).text.strip().replace('\n', ''),
            authors=li.find('p', attrs={'class': 'authors'}).findAll('a')[0].text.split()
        )
        arxiv_meta_list.append(arxiv_meta)
    return arxiv_meta_list


if __name__ == "__main__":
    logger.remove()
    logger.add(sys.stdout, level="INFO")

    arxiv_meta = fetch('1706.03762')

    logger.info(arxiv_meta)

    arxiv_meta_list = search('active learning,object detection')

    for item in arxiv_meta_list:
        logger.info(item)
