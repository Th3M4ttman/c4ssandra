import discord
import json
import humanize

def save(users):
	with open("users.json", "w") as f:
		f.write(json.dumps(users, indent=4, cls=CUencoder))

def load():
	with open("users.json") as f:
		_u = json.loads("".join(f.readlines()))
	for k, i in _u.items():
		_u[k] = CassUser(k)
		_u[k].from_str(i)
	return _u
		
from json import JSONEncoder

class CassUser():
	def __init__(self, id, inventory=[], gbp =0):
		self.id = id
		self.inventory = list(inventory)
		self.gbp = gbp
	
	def __iter__(self):
		yield from {"id": self.id,
		"inventory": [item.data for item in self.inventory],
		"gbp": self.gbp}.items()
	
	def __str__(self):
		return f"{self.id}"
		
	def __repr__(self):
		return str(self)
	
	def to_json(self):
		return json.dumps(dict(self), ensure_ascii=False)
	
	def from_str(self, str):
		self.__dict__ = json.loads(str)
	
	def use(self, item, ctx):
		found = False
		for i in self.inventory:
			if i.data["name"] == item:
				item = i
				found = True
				break
		if found:
			return item.use(ctx, self)
			
class CUencoder(JSONEncoder):
	def default(self, o:CassUser):
		return o.to_json()
		
templates = {}
def Use(self, ctx, user):
	try:
		return f"{user.name} Used {self.data['name']}"
	except:
		return ""
	
class Item():
	def __init__(self, data = {"name":"item",
												"value":0,}, use=Use):
		self.data = data
		self._use = use
	
	def use(self, ctx, user):
		return self._use(self, ctx, user)
			
	def sell(self):
		print("Sold", self.data["name"], "for ¥"+humanize.intcomma(self.data["value"]))
	
	def __str__(self):
		return f"{self.data['name']}"
	
	def __repr__(self):
		return str(self)
			

class ItemTemplate():
	def __init__(self, shop, name, price, use):
		self.name = name
		self.price = price
		self.shop = shop
		shop.add_item(self)
		self.use = use
		templates[name] = self
		
	def buy(self, user:CassUser):
		print("Bought for ¥", humanize.intcomma(self.price), sep="")
		if user.gbp >= self.price:
			i = Item({"name":self.name, "value":self.price}, use=self.use)
			user.inventory.append(i)
			user.gbp -= self.price
		else:
			print("Insufficient Funds")
			i = Item()
			
		return i
		
			
class Shop():
	def __init__(self):
		self.welcome = "Welcome to the shop! What would you like to buy?"
		self.items = []
		
	@property
	def name_price(self):
		return [[item.name, item.price] for item in self.items]
	
	def add_item(self, item):
		if item not in self.items:
			self.items.append(item)
	
	def add_items(self, *items):
		for item in items:
			self.add_item(item)
			
	def buy(self, item, user:CassUser):
		if type(item) == int:
			item = self.items[item]
		else:
			found = False
			i = 0
			for name, _ in self.name_price:
				print(name, item)
				if name.lower() == item.lower():
					item = self.items[i]
					found = True
					break
				i += 1
			if found == False:
				print("Not Found")
				return
		
		return item.buy(user)
	
	def __str__(self):
		out = self.welcome + "\n\n"
		i = 1
		for name, price in self.name_price:
			out += f"{i}: {name} - ¥{humanize.intcomma(price)}"
			i += 1
		if i == 1:
			return "Sorry Closed For Renovation"
		return out
	
def Sod_use(self, ctx, user):
	i = user.inventory.index(self)
	user.inventory.pop(i)
	return "killed people"

"""
u = CassUser(69)
print(u)
users = {0:u.to_json()}
save(users)
"""

users = load()
u = users["0"]


print(users)
shop = Shop()
Sod = ItemTemplate(shop, "Sword of Damocles", 69420, use=Sod_use)

print(shop)

u.gbp = 999999
print(u.gbp)
#x = Sod.buy(u)
#print(u.gbp)
print("inventory:", u.inventory)
y = shop.buy("Sword of Damocles", u)

#print(y)
print(u.gbp)
print("inventory:", u.inventory)

"""
for item in u.inventory:
	x = item.use(None, u)
	print(x)
	print("inventory:", u.inventory)
"""
#print(u.use("Sword of Damocles", None))

save(users)
