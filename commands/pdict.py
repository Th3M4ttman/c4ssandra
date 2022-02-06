from collections import UserDict
import os
import json
from copy import deepcopy
root = "/".join(__file__.split("/")[0:-1])

class pdict(dict):
	
	def __init__(self, file, defaults = {}, ctx = __file__):
		super().__setattr__("ctx", ctx)
		super().__setattr__("data", dict(file=file))
		super().__setattr__("defaults", defaults)
		self.load()
		
		
	def load(self, *args, **kwargs):
		for k, i in self.defaults.items():
				self.data[k]= i
		if os.path.exists(root+self.data["file"]):
			with open(root+self.data["file"]) as f:
				data = json.loads("".join(f.readlines()))
			for k, i in data.items():
				self.data[k]= i
		else:
			self.save()
			return self.load()
			
		if len(args) == 0 and len(kwargs) == 0:
			return self
		return self(*args, **kwargs)
		
	
	def save(self):
		with open(self.data["file"], "w") as f:
			f.write(json.dumps(super().__getattribute__("data"), indent=4))
	
	@property
	def path(self):
		
		if self["file"].count(".") <= 1:
			p = self["file"]
			if p.count("/") == 0:
				p = "/" + p
		else:
			p = ".".join(self["file"].split(".")[1:])
		
		#f len(self.ctx)
		return "/".join(self.ctx.split("/")[:-1]) + p
		
		
	def __getitem__(self, key):
		if key not in super().__getattribute__("data").keys():
			return self.__missing__(key)
		return super().__getattribute__("data")[key]
	
	def __setitem__(self, key, value):
		self.data[key] = value
		self.save()
		return self.data[key]
		
		
	def __getattr__(self, name):
		if name in self.__dict__.keys():
			return self.__dict__[name]
		if name in self.data.keys():
			return self.data[name]
		return super().__getattribute__(name)
	
	def __setattr__(self, name, value):
		try:
			x = super().__getattribute__(name)
			super().__setattr__(name, value)
			return super().__getattribute__(name)
		except Exception as e:
			#print(e)
			self[name] = value
			return self.data[name]
			
	def clear(self):
		os.remove(self.path)
		self.data = dict(file=self["file"], **self.defaults)
		self.load()
		
	def __missing__(self, x):
		for _x in [x, x.title(), x.lower(), x.upper()]:
			
			try:
				return self.defaults[_x]
			except:
				pass
		return None
	
	def __str__(self):
		return f"{self.__class__.__name__}: " + json.dumps(self.data, indent=4)
		
	def __repr__(self):
		return str(self.data)
		
	def __call__(self, *args, **kwargs):
		for key, item in kwargs.items():
			self.data[key] = item
		if len(kwargs) > 0:
			self.save()
			
		out = []
		for arg in args:
			out.append(self[str(arg)])
			
		
		if len(out) == 1:
			return out[0]
		if len(out) == 0:
			return self
		return out
		



