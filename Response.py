from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from my_fake_useragent import UserAgent
import requests
import json
import time


# 通过webdriver获取页面内容

def getDrivertDriverByWebdriver(url):
    opt=webdriver.ChromeOptions()
    # 请求头伪装
    opt.add_argument('--user-agent=%s' % UserAgent().random())
    # 已开发者模式启动浏览器
    opt.add_experimental_option('excludeSwitches',['enable-automation'])
     # 屏蔽保存密码提示框
    prefs={'credentials_enable_service':False,'profile.password_manager_enabled':False}
    opt.add_experimental_option('prefs',prefs)
    # 反爬虫特征处理
    opt.add_argument('--disable-blink-features=AutomationControlled')
     #ip代理
    opt.add_argument('--proxy-server={}'.format(getReuestIpProxies()))  
    driver=webdriver.Chrome(options=opt)
    # 浏览器最大化
    driver.maximize_window()
    driver.get(url=url)
    WebDriverWait(driver=driver,timeout=25)
    
    return driver


# 通过requests库获取页面内容
def getHtmlContentByRequests(url):
    proxies={
        'http':'http://'+getReuestIpProxies()
    }
    header={
        'User-Agent':UserAgent().random
    }
    reponse=requests.get(url=url,headers=header,proxies=proxies)
    reponse.encoding='utf-8'
    content=reponse.text
    return content


# ip代理
def getReuestIpProxies():
    ipUrle='https://api.xxx.com:8522/api/getIpEncrypt?dataType=0&encryptParam=SlDyzgfgDW12vuaMHmQkM1l3svlLMXCHw0IlSHvOue3lVhShpdEjb9vG2YRiwpyEuRVyxit%2BS%2BLPfM1vGfsJ7mEjAi0eMq%2Ft61ylMNCQgciuTUwZah7tVApJ9%2B8FOZYiAyw%2B0Hk2DtMscqY%2B%2FhM%2BdDz2krSwDgva62WETzjyvF7YFsJvJYxeLU9YDql4IJq6vs3ERyFHZ9FAgNS8WBDIMt0Jv%2FQlqwlcd4gkrYI6AFg%3D'
    reponse=requests.get(url=ipUrle)
    reponse.encoding='gb2312'
    ipData=json.loads(reponse.text)
    ip=''
    for row in ipData['data']:
        ip=(row['ip'])
        port=str(row['port'])
    http=ip+':'+port  
    return http


