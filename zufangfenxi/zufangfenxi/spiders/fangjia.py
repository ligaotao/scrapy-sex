import scrapy
from zufangfenxi.items import ZufangfenxiItem
import re

class FangjiaSpider(scrapy.Spider):
    name = 'Fangjia'

    start_urls = [
        'https://zz.lianjia.com/zufang/rs/'
    ]
    page = 1
    def parse(self, response):
        list_selector = response.css("div.content__list--item")

        for house in list_selector:
            text = house.css(".content__list--item--des::text")
            area = '0'
            rooms = '0'
            for t in text:
                if t.extract().find('㎡') >= 0:
                    area = re.findall(r"(\d+)㎡", t.extract())[0]
                elif t.extract().find('室') >= 0:
                    rooms = re.findall(r"(\d+)室", t.extract())[0]

            price = house.css(".content__list--item-price em::text").extract_first()
            position = house.css(".content__list--item--des a::text").extract_first()
            url = house.css(".content__list--item--title a::text").extract_first()
            yield ZufangfenxiItem(area=area, price=price, position=position, rooms=rooms, url=url)
        self.page += 1
        if self.page < 99:
            yield response.follow(f'https://zz.lianjia.com/zufang/pg{self.page}/#contentList', callback=self.parse)