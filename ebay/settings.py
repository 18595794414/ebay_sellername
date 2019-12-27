# -*- coding: utf-8 -*-

import os

BASE_PATH = os.path.dirname(__file__)

BOT_NAME = 'ebay'

SPIDER_MODULES = ['ebay.spiders']
NEWSPIDER_MODULE = 'ebay.spiders'

# 禁用机器协议
ROBOTSTXT_OBEY = False


# 并发
CONCURRENT_REQUESTS = 16

DOWNLOAD_DELAY = 0.3

# 下载超时时间
DOWNLOAD_TIMEOUT = 30

# 日志级别
LOG_LEVEL = 'INFO'
# LOG_FILE = BASE_PATH + 'ebay_seller_name.log'

# 开启重试：
RETRY_ENABLED = True

# 重试次数
RETRY_TIMES = 3

# 同一时间最大请求数
CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# 禁用cookie
COOKIES_ENABLED = False

# 开启自动限速
AUTOTHROTTLE_ENABLED = True

# 开始下载时限速并延迟时间
AUTOTHROTTLE_START_DELAY = 1

# 高并发请求时最大延迟时间
AUTOTHROTTLE_MAX_DELAY = 15

# 平均每秒并发数
AUTOTHROTTLE_TARGET_CONCURRENCY = 4.0

# 是否显示
# AUTOTHROTTLE_DEBUG = False


# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
}


# SPIDER_MIDDLEWARES = {
#    'ebay.middlewares.EbaySpiderMiddleware': 543,
# }


DOWNLOADER_MIDDLEWARES = {
   # 'ebay.middlewares.EbayDownloaderMiddleware': 543,
}


# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }


ITEM_PIPELINES = {


}



# 启用Redis调度存储请求队列，使用Scrapy-Redis的调度器,不再使用scrapy的调度器
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# 确保所有的蜘蛛通过Redis的共享相同的重复过滤
DUPEFILTER_CLASS  =  "scrapy_redis.dupefilter.RFPDupeFilter"
REDIS_URL = 'redis://127.0.0.1:6379/0'

# Requests的调度策略，默认优先级队列
# SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.PriorityQueue'

# 允许暂停,redis请求记录不会丢失(重启爬虫不会重头爬取已爬过的页面)
SCHEDULER_PERSIST = True
