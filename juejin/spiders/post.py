import scrapy
import json
from juejin.items import PostItem

ImgSrc = '''
    <script>
        const Images = document.querySelectorAll('img')
        for(let i=0; i<=Images.length; i++){
            let img = Images[i]
            if(!img) break
            img.src = img.getAttribute('data-src')
        }
    </script>'''


class Post(scrapy.Spider):
    name = 'post'
    allowed_domains = ['juejin.im']

    start_urls = [
        'https://juejin.im/post/6893286451711049742',
        'https://juejin.im/post/6893675091712802830',
        'https://juejin.im/post/6893435960705417224',
        'https://juejin.im/post/6893110732423397383',
        'https://juejin.im/post/6892786121189621774'
    ]

    # def start_requests(self):
    #     pass

    @staticmethod
    def getTitle(item, response):
        regx = '//article/h1/text()'
        return item

    @staticmethod
    def getMarkDownBody(item, response):
        regx1 = '//article/h1/text()'
        title = response.xpath(regx1).extract()[0].strip()
        print(title)
        regx = '//*[@class="markdown-body"]'
        data = response.xpath(regx).extract()[0] + ImgSrc
        # xdata = data.xpath('string(.)').extract()[0]
        with open("dist/%s.html" % title, 'wb') as f:
            f.write(data.encode(encoding='UTF-8'))
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
            self.getMarkDownBody(item, response)
            pass
