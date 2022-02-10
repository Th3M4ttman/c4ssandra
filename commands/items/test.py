from .items import define_item, Item
from discord.ext.commands.context import Context
from discord.ext.commands import Bot


class Testo(Item):
	async def use(self, ctx:Context, bot:Bot, *args, **kwargs):
		me = ctx.author.display_name
		
		try:
			user = ctx.message.mentions[0].mention
		except:
			user = None
			
				
		if user:
			return me + " Threw a " + self.name + " at " + user.mention
		return me + " Threw a " + self.name
		
define_item("Testo", Testo)
