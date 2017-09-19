class Field:
    pass


class ItemMeta(type):
    def __new__(cls, name, parents, attrs):
        new_attrs = {}
        fields = {}
        for attr in attrs:
            if isinstance(attrs[attr], Field):
                fields[attr] = True
            else:
                new_attrs[attr] = attrs[attr]
        new_attrs["_fields"] = fields
        return super(ItemMeta, cls).__new__(cls, name, parents, new_attrs)

class Item(metaclass=ItemMeta):
    _fields = {}
    _value = {}

    def __init__(self, **argv):
        #print(argv)
        for key in argv:
            if key not in self._fields:
                raise Exception("key error!")
            self._value[key] = argv[key]
    
    def __setitem__(self, key, value):
        if key not in self._fields:
            raise Exception("key error")
        self._value[key] = value
    
    def __getitem__(self, key):
        return self._value[key]

    def __str__(self):
        return str(self._value)


if __name__ == "__main__":
    class URL(Item):
        host = Field()
        path = Field()
    #u = URL()
    #u["host"] = 10
    #u["path"] = 20
    u = URL(host="www.baidu.com", path="/image")
    print(u["host"],u['path'])