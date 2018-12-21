import scrapy
from zufangfenxi.items import ZufangfenxiItem


class FangjiaSpider(scrapy.Spider):
    name = 'Fangjia'

    start_urls = [
        'https://zz.lianjia.com/zufang/rs/'
    ]

    def parse(self, response):
        list_selector = response.css("div.content__list--item")

        for house in list_selector:
            area = house.css(".content__list--item--des::text").extract_first()
            price = house.css(".content__list--item-price em::text").extract_first()
            position = house.css("address.details-item strong::text").extract_first()
            rooms = '1'
            yield ZufangfenxiItem(area=area, price=price, position=position, rooms=rooms)