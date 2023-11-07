from itemadapter import ItemAdapter
class ScrapyDangdangwangPipeline:#此条管道用来下载所有数据
    def open_spider(self,spider):#在爬虫执行前执行的函数，注意函数名不能写错，因为该写法相当于重写已提供的函数
        self.fp = open('book.json','w',encoding='utf-8')#只打开一次文件，不存在被覆盖写入的问题，原方法写一次就关一次文件，再次打开文件进行写入时会覆盖原内容
    def process_item(self, item, spider):#item就是yield后面的book对象
        # with open('book.json','a',encoding='utf-8') as fp:#将book数据存储到json文件中，注意'w'是覆盖写入，需要用追加'a'
        #     fp.write(str(item))#write必须是字符串对象
        #以上这种模式不推荐，因为每传递一个book就打开一次文件，对文件的操作过于频繁
        self.fp.write(str(item))#写入的本质是将内容以追加的方式写入缓冲区，在文件关闭时将缓冲区内容追加/覆盖写入文件中
        return item#函数本身的返回值（不能更改）
    def close_spider(self,spider):#同open_spider，是在爬虫文件执行完后执行的方法
        self.fp.close()#只关闭一次文件，此时缓冲区已存储全部book数据。注意self.fp也不能写错（也是内置重写）
import urllib.request
class Dangdangwang_downloadPipeline:#用来下载图片
    def process_item(self, item, spider):
        url = 'http:'+item.get('src')#item对象在items.py中定义，以字典形式存储数据，因此上面str(item)是一个json数据，而此处也能使用get方法由键获取值。注意item里面的url没加http头，要补上
        jpg_name = item.get('name').replace("/","或").replace("\\","或").replace("*","x").replace(":","：").replace("?","？").replace("\"","”").replace("|","I").replace("<","《").replace(">","》")#去掉文件名中不允许的字符
        file_name = './book_pic/'+jpg_name+'.jpg'#存储在books文件夹下
        urllib.request.urlretrieve(url=url,filename=file_name)
        return item