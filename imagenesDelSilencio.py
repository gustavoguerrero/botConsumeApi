import scrapy
import os
from scrapy.http import Request
from urllib import request
from cfg import headers


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = ['https://imagenesdelsilencio.uy/memoria/']

    async def start(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse,
                           headers=headers)


    def parse(self, response):
        for quote in response.xpath("//span[text()=' Ver Cartel']/ancestor::a"):
            pos = quote.xpath('./@href').get()
            link = f'{pos}'
            yield Request(link, callback=self.parse_imagenes, meta={"link":link},
                          headers=headers)

    def parse_imagenes(self, response):

        link = response.meta.get('link')
        name = link.split("/")[-1].split(".")[0]
        
        print(f'\n######URL FOTO {link}######')
        print(f'\n######NOMBRE {name}######')
        
        try:
            os.makedirs('carpeta')
        except FileExistsError:
            pass
        ruta = f'/home/veodoble/Documentos/workplace/botConsumeApi/carpeta/{name}.pdf'
        
        try:
            request.urlretrieve(link, ruta)
            print(f"\nArchivo descargado exitosamente")
            print(f'\n\n###### RUTA {ruta}######')
        except Exception as e:
            print(f"\n##### Error al descargar el archivo: {e}")

        yield {
            'name':name,
            'link': link,
        }