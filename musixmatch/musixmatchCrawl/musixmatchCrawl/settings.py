# Scrapy settings for musixmatchCrawl project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from dotenv import load_dotenv
import os

BOT_NAME = 'musixmatchCrawl'

SPIDER_MODULES = ['musixmatchCrawl.spiders']
NEWSPIDER_MODULE = 'musixmatchCrawl.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 8

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 8
#CONCURRENT_REQUESTS_PER_IP = 16

DOWNLOAD_TIMEOUT = 600 

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'musixmatchCrawl.middlewares.MusixmatchcrawlSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'musixmatchCrawl.middlewares.MusixmatchcrawlDownloaderMiddleware': 543,
#}

#########################################################################
### PRIVOXY WITH TOR 1
# DOWNLOADER_MIDDLEWARES = {
#     'musixmatchCrawl.middlewares.ProxyMiddleware.ProxyMiddleware': 543,
# }
#########################################################################

#########################################################################
### PRIVOXY WITH TOR 2
# see: https://datawookie.dev/blog/2021/06/scrapy-rotating-tor-proxy/
# DOWNLOADER_MIDDLEWARES = {
#     # 'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
#     'musixmatchCrawl.middlewares.rotatingProxies.RotatingProxyMiddleware': 610,
#     'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
# }

# ROTATING_PROXY_BAN_POLICY = 'musixmatchCrawl.middlewares.banPolicy.MyPolicy'

# ROTATING_PROXY_LIST = [
#     'http://127.0.0.1:9990',
#     'http://127.0.0.1:9991',
#     'http://127.0.0.1:9992',
#     'http://127.0.0.1:9993',
#     'http://127.0.0.1:9994',
#     'http://127.0.0.1:9995',
#     'http://127.0.0.1:9996',
#     'http://127.0.0.1:9997',
#     'http://127.0.0.1:9998',
#     'http://127.0.0.1:9999',
# ]

# ROTATING_PROXY_PAGE_RETRY_TIMES = 500

#########################################################################

########################################################################
## ZYTE
DOWNLOADER_MIDDLEWARES = {
  'scrapy_zyte_smartproxy.ZyteSmartProxyMiddleware': 610
  }
ZYTE_SMARTPROXY_ENABLED = True
ZYTE_SMARTPROXY_APIKEY = os.environ.get('ZYTE_SMARTPROXY_APIKEY')
########################################################################

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
  'musixmatchCrawl.pipelines.JsonWriterPipeline': 900,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = False
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
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


# # Splash settings
# SPLASH_URL = 'http://localhost:8050'

# DOWNLOADER_MIDDLEWARES = {
#   'scrapy_splash.SplashCookiesMiddleware': 723,
#   'scrapy_splash.SplashMiddleware': 725,
#   'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
# }

# SPIDER_MIDDLEWARES = {
#   'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
# }

# DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'

# HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'