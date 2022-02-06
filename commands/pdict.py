from collections import UserDict
import os
import json
from copy import deepcopy
root = "/".join(__file__.split("/")[0:-1])

class pdict():
	
	def __init__(self, file, defaults = {}, ctx = __file__):
		self.ctx = ctx
		self.data = dict()
		self.file = file
		self.defaults = defaults
		self.load()
		
		
	def load(self, *args, **kwargs):
		for k, i in self.defaults.items():
				self.data[k]= i
		if os.path.exists(self.path):
			with open(self.path) as f:
				data = json.loads("".join(f.readlines()))
			for k, i in data.items():
				self.data[k]= i
		else:
			print(self.path, "doesnt exist, creating...")
			self.save()
			return self.load()
			
		if len(args) == 0 and len(kwargs) == 0:
			return self
		return self(*args, **kwargs)
		
	
	def save(self):
		with open(self.path, "w") as f:
			f.write(json.dumps(self.data , indent=4))
	
	@property
	def path(self):
		return root + self.file
		
	
	def __getitem__(self, key):
		return self.data[key]
	
	def __setitem__(self, key, value):
		self.data[key] = value
		return self.data[key]
	
	def clear(self):
		os.remove(self.path)
		self.data = dict(file=self["file"], **self.defaults)
		self.load()
		
	
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
		
