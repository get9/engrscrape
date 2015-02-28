from engrscrape.items import URLItem
from engrscrape.util import gethash, make_absolute_urls

import scrapy
from scrapy import Request
from scrapy.contrib.spiders import CrawlSpider

from urlparse import urlsplit

# Main spider class
class EngrSpider(CrawlSpider):
    name = 'engrspider'
    allowed_domains = [
        'engr.uky.edu',
        'cs.uky.edu',
    ]
    start_urls = [
        'http://www.engr.uky.edu/',
        'http://cs.uky.edu/',
    ]

    # Default callback for parsing response from fetch
    def parse(self, response):
        # Get a bunch of these errors on endpoint pages; just make outlinks
        # empty if we do.
        links = []
        if hasattr(response, 'xpath') and callable(getattr(response, 'xpath')):
            links = response.xpath('//a/@href').extract()
        else:
            links = []

        # Make every URL absolute so we can index, fetch, and hash appropriately
        page_links = make_absolute_urls(response.url, links)

        # Filter non-domain URLs from the list of page links.
        page_links = filter(lambda x: urlsplit(x)[1] in self.allowed_domains, page_links)
        url_outlinks = set(gethash(u) for u in page_links)
        yield URLItem(url=response.url, xhash=gethash(response.url), outlinks=url_outlinks)
        for url in page_links:
            yield Request(url, callback=self.parse)
