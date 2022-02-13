from discord.ext import commands
from .levels import CUser, get_level, update
from .bot import cassandra, bs_say
import discord
from asyncio import sleep
from humanize import intcomma



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


async def wages(bot):
	await sleep(20)
	while True:
		msg = "Daily wages:\n"
		done = []
		for guild in bot.guilds:
			for m in guild.members:
				if m.id not in done:
					u = CUser(m.id)
					wage = 100
					add = 50
					for _ in range(0, get_level(u.exp)):
						wage += add
					
					u.add_gbp(wage)
					done.append(u.discord)
					msg += f"{m.display_name}: ¥{intcomma(wage)}"
		
		await bs_say(msg)
		day = (60 * 60) * 24
		await sleep(day)
					
	
def setup(bot):
	print("Loading Level Extension")
	bot.add_cog(LevelCog(bot))
	bot.loop.create_task(wages(bot))
	
try:
	setup(cassandra)
except:
	pass
