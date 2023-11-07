import scrapy
from scrapy_movie.items import ScrapyMovieItem
class MovieSpider(scrapy.Spider):
    name = 'movie'
    allowed_domains = ['www.dytt8.net']#注意访问新地址要更改此项
    start_urls = ['http://www.dytt8.net/html/gndy/china/index.html']
    def parse(self, response):
        a_list = response.xpath('//div[@class="co_content8"]//td[2]//a[2]')#a标签的xpath
        for a in a_list:
            name = a.xpath('./text()').extract_first()#电影名称（即a标签里的内容），用text()方法获取
            href = a.xpath('./@href').extract_first()#下一个网站地址（即a标签内href属性值），用@获取
            url = "http://www.dytt8.net"+href#真正使用的网站地址
            yield scrapy.Request(url=url,callback=self.parse_second,meta={'first_name':name})#与上个案例不同的是，访问网页后爬取逻辑发生改变，需自定义另一个函数写入新的处理逻辑
            #meta可以将第一步爬取的信息传给下一步构造对象（以字典形式）
    def parse_second(self,response):
        src = response.xpath('//div[@id="Zoom"]//img/@src').extract_first()#图片网址
        #注意有时span等标签可能识别不成功，如//div[@id="Zoom"]/span/img/@src就拿不到数据，此时考虑删改xpath路径中的标签
        name = response.meta['first_name']#接收上面传过来的name
        movie = ScrapyMovieItem(src=src,name=name)
        yield movie#将最终的movie返回给管道