# -*- coding: utf-8 -*-
import scrapy
import json
import datetime as dt
import re


class CarsSpider(scrapy.Spider):
    name = 'cars'
    allowed_domains = ['ebay-kleinanzeigen.de']
    start_urls = ['https://www.ebay-kleinanzeigen.de/s-immobilien/c195'] #['https://www.ebay-kleinanzeigen.de/s-autos/c216']
    imagere = re.compile(r"z\/(.+)\/\$\_\d{2}\.JPG")
    verkaufre = re.compile(r"verkauf|ankauf", re.I)

    def parse(self, response):
        for ad in response.css('h2.text-module-begin a'):
            if not self.verkaufre.search(ad.extract()):
                yield response.follow(ad, callback=self.parse_ad)
        for page in response.css('a.pagination-page'):
            yield response.follow(page, callback=self.parse)

    def parse_ad(self, response):
        desc = '\n'.join([i.strip() for i in response.xpath("//p[@id = 'viewad-description-text']//text()").extract()])

        if self.verkaufre.search(desc):
            return

        ks = list(filter(lambda v: v!='' and v!=',', [i.strip()[:-1] for i in response.xpath('//dt//text()').extract()]))
        vals_temp = [i.strip() for i in response.xpath('//dd//text()').extract()] #list(filter(lambda v: v!='' and v!=',', [i.strip() for i in response.xpath('//dd//text()').extract()]))

        vals = []
        add_to_last = False
        for i in range(len(vals_temp)):
            if add_to_last and vals_temp[i] != ',':
                vals[len(vals)-1] += (', ' + vals_temp[i])
                add_to_last = False
                continue
            if vals_temp[i] == '': continue
            if vals_temp[i] == ',':
                add_to_last = True
                continue
            else:
                vals.append(vals_temp[i])


        item = dict(zip(ks, vals))

        item['url'] = response.url
        item['desc'] = desc
        item['ts'] = dt.datetime.now().timestamp()


        try:
            item['price'] = response.css('h2#viewad-price.articleheader--price::text').re(r'[\d\.\,]+')[0]
        except IndexError:
            item['price'] = 'VB'

        try:
            item['pics'] = list(map(lambda url: self.imagere.findall(url)[0],filter(lambda url: url[-6:-4] == '57', response.css('div.imagebox-thumbnail img').xpath('@data-imgsrc').extract())))
        except IndexError:
            item['pics'] = self.imagere.findall(response.css('div.ad-image img').xpath('@src').extract_first())

        try:
            request = scrapy.Request("https://www.ebay-kleinanzeigen.de/s-vac-inc-get.json?adId={}&userId=25763233".format(item['Anzeigennummer']), callback=self.parse_views)
        except KeyError:
            item['views'] = 'nan'
            return item

        request.meta['item'] = item

        yield request


    def parse_views(self, response):
        item = response.meta['item']
        item['views'] = json.loads(response.body.decode("utf-8"))['numVisits']

        yield item

