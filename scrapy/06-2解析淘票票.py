import urllib.request
url="https://dianying.taobao.com/showAction.json?_ksTS=1696476273498_64&jsoncallback=jsonp65&action=showAction&n_s=new&event_submit_doGetSoon=true"
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.69',
    'Cookie':'t=35b7b043a3c553174a6c959e5974660e; cookie2=1e08da99d3c1bd50d02c20da66251c8d; v=0; _tb_token_=e776156efe1f; cna=Y9aZHfungmUCAXOcjEcqbZ6a; xlly_s=1; tfstk=dH92n69P4xHqNM05GsWwYbZ8zgXAC93IQd_1jhxGcZbmWI6w_nTV1EtG5O8w7F7fsqBXQUWvFIw1lqBwje6ZR2MIdnKA6O0IRai2DnnbyQHxdvtvDs-S30HIDIiyfTb1l5lza1MJYavjvf01zTxczR-vUif4MnbzIRvyisWwFPIlBgv9gPVNigIPR0oyqfHE4; l=fBNsBq5nPE6FJ4UvKOfaFurza77OSIRYYuPzaNbMi9fP9C1B5leOW1HEueL6C3GVFsIkR3-P4wWWBeYBq7VonxvTaxom40kmndLHR35..; isg=BDMz5_7wUsRdXR4Q-Teus1-WwjddaMcqGryW3OXQj9KJ5FOGbThXepHynhQKwR8i',
    'Referer':'https://dianying.taobao.com/'
}
request=urllib.request.Request(url=url,headers=headers)
response=urllib.request.urlopen(request)
content=response.read().decode('utf8')
#去除开头的”jsonp65(“以及结尾的“);”
content=content.split("(")[1]#按(切片，取第二个元素，第一个元素是jsonp65
content=content.split(')')[0]#再按)切片，取第一个元素，第二个元素是;
with open('json_path.json',"w",encoding='utf-8') as fp:
    fp.write(content)#因为jsonpath只能解析本地文件，所以要把content写入
#按CTRL+alt+l可以快速把内容变成json格式（无需选中）
import json,jsonpath
obj=json.load(open("json_path.json","r",encoding='utf-8'))
show_name=jsonpath.jsonpath(obj,"$..showName")#读取所有的电源名称
print(show_name)