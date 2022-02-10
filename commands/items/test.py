from .items import define_item, Item
from discord.ext.commands.context import Context
from discord.ext.commands import Bot


class Testo(Item):
	async def use(self, ctx:Context, bot:Bot, *args, **kwargs):
		me = ctx.author.display_name
		cont = ctx.message.content.splot(" ")
		try:
			user = int(cont[2].replace("<", "").replace(">").replace("@", ""))
			user = bot.get_user(user)
		except:
			user = None
			
				
				
		if user:
			return me + " Threw a " + self.name + " at " + user.mention
		return me + " Threw a " + self.name
		
define_item("Testo", Testo)
