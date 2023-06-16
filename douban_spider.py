from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import requests
import random
import time
import sys
from lxml import etree
from retrying import retry

user_agent_= [
        # Opera
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60",
        "Opera/8.0 (Windows NT 5.1; U; en)",
        "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50",
        # Firefox
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
        "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
        # Safari
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
        # chrome
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
        # 360
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
        # 淘宝浏览器
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
        # 猎豹浏览器
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
        # QQ浏览器
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        # sogou浏览器
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)",
        # maxthon浏览器
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36",
        # UC浏览器
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36",

    #各种移动端

        # IPhone
        "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
        # IPod
        "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
        # IPAD
        "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
        "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
        # Android
        "Mozilla/5.0 (Linux; U; Android 2.2.1; zh-cn; HTC_Wildfire_A3333 Build/FRG83D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        # QQ浏览器 Android版本
        "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        # Android Opera Mobile
        "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
        # Android Pad Moto Xoom
        "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
        # BlackBerry
        "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
        # WebOS HP Touchpad
        "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
        # Nokia N97
        "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
        # Windows Phone Mango
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
        # UC浏览器
        "UCWEB7.0.2.37/28/999",
        "NOKIA5700/ UCWEB7.0.2.37/28/999",
        # UCOpenwave
        "Openwave/ UCWEB7.0.2.37/28/999",
        # UC Opera
        "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999"
    
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"     
    ]


