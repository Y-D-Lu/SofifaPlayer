# -*- coding: utf-8 -*-

import scrapy
import os

class player_url(scrapy.Spider):

    name = "playerurl"

    allowed_domains = ["sofifa.com"]

    start_urls = [
        "http://sofifa.com/players?offset=0"      #起始url
    ]

    def parse(self, response):

        sel = scrapy.Selector(response)

        url100 = sel.xpath('//*[@id="pjax-container"]/div/table/tbody/tr/td[1]/a/@href').extract()

        f = open('playerurl1.txt', 'a')  #a = append

        for url in url100: f.write('http://sofifa.com'+url+'?units=mks'+os.linesep)

        f.close()



        next_urls = sel.xpath('//*[@id="pjax-container"]/div/div[2]/ul/li[2]/a/@href').extract()


        for next_url in next_urls:
            next_url = "http://sofifa.com" + next_url
            print next_url
            yield scrapy.Request(next_url, callback=self.parse)