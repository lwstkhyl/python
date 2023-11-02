#获取源码↓
import requests
url="https://so.gushiwen.cn/user/login.aspx?from=http%3a%2f%2fso.gushiwen.cn%2fuser%2fcollect.aspx"
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.46',
}
response=requests.get(url=url,headers=headers)
content=response.text
#隐藏值获取↓
from bs4 import BeautifulSoup
soup=BeautifulSoup(content,'lxml')
viewstate=soup.select('#__VIEWSTATE')[0].attrs.get('value')
viewstategenerator=soup.select('#__VIEWSTATEGENERATOR')[0].attrs.get('value')#获取两个隐藏值
#验证码获取↓
code=soup.select('#imgCode')[0].attrs.get('src')
code_url="https://so.gushiwen.cn"+code
# import urllib.request
# urllib.request.urlretrieve(url=code_url,filename='code.jpg') 此种方法无法实现功能
#使用requests里面的session方法，使网页请求变为同一个对象
session=requests.session()
response_code=session.get(code_url)#获取验证码url的内容
content_code=response_code.content#注意此时要使用二进制数据content，而非utf-8编码后的text，因为我们要使用的是图片的下载
with open('code.jpg','wb') as fp:#'wb'模式就是将二进制数据写入到文件
    fp.write(content_code)
code_name=input('验证码：')
#登录↓
data_post={
    "__VIEWSTATE":viewstate,
    "__VIEWSTATEGENERATOR":viewstategenerator,
    "from": "http://so.gushiwen.cn/user/collect.aspx",
    "email": "1271943237@qq.com",
    "pwd": "111111",
    "code":code_name,
    "denglu":""
}
response_post=session.post(url=url,headers=headers,data=data_post)#使用同一个对象session进行登录，确保验证码与本次登录匹配
content_post=response_post.text#登录后的网站源码
print(content_post)