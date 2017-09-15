from BaseSpider import Spider ,Request
from lxml import etree
class MySpider(Spider):
  start_urls = ["http://www.wmpic.me/"]
  def parse(self, response):
    host = "http://www.wmpic.me"
    dom = etree.HTML(response.text)
    urls = dom.xpath("//div[@class='div_cam']//a/@href")
    urls = [host+url for url in urls]
    for url in urls:
      yield Request(url, callback=self.parseImg)
    

  def parseImg(self,response):
    dom = etree.HTML(response.text)
    urls = dom.xpath("//div[@class='post']//img/@src")
    for url in urls:
      yield Request(url,callback=self.saveImg)

  def saveImg(self,response):
    filename = response.url.split("/")[-1]
    with open(filename,"wb") as f:
      f.write(response.content)

if __name__ == "__main__":
  spider = MySpider()
  spider.execute()