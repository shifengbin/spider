from framework.BaseSpider import Spider ,Request,formatURLs
from lxml import etree
import os

class MySpider(Spider):
  start_urls = ["http://www.wmpic.me/"]
  host = "http://www.wmpic.me"
  def parse(self, response):
    '''
    获取图片分类
    '''
    dom = etree.HTML(response.text)
    urls = dom.xpath("//div[@class='div_cam']//a/@href")
    urls = formatURLs(urls, self.host)
    for url in urls:
      yield Request(url, callback=self.parseCategory)
    

  def parseCategory(self,response):
    '''
    获取分页和详情页
    '''
    dom = etree.HTML(response.text)
    urls = dom.xpath("//li[@class='item_box']//a/@href")
    urls = formatURLs(urls, self.host)
    pages = dom.xpath("//div[@class='wp-pagenavi']//a/@href")
    pages = formatURLs(pages, self.host)
    for url in urls:
      yield Request(url,callback=self.parsePage)
    
    for page in pages:
      yield Request(page, callback=self.parseCategory)

  def parsePage(self, response):
    '''
    获取图片URL
    '''
    dom = etree.HTML(response.text)
    imgUrls = dom.xpath("//center//img/@src")
    imgUrls = formatURLs(imgUrls, self.host)
    for url in imgUrls:
      yield Request(url, callback=self.saveImg)

  def saveImg(self,response):
    '''
    保存图片
    '''
    if not os.path.exists("./img"):
      os.mkdir("img")

    filename = "./img/"+response.url.split("/")[-1]

    with open(filename,"wb") as f:
      f.write(response.content)

if __name__ == "__main__":
  spider = MySpider()
  spider.execute()