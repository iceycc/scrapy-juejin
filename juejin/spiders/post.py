import scrapy
import json
from juejin.items import PostItem


class Post(scrapy.Spider):
    name = 'post'
    allowed_domains = ['juejin.im']

    start_urls = ['https://juejin.im/post/6893286451711049742']

    # def start_requests(self):
    #     pass

    def getTitle(self, item, response):
        regx = '//*[@id="juejin"]/div[2]/main/div/div[1]/article/h1/text()'
        return item

    def getContent(self, item, response):
        regx = '//*[@class="markdown-body"]//p/text()'
        data = response.xpath(regx).extract()
        # print(data)
        return item

    def getImage(self, item, response):

        return item

    def getMarkDownBody(self,item,response):
       regx = '//*[@class="markdown-body"]'      
       data = response.xpath(regx)
       xdata = data.xpath('string(.)').extract[0]
       print(data)
       with open('index.html','wb') as f:
         f.write(xdata.encode(encoding='UTF-8')) 
       pass

    def parse(self, response):
        if 35000 > len(response.body):
            print(response.body)
            print(response.url)
        elif 404 == response.status:
            print(response.url)
        else:
            item = PostItem()
            self.getTitle(item, response)
            self.getContent(item, response)
            self.getMarkDownBody(item,response)
            pass
