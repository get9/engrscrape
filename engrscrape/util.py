from xxhash import xxh64

# Hash the url. Can change hash function if necessary, but xxhash is fast.
def gethash(url):
    return xxh64(url).hexdigest()
