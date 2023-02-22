import scrapy
from scrapy.crawler import CrawlerProcess

import datetime as dt
import os


try:
    os.remove("./retail_spider/csv/scraps.csv")
    print("scraps.csv supprimé.")
except:
    print('Pas de fichier csv.')


class SolMurSpider(scrapy.Spider):

    name = "SolMurSpider"
    
    base_url = 'https://www.castorama.fr'
    
    def start_requests(self):

        urls = ['/carrelage-sol/cat_id_3630.cat']

        for url in urls:
            next_url = self.base_url + url
            yield scrapy.Request(url=next_url, callback=self.parse_cat)

    def parse_cat(self, response):
        
        cats = response.xpath('//*[@id="side-navigation-menu-1"]/li')

        next_urls = []

        for cat in cats:
            next_urls.append(cat.xpath('a/@href').get())

        if len(next_urls) > 0:
            for url in next_urls:
                next_url = self.base_url + url
                yield scrapy.Request(url=next_url, callback=self.parse_cat)

        else:
            products = response.xpath('//*[@id="content"]/div/div[1]/div/div/div[2]/div/div/div[3]/div/div[3]/div[2]/main/div/div[3]/ul/li')

            for product in products:
                url_product = product.xpath('div/a/@href').get()
                yield scrapy.Request(url=self.base_url + url_product, callback=self.parse_detail)

    def parse_detail(self, response):

        print('##############################', response)
        pass



process_base = CrawlerProcess(
    settings = {
        'FEEDS':{
            './retail_spider/csv/scraps.csv':{
                'format':'csv'
            }
        },
        'USER_AGENT' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
    }
)



process_base.crawl(SolMurSpider)
process_base.start()
process_base.stop()