import urllib.request
from lxml import etree
def create_request(page):#定制请求
    if(page==1):
        url='https://sc.chinaz.com/tupian/fengjingtupian.html'
    else:
        url='https://sc.chinaz.com/tupian/fengjingtupian_'+str(page)+'.html'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.69'
    }
    request = urllib.request.Request(url=url,headers=headers)
    return request
def get_content(request):#获取网页源码
    response=urllib.request.urlopen(request)
    content=response.read().decode('utf-8')
    return content
def download_picture(content):#下载图片
    tree=etree.HTML(content)
    src_list=tree.xpath("//div[@class='item']/img/@data-original")#获取图片所在网址，此时的网址没有前缀https:
    name_list=tree.xpath("//div[@class='item']/img/@alt")#获取图片名称
    #注意1：有时网页的xpath路径与python中的不同，此时需要输出content源码，在其中找图片网址
    #注意2：如果此时src_list为空，说明网页进行了懒加载，即未划到图片时和划到图片时的@data-original值不同，需要在网页源码中找到未划到时的值作为xpath路径
    for i in range(len(src_list)):
        name=name_list[i]
        src=src_list[i]
        url="http:"+src
        urllib.request.urlretrieve(url=url,filename='./zhanzhang_picture_test/'+name+'.jpg')#使用网址下载图片，filename为路径及文件名
if __name__ == '__main__':
    start_page=int(input("起始页码："))
    end_page=int(input("结束页码："))
    for page in range(start_page,end_page+1):
        request=create_request(page)
        content=get_content(request)
        #print(content)
        download_picture(content)