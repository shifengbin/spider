from framework.BaseSpider import Spider ,Request,formatURLs
from lxml import etree
from pipline import MyPipLine
from item import MyItem
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
    yield MyItem(name="asdf")

if __name__ == "__main__":
  pipline = MyPipLine()
  spider = MySpider(pipline)
  spider.execute()