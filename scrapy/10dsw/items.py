import scrapy
class ScrapyDswItem(scrapy.Item):
    name = scrapy.Field()#别忘了结尾的括号
    src = scrapy.Field()
