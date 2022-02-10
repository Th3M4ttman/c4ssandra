from discord.ext import tasks
from asyncio import sleep
from .db import CUser, cassandra
import datetime		
			
from discord.ext.commands import Cog

@tasks.loop(minutes=5)
async def check_lounge(self):
	print("looping through users")
	for guild in self.guilds:
		for m in guild.m:
			user = CUser(m.id)
			if "expiry" in user.stats.keys():
				expiry = datetime.datetime.fromtimestamp(user.stats["expiry"])
			else:
				expiry = datetime.datetime.fromtimestamp(0)
				
			name = self.get_user(user.discord).display_name
			if expiry <= datetime.datetime.now():
				print(f"{name} not allowed in the lounge")
			else:
				print(f"{name} is allowed in the lounge")
			
	
					


def setup(bot):
	print("Starting lounge loop")
	bot.loop.create_task(check_lounge(bot))
	
try:
	setup(cassandra)
except:
	pass

