import scrapy


class demo(scrapy.Spider): # 需要继承spider类
    name = 'demo2'

    def start_requests(self):

        # 定义爬取链接
        urls = [
            'http://lab.scrapyd.cn/page/1/',
            'http://lab.scrapyd.cn/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        page = response.url.split("/")[-2]  # 根据上面的链接提取分页,如：/page/1/，提取到的就 1
        filename = 'mingyan-%s.html' % page  # 拼接文件名
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'保存文件 {filename}')
