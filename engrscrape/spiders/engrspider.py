from engrscrape.items import URLItem
from engrscrape.util import gethash

from scrapy import Request, log
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.utils.url import canonicalize_url

from urlparse import urljoin, urlsplit

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
        #'http://cs.uky.edu/~jurek/advising/important_resources.sphp'
    ]

    # Default callback for parsing response from fetch
    def parse(self, response):
        #response = response.replace(url=response.url.strip().strip('.'))
        print("url = {}".format(response.url))
        current_url = response.url
        # Get a bunch of these errors on endpoint pages; just make outlinks
        # empty if we do.
        links = []
        if hasattr(response, 'xpath') and callable(getattr(response, 'xpath')):
            links = response.xpath('//a/@href').extract()

        # Make every URL absolute and canonical so we can index, fetch, and hash appropriately
        links = map(lambda l: l.strip().strip('.'), links)
        links = map(lambda l: urljoin(response.url, l), links)
        links = map(lambda l: canonicalize_url(l), links)
        before_domain_filter = set(links)

        # Filter non-domain URLs from the list of outlinks.
        links = filter(lambda x: urlsplit(x)[1] in self.allowed_domains, links)
        #print(before_domain_filter - set(links))
        url_outlinks = set(gethash(u) for u in links)
        yield URLItem(url=current_url, xhash=gethash(current_url), outlinks=url_outlinks)
        for url in links:
            yield Request(url, callback=self.parse)
