from .pdict import pdict
import json
import  humanize
from . import ROOT

class Item():
	def __init__(self, data:dict, itemstore=None):
		self.name = list(data.keys())[0]
		if itemstore is None:
			global IS
			itemstore = IS
		
		
		self.data = data[self.name]
		self.value = self.data["value"]
		
	def to_dict(self):
		return {self.name: self.data}
	
	
	def use(self, user):
		print("Used", self.name)
		user.remove_item(self)
				
	
	def __str__(self):
		return self.name
		
	def __repr__(self):
		return str(self)
	

class User():
	def __init__(self, id, gbp=0, inventory=[], exp=0, data = None, users = None):
		self.users = users
		if data:
			gbp = data["gbp"]
			inventory = data["inventory"]
			exp = data["exp"]
			
		self.id = id
		self.gbp = gbp
		self._inventory = inventory
		self.exp = exp
		
	@property
	def inventory(self):
		global IS
		out = []
		for i, item in enumerate(self._inventory):
			name = list(item.keys())[0]
			item = IS.buy(name)
			out.append(item)
		return out
	
	def to_json(self):
		self.update_inventory()
		return {"gbp":self.gbp, "inventory":self._inventory, "exp":self.exp}
	
	def __str__(self):
		return f"{self.id}: {json.dumps(self.to_json(), indent=4)}"
		
	def add_item(self, item):
		if type(item) == Item or issubclass(item.__class__, Item):
			self._inventory.append(item.to_dict())
			self.update_inventory()
	
	def remove_item(self, item):
		if type(item) == Item or issubclass(item.__class__, Item):
			for i, it in enumerate(self.inventory):
				if it.data == item.data:
					self._inventory.pop(i)
					self.update()
					break
			return
		self.inventory.pop(item)
		self.update()
		
	def buy(self, item, itemstore=None):
		if itemstore is None:
			global IS
			itemstore = IS
		
		i = itemstore.buy(item)
		if self.gbp >= i.value:
			self.give_gbp(-i.value)
		else:
			print("Insufficient Funds")
			return
		self.add_item(i)
		self.update()
		return i
		
	def update_inventory(self):
		out = []
		for item in self.inventory:
			out.append(item.to_dict())
		self._inventory = out
		
		
	def update(self):
		self.users.update_user(self)
		
	def give_gbp(self, amount):
		self.gbp += amount
		self.update()
	
		
			
			

class UserStore(pdict):
	def __init__(self, file, defaults={"users":{}}):
		super().__init__(file, defaults, ctx=__file__)
		
	@property
	def users(self):
		if self.data["users"] is None:
			self.users = dict()
		
		out = {}
		for id, user in self.data["users"].items():
			out[id] = User(id, user["gbp"], user["inventory"], user["exp"])
		return out
		
	def update_user(self, user:User):
		users = self.users
		if str(user.id) in users.keys():
			users[user.id] = user.to_json()
		else:
			raise ValueError("User doesnt exist")
		self.users = users
		self.save()
		
		
	def add_user(self, user:User):
		users = self.users
		if str(user.id) in users.keys():
			raise ValueError("User already exists")
		if type(user) == int:
			users[str(id)] = User(id).to_json()
		else:
			users[str(user.id)] = user.to_json()
		self.users = users
		self.save()
		
	def del_user(self, user:str):
		user = str(user)
		if user in self.users.keys():
			self["users"].pop(user)
		self.save()
	
	@users.setter
	def users(self, value):
		self.data["users"] = value
		self.save()
		
	def get_user(self, id):
		try:
			for i, user in self.data["users"].items():
				if i == id:
					return User(str(id), data=user, users=self)
		except:
			pass
		return None

class ItemStore():
	def __init__(self, *items):
		self.items = items
		
	def buy(self, item:Item):
		if type(item) == int:
			return self.items[item]()
		if type(item) == str:
			for i in self.items:
				if i().name == item:
					return i()
		
		
	
	def __str__(self):
		out = "Welcome to the shop! What would you like to buy?\n\n"
		for i, item in enumerate(self.items):
			
			out += f"{i} : {item().name} - ¥{item().value}"
		return out

class sod(Item):
	def __init__(self):
		super().__init__({"Sword of Damacles":{"value":69}})
		
	def use(self, user):
		user.give_gbp(99999)
		super().use(user)
		



US = UserStore("/users/users.json")
IS = ItemStore(sod)
"""
#y = User(0, 69, [], 420)
#x.add_user(y)
print(IS)
#print(x.get_user(0).inventory)
y = US.get_user(0)
for i in y.inventory:
	i.use(y)

#y.give_gbp(69420)
#y.buy("Sword of Damacles")
#y.add_item()
print(y)
#interp(locals(), globals())
"""
from .bot import cassandra, bs
from discord.ext.commands import Context

@cassandra.command(name="gbp")
async def gbp(ctx:Context, action=None):
	user = US.get_user(ctx.author.id)
	print("User=", user)
	await bs(ctx)
	if user is None:
		US.add_user(User(int(ctx.author.id)))
		user = US.get_user(ctx.author.id)
		
	if action == None:
		dn = ctx.message.author.display_name
		msg = f"Good Boy Points:\n\t{dn}: ¥{humanize.intcomma(user.gbp)}"
		await ctx.message.channel.send(msg)
		
	
@cassandra.command(name="users")
async def users(ctx):
	await ctx.message.channel.send(str(US))