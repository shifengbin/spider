from abc import ABC,abstractmethod
from queue import Queue
from collections import Iterable
from threading import local
from .utils import addURLToMap
from .Pipline  import Pipline
from .Items import Item
import requests

from  .logger import logger

_url_queue = Queue()


def isAbsoluteURL(url):
  if url.startswith("http:") or url.startswith("https:"):
    return True
  return False

def formatURL(url, host):
  if isAbsoluteURL(url):
    return url
  else:
    if url.startswith("/") or host.endswith("/"):
      return host+url
    return host+"/"+url

def formatURLs(urls, host):
  return [ formatURL(url, host) for url in urls]

class Request:
  headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36",
  }
  
  def __init__(self, url, callback, proxy = None):
    self.url = url
    self.callback = callback
    self.proxy = proxy
  
  def request(self):
    try:
      ret = addURLToMap(self.url)
      if ret:
        logger.info("{} has been saved".format(self.url))
        return None
      response = requests.get(self.url, headers = self.headers, proxies=self.proxy)
      response.raise_for_status()
      logger.info("{}:{}".format(self.url, response.status_code))
    except Exception as e:
      logger.error("request error:{}".format(str(e)))
      return None
    return response

class Spider(ABC):
  start_urls = []
  

  def __init__(self,pipline = None):
    global _url_queue

    if pipline and isinstance(pipline,Pipline):
      self.pipline = pipline
    else :
      self.pipline = None
      
    self.url_queue = _url_queue
  
  def start_request(self):
    for url in self.start_urls:
      self.url_queue.put(Request(url, callback = self.parse))

  @abstractmethod
  def parse(self, response):
    pass

  def execute(self):
    self.start_request()
    logger.info("add start url finished!")
    if self.pipline:
      self.pipline.start_spider()
    while not self.url_queue.empty():
      request = self.url_queue.get(False)
      response = request.request()
      if not response:
        continue
      result = request.callback(response)

      if not isinstance(result,Iterable):
        continue
      for req in result:
        if isinstance(req, Item) and self.pipline:
          self.pipline.response(req)
          continue
        if isinstance(req, Request):
          self.url_queue.put(req)
    if self.pipline:
      self.pipline.end_spider()
    logger.info("spider finished!")
        
