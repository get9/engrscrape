# -*- coding: utf-8 -*-

# Scrapy settings for engrscrape project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'engrscrape'

SPIDER_MODULES = ['engrscrape.spiders']
NEWSPIDER_MODULE = 'engrscrape.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'engrscrape (+http://www.engr.uky.edu)'

# Respect robots.txt
ROBOTSTXT_OBEY = True
