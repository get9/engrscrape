import sqlite3

from scrapy import log

HEX_BASE = 16

# Check if database currently contains a URL
def has_url(conn, item):
    check_url = "SELECT * FROM urls WHERE hash = ?"
    with conn.cursor() as curs:
        curs.execute(check_url, (int(item['xhash'],), HEX_BASE))
        if curs.fetchone():
            return True
    return False

# Adds an item to the database; assumes that it doesn't already exist (taken
# care of by the FilterDuplicatesPipeline in pipelines.py)
def add_url(conn, item):
    add = "INSERT INTO urls VALUES (?, ?)"
    with conn.cursor() as curs:
        curs.execute(add, (int(item['xhash'], HEX_BASE), item['url']))

# Adds outlinks to the linkgraph table. By virtue of the
# FilterDuplicatesPipelineObject and the fact that add_url and add_outlinks are
# called together in the same process_item method, this should only have unique
# entries in it. Exception checking is included for sanity's sake.
def add_outlinks(conn, item):
    add = "INSERT INTO linkgraph VALUES (?, ?)"
    with conn.cursor() as curs:
        for h in item['outlink']:
            try:
                curs.execute(add, (int(item['xhash'], HEX_BASE), int(h, HEX_BASE)))
            except sqlite3.IntegrityError:
                log("outlinks for '{}' already exist".format(item['url']))
