from discord.ext import tasks
from asyncio import sleep
from .db import CUser, cassandra
import datetime		
			
from discord.ext.commands import Cog


async def check_lounge(self):
	print("looping through users")
	for guild in self.bot.guilds:
		for m in guild.m:
			user = CUser(m.id)
			if "expiry" in user.stats.keys():
				expiry = datetime.datetime.fromtimestamp(user.stats["expiry"])
			else:
				expiry = datetime.datetime.fromtimestamp(0)
				
			name = self.bot.get_user(user.discord).display_name
			if expiry <= datetime.datetime.now():
				print(f"{name} not allowed in the lounge")
			else:
				print(f"{name} is allowed in the lounge")
			
	
					
class LoungeCog(Cog):
	def __init__(self, bot):
	   self.bot = bot
	   super().__init__()
	   print("lounge init")
	
	@Cog.listener()
	async def on_ready(self):
		print("wtf man")
		while True:
			await check_lounge(self)
			await sleep(60)
			
def setup(bot):
	print("setup Lounge Extension...")
	bot.add_cog(LoungeCog)
	
try:
	setup(cassandra)
except:
	pass

