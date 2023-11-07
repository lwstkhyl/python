import scrapy
class ScrapyMovieItem(scrapy.Item):
    name = scrapy.Field()
    src = scrapy.Field()
