from engrscrape.items import URLItem
from engrscrape.util import gethash

from scrapy import Request
from scrapy.contrib.spiders import CrawlSpider

# Main spider class
class EngrSpider(CrawlSpider):
    name = 'engrspider'
    allowed_domains = [
        'engr.uky.edu',
        'cs.uky.edu'
    ]
    start_urls = [
        'http://www.engr.uky.edu'
    ]

    # Default callback for parsing response from fetch
    def parse(self, response):
        self.log("{}".format(response.url))
        page_links = response.xpath('//a/@href').extract()
        url_outlinks = set(gethash(u) for u in page_links)
        # Not sure how this works, but apparently you can yield two things and
        # it will Just Work (TM)
        yield URLItem(url=response.url, xhash=gethash(response.url), outlinks=url_outlinks)
        for url in page_links:
            yield Request(url, callback=self.parse)
