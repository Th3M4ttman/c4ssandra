from discord.ext import commands
from .levels import CUser, get_level, update
from .bot import cassandra
import discord
from asyncio import sleep



class LevelCog(commands.Cog):
	def __init__(self, bot):
	   self.bot = bot
	   super().__init__()
	  
	@commands.Cog.listener()
	async def on_message(self, message):
	   c = len(message.content)
	   await sleep(2)
	   await self.add_exp(message.author.id, c, message.channel)
	 
	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload:discord.RawReactionActionEvent =None):
		if payload is not None:
			await sleep(2)
			await self.add_exp(payload.user_id, 20, cassandra.get_channel(payload.channel_id))
	
	async def add_exp(self, id, exp, channel, a=True):
		if a:
			pass
			#print("Adding", exp, "exp")
			#print(f"Id: {id}")
		u = CUser(id)
		before = get_level(u.exp)
		after = get_level(u.exp + exp)
		if before != after:
			nl = str(get_level(u.exp + exp))
			if nl.isnumeric():
				nl = f"Level {nl}"
			await channel.send(f"Congratulations {cassandra.get_user(u.discord).mention} You Reached {nl}")
		
		
		
		#if self.bot.get_user(id).display_name != "C4ssandra":
			#print("Before:", u.refresh().exp)
		update(discord=u.discord, exp=u.exp+exp, gbp=u.gbp, _inventory=u.inventory, stats=u.stats)
		#if self.bot.get_user(id).display_name != "C4ssandra":
			#print("After:", u.refresh().exp)



	
def setup(bot):
	print("Loading Level Extension")
	bot.add_cog(LevelCog(bot))
	
try:
	setup(cassandra)
except:
	pass
