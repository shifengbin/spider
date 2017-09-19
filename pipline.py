from framework.Pipline import Pipline

class MyPipLine(Pipline):
  def start_spider(self):
    self.file = open("aa.txt","w")
  
  def response(self, item):
    #print("-----------{}-----------",item)
    self.file.write(item["name"])
  
  def end_spider(self):
    self.file.close()