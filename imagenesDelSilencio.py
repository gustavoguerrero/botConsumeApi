import scrapy
import os
from scrapy.http import Request
from urllib import request
from cfg import imagenesSilencio as startUrl


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = startUrl

    def parse(self, response):
        for quote in response.xpath('//main/a'):
            pos = quote.xpath('./@href').get()
            link = f'{self.start_urls[0]}/{pos}'
            yield Request(link, callback=self.parse_imagenes, meta={
                                                            "link":link
                                                            })

    def parse_imagenes(self, response):

        link = response.meta.get('link')
        preUrlFoto = response.xpath('//div[@class="Page_downloadContainer__i0CzX"]/a[2]/@href').get()
        name = preUrlFoto.split("/")[-1].split(".")[0]
        
        preUrlFoto = preUrlFoto.replace(" ", "%20")
        print(f'\n######PRE URL FOTO {preUrlFoto}######')
        nombreFoto = preUrlFoto.split('/media/')[1]
        print(f'\n######NOMBRE FOTO {nombreFoto}######')
        urlFoto = self.start_urls[0] + preUrlFoto
        
        
        print(f'\n######URL FOTO {urlFoto}######')
        try:
            os.makedirs('carpeta')
        except FileExistsError:
            pass
        ruta = os.path.join('/home/veodoble/Documentos/workplace/Python/Scrapy/carpeta/', nombreFoto)
        
        request.urlretrieve(urlFoto, ruta)

        yield {
            'name':name,
            'link': link,
            'nombreFoto': nombreFoto,
            'urlFoto': urlFoto
        }