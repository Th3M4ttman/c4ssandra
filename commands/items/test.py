from .items import define_item, Item



class Testo(Item):
	def use(self):
		return "hell yeah"
define_item("Testo", Testo)
