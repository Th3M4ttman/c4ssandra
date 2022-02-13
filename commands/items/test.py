from .items import define_item, Item
from discord.ext.commands.context import Context
from discord.ext.commands import Bot
from humanize import intcomma
from asyncio import sleep
import datetime
import discord
	

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

class LoungePass(Item):
	@property
	def length(self):
		if "length" in self.data.keys():
			return self.data["length"]
		return 1
		
	async def use(self, ctx:Context, bot:Bot,  user, *args, **kwargs):
		me = bot.get_user(user.discord).display_name
		msg = f"{me} activated their {self.name}"
		
		if "expiry" in user.stats.keys():
			e = datetime.datetime.fromtimestamp(user.stats["expiry"])
			if datetime.datetime.now() < e:
				user.stats["expiry"] = (e + datetime.timedelta(days=self.length)).timestamp()
				msg += " extending their membership"
			else:
				user.stats["expiry"] = (datetime.datetime.now() + datetime.timedelta(days=self.length)).timestamp()
		else:
			user.stats["expiry"] = (datetime.datetime.now() + datetime.timedelta(days=self.length)).timestamp()
		user.update()
		lounge_role = discord.utils.get(ctx.guild.roles, name = "lounge")
		
		for m in ctx.guild.members:
			if m.id == user.discord:
				m.add_roles(lounge_role)
		return True, msg

define_item("Pass", LoungePass)
define_item("Crystal", Crystal)
define_item("Testo", Testo)
