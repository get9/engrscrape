from xxhash import xxh64
from urlparse import urljoin, urlsplit

# Hash the url. Can change hash function if necessary, but xxhash is fast.
def gethash(url):
    return xxh64(url).hexdigest()

# Filter out any domains that are not a part of the domain(s) we care about
def filter_external_domains(allowed_domains, page_links):
    return filter(lambda x: urlsplit(x)[1] in allowed_domains, page_links)
