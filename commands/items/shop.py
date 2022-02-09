
from .items import *
from copy import deepcopy
from datetime import datetime

class Shop():
	def __init__(self, items=[]):
		self.items = items
		
	def add_item(self, item):
		self.items.append(item)
		
	def get(self, item):
		if type(item) == int:
			return self.items[item]
		elif type(item) == str:
			for i in self.items:
				if i.name.lower() == item.lower():
					return i
	
	def construct(self, item):
		if not self.get(item):
			return
		
		out = deepcopy(self.get(item))
		out.data["created"] = str(datetime.now())
		return out
		
		
	def __str__(self):
		out = "Welcome to the shop! What would you like to buy?" if len(self.items) >= 1 else "Sorry, Closed for business."
		for i, item in enumerate(self.items):
			out += f"\n\t{i}: {item.name} - {item.val_str}"
		return out

"""

SHOP = Shop()
poo = construct({"name":"poo", "value":5, "cls":"Testo"})
superpoo = construct({"name":"superpoo", "value":50, "cls":"Testo"})

SHOP.add_item(poo)
SHOP.add_item(superpoo)


x = SHOP.construct(0)
print(x.data)
print(x)
print(x.use())
"""
