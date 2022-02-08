import scrapy

class IfconfigSpider(scrapy.Spider):
    name = 'check_tor'
    allowed_domains = ['ifconfig.me']
    start_urls = ['http://ifconfig.me/']
    def parse(self, response):
        self.log('IP : %s' % response.css('#ip_address').get())