from discord.ext import tasks
from asyncio import sleep
from .db import CUser
import datetime

@tasks.loop(minutes=60)
async def test(bot):
	for guild in bot.guilds:
		for m in guild.m:
			user = CUser(m.id)
			if "expiry" in user.stats.keys():
				expiry = datetime.datetime.fromtimestamp(user.stats["expiry"])
			else:
				expiry = datetime.datetime.fromtimestamp(0)
				
			name = bot.get_user(user.discord).display_name
			if expiry <= datetime.datetime.now():
				print(f"{name} not allowed in the lounge")
			else:
				print(f"{name} is allowed in the lounge")
				
			
	