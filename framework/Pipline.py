from abc import ABC,abstractmethod
class Pipline(ABC):
  def start_spider(self):
    pass
  
  @abstractmethod
  def response(self, item):
    pass
  
  def end_spider(self):
    pass