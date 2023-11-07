class ScrapyMoviePipeline:
    def open_spider(self,spider):
        self.fp = open('movie.json','w',encoding='utf-8')
    def process_item(self, item, spider):
        self.fp.write(str(item))
        return item
    def close_spider(self,spider):
        self.fp.close()
