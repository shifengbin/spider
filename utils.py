import hashlib

from threading import Lock

_url_map = {}
_url_lock = Lock()

def md5( data:str ) ->str:
    m = hashlib.md5()
    m.update(data)
    return m.hexdigest()


def addURLToMap(url:str) ->bool:
    '''
    如果存在返回True，如果不存在返回False
    '''
    global _url_lock
    key = md5(url)
    _url_lock.aquire()
    ret = _url_lock.get(key,False)
    _url_lock[key] = True
    _url_lock.release()
    return ret



