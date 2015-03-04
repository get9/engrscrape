from __future__ import print_function
from xxhash import xxh64

import sys
import pickle
import sqlite3

# Hashing function used in previous crawl
def gethash(x):
    return xxh64(x).hexdigest()

# Load graph in via pickle
def read_graph(filename):
    with open(filename, 'r') as f:
        try:
            graph = pickle.load(f)
        except:
            print("[error]: couldn't unpickle {}".format(filename), file=sys.stderr)
        return graph

# Need two lists of tuples:
#     - [(url, hash(url)]
#     - [(hash(url), hash(url))]
# Graph hash looks like this:
#     {
#         'url': {
#             'in': set([url, ...]),
#             'out': set([url, ...]),
#         }
#         ...
#     }
# where 'in' value is the set of inlinks
def construct_tuple_lists(graph):
    urls = []
    linkgraph = []
    for k, v in graph.iteritems():
        # Construct tuple for 'urls' table
        urlhash = gethash(k)
        urls.append((k, urlhash))
        
        # Parse outlinks and construct a hash for them
        for u in v['out']:
            linkgraph.append((urlhash, gethash(u)))

    return [urls, linkgraph]

# Puts tuples from each list into the db
# Note: Assumes db already exists
def lists2db(dbfile, urls, linkgraph):
    conn = sqlite3.connect(dbfile)
    with conn:
        curs = conn.cursor()
        insert_urls = "INSERT INTO urls VALUES (?, ?)"
        insert_linkgraph = "INSERT INTO linkgraph VALUES (?, ?)"
        curs.executemany(insert_urls, urls)
        curs.executemany(insert_linkgraph, linkgraph)

if __name__ == "__main__":
    _, graphname, dbname = sys.argv
    g = read_graph(graphname)
    urls, linkgraph = construct_tuple_lists(g)
    lists2db(dbname, urls, linkgraph)
