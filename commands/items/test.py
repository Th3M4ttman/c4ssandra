from .items import define_item, Item
from discord.ext.commands.context import Context
from discord.ext.commands import Bot
from humanize import intcomma
from asyncio import sleep
	

class Testo(Item):
	async def use(self, ctx:Context, bot:Bot, *args, **kwargs):
		me = ctx.author.display_name
		
		try:
			user = ctx.message.mentions[0]
		except:
			user = None
			
				
		if user:
			return True, me + " Threw a " + self.name + " at " + user.mention
		return True, me + " Threw a " + self.name

class Crystal(Item):
	async def use(self, ctx:Context, bot:Bot,  user, *args, **kwargs):
		if "exp" in self.data.keys():
			exp = self.data["exp"]
		else:
			exp = 10
		
		await bot.cogs["LevelCog"].add_exp(user.discord, exp, ctx.channel, a=True)
		#print("Crystal Added", exp, "Exp")
		me = bot.get_user(user.discord).display_name
		return True, f"{me} crushes a {self.name} in their hand, gaining {intcomma(exp)} exp"


define_item("Crystal", Crystal)
define_item("Testo", Testo)
