from abc import ABC,abstractmethod
from queue import Queue
from collections import Iterable
from threading import local
import requests

url_map  = local()
url_map.urls = {}

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
  proxy = None
  def __init__(self, url, callback):
    self.url = url
    self.callback = callback
  
  def request(self):
    try:
      if not url_map.urls.get(self.url,False):
        url_map.urls[self.url] = True
      else:
        return None
      response = requests.get(self.url, headers = self.headers, proxies=self.proxy)
      response.raise_for_status()
      print("{}:{}".format(self.url, response.status_code))
    except:
      return None
    return response

class Spider(ABC):
  start_urls = []
  url_queue = Queue()
  
  def start_request(self):
    for url in self.start_urls:
      self.url_queue.put(Request(url, callback = self.parse))

  @abstractmethod
  def parse(self, response):
    pass

  def execute(self):
    self.start_request()
    while not self.url_queue.empty():
      request = self.url_queue.get(False)
      response = request.request()
      if not response:
        continue
      result = request.callback(response)
      if not isinstance(result,Iterable):
        continue
      for req in result:
        if not isinstance(req, Request):
          pass
        self.url_queue.put(req)
        
