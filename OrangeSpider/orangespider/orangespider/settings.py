# -*- coding: utf-8 -*-

# Scrapy settings for orangespider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
import os
import logging

BOT_NAME = 'orangespider'

SPIDER_MODULES = ['orangespider.spiders']
NEWSPIDER_MODULE = 'orangespider.spiders'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'orangespider (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'orangespider.middlewares.OrangespiderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'orangespider.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    # 'orangespider.pipelines.BookPipeline': 300,
    'orangespider.pipelines.BookPipeline': 3,
    'orangespider.pipelines.ArticlePipeline': 5,
}

# MONGO_URI = '127.0.0.1:27017'
# MONGO_DATABASE = 'crawl'
DATABASE = {'drivername': 'mysql',
            'host': '127.0.0.1',
            'port': '3306',
            'username': 'root',
            'password': 'zaq123456',
            'database': 'crawl',
            'query': {'charset': 'utf8'}}

# 图片下载设置
IMAGES_STORE = os.path.join(BASE_DIR, 'tmp')
IMAGES_EXPIRES = 30  # 30天内抓取的都不会被重抓

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# LOG_LEVEL = logging.INFO
# LOG_ENABLED = True
# LOG_STDOUT = True
# LOG_FILE = os.path.join(BASE_DIR, 'spider.log')
# LOG_FORMAT = "%(asctime)s [%(name)s] %(levelname)s: %(message)s"
