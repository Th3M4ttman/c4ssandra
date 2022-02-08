
from items import *
import test

x = construct({"name":"testitem", "value":69420})
y = construct({"name":"Testo", "value":69420, "class": "Testo"})

x.use()
print(x.data)
y.use()
print(y.data)