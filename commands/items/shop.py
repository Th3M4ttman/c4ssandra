
from .items import *
from copy import deepcopy
from datetime import datetime

class Shop():
	def __init__(self, items=[], special=[]):
		self.items = items
		self.special = special
		
	def add_item(self, item):
		self.items.append(item)
		
	def add_special(self, item):
		self.special.append(item)
		
	def get(self, item):
		if type(item) == int:
			return self.items[item]
		elif type(item) == str:
			for i in self.items:
				if i.name.lower() == item.lower():
					return i
					
	def getspecial(self, item):
		if type(item) == int:
			return self.items[item]
		elif type(item) == str:
			for i in self.items:
				if i.name.lower() == item.lower():
					return i
	
	def construct(self, item):
		if not self.get(item):
			if not self.getspecial(item):
				return
			else:
				out = deepcopy(self.getspecial(item))
				out.data["created"] = str(datetime.now())
				return out
		
		out = deepcopy(self.get(item))
		out.data["created"] = str(datetime.now())
		return out
		
		
	def __str__(self):
		out = "Welcome to the shop! What would you like to buy?" if len(self.items) >= 1 else "Sorry, Closed for business."
		for i, item in enumerate(self.items):
			out += f"\n\t{i}: {item.name} - {item.val_str}"
		return out

SHOP = Shop()

poo = construct({"name":"poo", "value":5, "cls":"Testo"})
superpoo = construct({"name":"superpoo", "value":50, "cls":"Testo"})

SHOP.add_item(poo)
SHOP.add_item(superpoo)

scryst = construct({"name":"Small EXP Crystal", "value":50, "cls":"Crystal", "exp":100})
lcryst = construct({"name":"Large EXP Crystal", "value":500, "cls":"Crystal", "exp":1000})
hcryst = construct({"name":"Huge EXP Crystal", "value":4000, "cls":"Crystal", "exp":10000})

SHOP.add_item(scryst)
SHOP.add_item(lcryst)
SHOP.add_item(hcryst)
pass1 = construct({"name":"1 day Lounge Pass", "value":200, "cls":"Pass", "length":1})
pass7 = construct({"name":"7 day Lounge Pass", "value":1000, "cls":"Pass", "length":7})
pass30 = construct({"name":"30 day Lounge Pass", "value":1500, "cls":"Pass", "length":30})

SHOP.add_item(pass1)
SHOP.add_item(pass7)
SHOP.add_item(pass30)

"""
x = SHOP.construct(1)
x.value *= 0.9
print(SHOP)
"""
