from humanize import intcomma

items = {}

def define_item(name, cls):
	items[name] = cls
	
def construct(item):
	if "cls" in item.keys():
		if item["cls"] in items.keys():
			return items[item["cls"]](item)
	return Item(item)

class Item():
	def __init__(self, data, name="item", value=0, cls = "item"):
		self.data = data
		if "name" not in self.data.keys():
			self.data["name"] = name
		if "value" not in self.data.keys():
			self.data["value"] = value
		if "cls" not in self.data.keys():
			self.data["cls"] = "item"
			
		self.cls = self.data["cls"]
		self.name = self.data["name"]
		self.value = self.data["value"]
		
	def __getitem__(self, index):
		try:
			return self.data[index]
		except:
			return None
		
	@property
	def sell_price(self):
		return int(self.value * 0.9)
		
	@property
	def val_str(self):
		return f"¥{intcomma(self.value)}"
		
	@property
	def sell_str(self):
		return f"¥{intcomma(self.sell_price)}"
		
	def __str__(self):
		return f"{self.cls}: {self.name} - {self.val_str}"
		
	async def use(self, ctx:Context, bot:Bot, *args, **kwargs):
		return f"used {self.name} ✓"
		