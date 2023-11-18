class ScrapyDswPipeline:
    def open_spider(self,spider):
        self.fp = open('book.json','w',encoding='utf-8')
    def process_item(self, item, spider):
        self.fp.write(str(item))
        return item
    def close_spider(self,spider):
        self.fp.close()
from scrapy.utils.project import get_project_settings #加载settings文件
import pymysql
class MySQLPipeline:
    def open_spider(self, spider):
        settings = get_project_settings()
        self.host = settings['db_host']
        self.port = settings['db_port']
        self.user = settings['db_user']
        self.password = settings['db_password']
        self.name = settings['db_name']
        self.char_set = settings['db_char_set']
        self.connect() #与MySQL建立连接
    def connect(self):
        self.conn = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            db=self.name,
            charset=self.char_set
        )
        self.cursor = self.conn.cursor()
    def process_item(self, item, spider):
        sql = 'insert into book(name,src) values("{}","{}")'.format(item['name'],item['src']) #直接可以执行MySQL语句
        self.cursor.execute(sql) #执行语句
        self.conn.commit() #提交
        return item
    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close() #关闭连接