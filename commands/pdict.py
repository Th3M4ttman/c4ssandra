from collections import UserDict
import os
import json
from copy import deepcopy
root = "/".join(__file__.split("/")[0:-1])

class pdict():
	
	def __init__(self, file, defaults = {}, ctx = __file__):
		self.ctx = ctx
		self.data = dict(file=file)
		self.defaults = defaults
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
			f.write(json.dumps(self.data, indent=4))
	
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
		return self.data[key]
	
	def __setitem__(self, key, value):
		self.data[key] = value
		self.save()
		return self.data[key]
	
	"""
		
	def __getattr__(self, name):
		return super().__getattribute__(name)
	
	def __setattr__(self, name, value):
		try:
			if name in ("data", "ctx", "defaults"):
				super().__setattr__(name, value)
			else:
				raise ValueError("Nah")
			super().__getattribute__(name)
		except Exception as e:
			#print(e)
			self[name] = value
	"""
			
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
		



