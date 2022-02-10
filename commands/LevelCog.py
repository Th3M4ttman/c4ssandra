from discord.ext import commands
from .levels import CUser, get_level, update
from .bot import cassandra
import discord



class LevelCog(commands.Cog):
	def __init__(self, bot):
	   self.bot = bot
	   super().__init__()
	  
	@commands.Cog.listener()
	async def on_message(self, message):
	   c = len(message.content)
	   await self.add_exp(message.author.id, c, message.channel)
	 
	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload:discord.RawReactionActionEvent =None):
		if payload is not None:
			await self.add_exp(payload.user_id, 20, cassandra.get_channel(payload.channel_id))
	
	async def add_exp(self, id, exp, channel, a=True):
		if a:
			print("Adding", exp, "exp")
			print(f"Id: {id}")
		u = CUser(id)
		before = get_level(u.exp)
		after = get_level(u.exp + exp)
		if before != after and id != self.bot.user.id:
			nl = str(get_level(u.exp + exp))
			if nl.isnumeric():
				nl = f"Level {nl}"
			await channel.send(f"Congratulations {cassandra.get_user(u.discord).mention} You Reached {nl}")
		
		
		u.refresh()
		if id != self.bot.user.id:
			print("Before:", u.exp)
		update(discord=u.discord, exp=u.exp+exp, gbp=u.gbp, _inventory=u.inventory)
		if id != self.bot.user.id:
			print("After:", u.exp)



	
def setup(bot):
	print("Loading Level Extension")
	bot.add_cog(LevelCog(bot))
	
try:
	setup(cassandra)
except:
	pass