"""
爬取豆瓣流程
1:打开浏览器，打开网页
2:点击全部地区，点击第一个地区
3:根据地区创建文件，打开文件
4:获取列表数据
5:获取详情数据
6:写入文件
7:关闭文件
8:关闭浏览器
"""
class DoubanSpider():
    def __init__(self) -> None:
        self.currentPath=sys.path[0]
        self.userAgent=random.choice(user_agent_)
      
        pass

     # todo 次数需要进行异常处理
    def getDriver(self,url):
        opt=webdriver.ChromeOptions()
        opt.add_argument('--user-agent=%s' % self.userAgent)
        opt.add_argument('--proxy-server=' + self.getReuestIpProxies())              #ip代理
        driver=webdriver.Chrome()
        driver.get(url=url)
        return driver
    
     # 获取伪装ip
    def getReuestIpProxies(self):
        ipUrle='xxx.com'
        reponse=requests.get(url=ipUrle)
        reponse.encoding='utf-8'
        ipData=json.loads(reponse.text)
        ip=''
        for row in ipData['data']:
            ip=(row['ip'])
            port=str(row['port'])
        http=ip+':'+port  
        return http
     
     # 获取内容
    def getReponse(self,url):
        proxies={
            'http':self.getReuestIpProxies()
        }
        header={
             'User-Agent':self.userAgent
        }
        reponse=requests.get(url=url,headers=header,proxies=proxies)
        reponse.encoding='utf-8'
        content=reponse.text
        return content 
  
    def getCates(self):
        driver=self.driver
        # 点击全部分类
        allCatesButtonEle=WebDriverWait(driver=driver,timeout=10).until(
            EC.presence_of_element_located((By.XPATH,'//*[@id="app"]/div/div[1]/div/div[1]/div[2]/div/div[1]/span'))
        )
        time.sleep(1)
        allCatesButtonEle.click()
        time.sleep(random.randint(2,6))
        #点击获取第一个分类  
        cateButtonEle=driver.find_element(By.XPATH,self.cateEleStr)
        time.sleep(random.randint(5,10))
        cateButtonEle.click()
        # 开始获取列表数据
        self.getListContent()
        pass
    
    def writeTxt(self,cate,val):
        path=self.currentPath+'\\tv_data\\'+cate+'.txt'
        with open(path,'+a',encoding='utf-8') as f:
            self.f=f
            f.write(repr(val)+'\n')
        pass

    def getListContent(self):
        time.sleep(random.randint(10,17))
        driver=self.driver
        js="var q=document.documentElement.scrollTop=100000"  
        cateEle=driver.find_element(By.XPATH,'//*[@id="app"]/div/div[1]/div/div[1]/div[2]/div/div/span')
        currentCate=cateEle.text
        try:
            index=1
            while index < self.totalPage:
                # 先下拉到最底部
                driver.execute_script(js)  
                data=self.getListData(driver)   
                for row in data:
                    self.writeTxt(currentCate,row)                 #数据写入文件
                moreButton=WebDriverWait(driver=driver,timeout=5).until(
                    EC.presence_of_element_located((By.XPATH,'//*[@id="app"]/div/div[2]/div/button'))
                )  
                moreButton.click()  
                index+=1
                self.f.close()
                pass
            pass
        finally:
            driver.close()
        pass

    def getListData(self,driver):
        titlesEleArr=driver.find_elements(By.XPATH,'//*[@id="app"]/div/div[2]/ul/li/a/div/div[2]/div/div[1]/span')
        listImgEleArr=WebDriverWait(driver=driver,timeout=10).until(
            EC.presence_of_all_elements_located((By.XPATH,'//*[@id="app"]/div/div[2]/ul/li/a/div/div[1]/div/img'))
        )  
        infoUrlsEleArr=driver.find_elements(By.XPATH,'//*[@id="app"]/div/div[2]/ul/li/a')
        listImgEleArr=listImgEleArr[-20:]
        infoUrlsEleArr=infoUrlsEleArr[-20:]
        for index in range(len(titlesEleArr[-20:])):
            titleStr=titlesEleArr[index].text
            listImg=listImgEleArr[index].get_attribute('src')
            infoUrl=infoUrlsEleArr[index].get_attribute('href')
            infoId=infoUrl.replace('https://www.douban.com/doubanapp/dispatch?uri=/tv/','')
            infoData=self.getInfoData(infoId)
            val={
                'title':titleStr,
                'img':listImg,
                'info_url':infoUrl,
                'info_id':infoId,
                'director':infoData['director'],
                'actors':infoData['actors'],
                'type':infoData['type'],
                'area':infoData['area'],
                'years':infoData['years'],
                'language':infoData['language'],
                'episodes':infoData['episodes'],
                'dec':infoData['dec'],
                }
            yield val
        pass

    def getInfoData(self,infoId):
        url='https://movie.douban.com/subject/{}/'.format(infoId)
        time.sleep(random.randint(10,15))
        content=self.getReponse(url)
        html=etree.HTML(content)
        directorArr=html.xpath('//*[@id="info"]/span[1]/span[2]/a/text()')
        actorsArr=html.xpath('//*[@id="info"]/span[3]/span[2]/a/text()')
        actors='/'.join(actorsArr)
        typeArr=html.xpath('//*[@id="info"]/span[@property="v:genre"]/text()')
        typeStr=','.join(typeArr)
        areaArr=html.xpath('//span[contains(./text(), "制片国家/地区:")]/following::text()[1]')
        languageArr=html.xpath('//span[contains(./text(), "语言:")]/following::text()[1]')
        episodesNumArr=html.xpath('//span[contains(./text(), "集数:")]/following::text()[1]')
        decArr=html.xpath('//*[@id="link-report-intra"]/span/text()')[0].replace(' ','').replace('\u3000','').replace('\n','')
        yearsArr=html.xpath('//*[@id="info"]/span[@property="v:initialReleaseDate"]/text()')
        val={
            'director':directorArr[0],
            'actors':actors,
            'type':typeStr,
            'area':areaArr[0],
            'years':yearsArr[0],
            'language':languageArr[0],
            'episodes':episodesNumArr[0],
            'dec':decArr
            }
        return val
    
    def run(self,totalPage,cateEleStr):
        self.cateEleStr=cateEleStr      #当前分类元素的xpath
        self.totalPage=totalPage
        url='https://movie.douban.com/tv/'
        self.driver=self.getDriver(url)
        self.getCates()
        pass


@retry(stop_max_attempt_number=2)                 #报错重试
def main():
    spider=DoubanSpider()
    cateEleStr='//*[@id="app"]/div/div[1]/div/div[1]/div[2]/div/div[2]/div/div/ul/li[4]/span/span'
    spider.run(50,cateEleStr)    


if __name__=="__main__":
    main()

