from selenium import webdriver
from selenium.webdriver.chrome.options import Options
def share_browser():#使用chromehandless时固定配置（除了path需要自己设置），所以封装成函数
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'#path是chrome浏览器的路径
    chrome_options.binary_location = path
    browser = webdriver.Chrome(chrome_options=chrome_options)
    return browser