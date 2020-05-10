# -*- coding: utf-8 -*-
import scrapy
from tarea1_scrapy.items import articles, article

class ArticleSpider(scrapy.Spider):
    name = 'article'
    allowed_domains = ['en.wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/Wikipedia:Featured_articles']

    custom_settings = {
        'FEED_FORMAT' : 'json',
        'FEED_URI' : 'file:C://Users//rsantizo//OneDrive - Comunicaciones Celulares, S.A//UVG//03_DA_PREP//data//tarea1_scrapy//tarea1-%(time)s.json'
    }


    def parse(self, response):
        host = self.allowed_domains[0]
        num_link = 0

        for link in response.css(".featured_article_metadata > a"):
            num_link = num_link +1
            if num_link > 200:
                break
            title = link.attrib.get("title")
            link = f"https://{host}{link.attrib.get('href')}"

            #yield articles(title = link.attrib.get("title"), link = f"https://{host}{link.attrib.get('href')}"  )
            yield response.follow(link,callback=self.parse_detail, meta={'link':link, 'title':title})

    def parse_detail(self, response):
        items = articles()
        item  = article()

        items["link"] = response.meta["link"]
        item["title"] = response.meta["title"]
        item["paragraph"] = list()

        num_parrafo = 0
        for text in response.css("div.mw-parser-output > p").extract():
            num_parrafo = num_parrafo +1
            item["paragraph"].append(text)
            # *** PUSE HASTA 2 PARRAFOS, YA QUE EN ALGUNOS CASOS EL PRIMERO Y SEGUNDO PARRAFO ESTAN VACIOS ***
            if num_parrafo > 1:
                break

        items["body"] = item
        return items