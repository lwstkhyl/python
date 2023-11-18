import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_dsw.items import ScrapyDswItem
class DswSpider(CrawlSpider):
    name = 'dsw'
    allowed_domains = ['www.dushu.com']
    start_urls = ['https://www.dushu.com/book/1188_1.html']

    rules = (
        Rule(LinkExtractor(allow=r'/book/1188_\d+\.html'),#或修改为/book/1188(_\d+)*\.html
             callback='parse_item',
             follow=False),#follow参数表示是否跟进
    )
    '''
    在第一页时，底下页码只能看到第13页，而只有在第二页时才能看到第14页
    若不设置跟进（如上），就只访问start_url网页提取到的链接，即1-13页
    若设置跟进(=True)，就在每次访问网页时都提取链接，并访问所有提取到的链接
    例如在访问第13页时，可以获取13-25页的链接，若设置了跟进，就会继续访问14-25页，
    以此类推，直至获取不到链接（所有页数都访问过了）
    此处为了节省运行时间不设置跟进
    '''
    def parse_item(self, response):
        img_list = response.xpath('//div[@class="bookslist"]//img')
        for img in img_list:
            name = img.xpath('./@alt').extract_first()
            src = img.xpath('./@data-original').extract_first()
            book = ScrapyDswItem(name=name,src=src)
            yield book
