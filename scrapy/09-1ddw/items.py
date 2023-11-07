import scrapy
class ScrapyDangdangwangItem(scrapy.Item):
    src = scrapy.Field() #书的图片url
    name = scrapy.Field() #名称
    price = scrapy.Field() #价格
