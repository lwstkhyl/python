import scrapy
from scrapy_dangdangwang.items import ScrapyDangdangwangItem
class DdwSpider(scrapy.Spider):
    name = 'ddw'
    allowed_domains = ['category.dangdang.com']
    start_urls = ['http://category.dangdang.com/cp01.01.02.00.00.00.html']
    base_url1 = 'http://category.dangdang.com/pg'
    base_url2 = '-cp01.01.02.00.00.00.html'
    page = 1
    def parse(self, response):
        li_list = response.xpath('//ul[@id="component_59"]//li')#获取所有的li标签，得到selector对象
        for li in li_list:#每个li都存储着一本书的图片、名字和价格
            src = li.xpath('.//img/@data-original').extract_first()#所有的selector对象都可以再次调用xpath方法
            if src:#如果src不为空（即使用data-original可以获取图片）就不作处理
                pass
            else:#如果src为空（即是第一张图片，无data-original）
                src = li.xpath('.//img/@src').extract_first()#就用@src进行获取
            name = li.xpath('.//img/@alt').extract_first()#注意xpath路径中的.很重要，若不加就相当于直接src=//ul[@id="component_59"]//li//img/@src
            name = name[2:]#去掉name开头的空格
            price = li.xpath('.//p[@class="price"]/span[1]/text()').extract_first()
            book = ScrapyDangdangwangItem(src=src,name=name,price=price)
            yield book
        if self.page<1:#共爬取100页
            self.page = self.page+1#注意要加self.
            url = self.base_url1+str(self.page)+self.base_url2
            yield scrapy.Request(url=url,callback=self.parse)#url就是请求地址，callback是要执行的函数（不需要加括号）