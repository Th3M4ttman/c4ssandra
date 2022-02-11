from discord.ext import tasks
from asyncio import sleep
from .db import CUser, cassandra
import datetime		
			
from discord.ext.commands import Cog
import discord

async def check_lounge(self):
	await sleep(20)
	while True:
		print("Running lounge membership check...")
		for guild in self.guilds:
			lounge_role = discord.utils.get(guild.roles, name = "lounge")
			for m in guild.members:
				user = CUser(m.id)
				if user.stats is None:
					user.update(stats={})
				if "expiry" in user.stats.keys():
					expiry = datetime.datetime.fromtimestamp(user.stats["expiry"])
				else:
					expiry = datetime.datetime.fromtimestamp(0)
					
				name = m.display_name
				if expiry <= datetime.datetime.now():
					try:
						await m.add_roles(lounge_role)
						print("Added lounge role to", name, datetime.datetime.now() - expiry)
					except Exception as e:
						print(e)
					
				else:
					try:
						await m.remove_roles(lounge_role)
						print("Removed lounge role from", name)
					except Exception as e:
						print(e)
					
		await sleep(60)
			
	
					


def setup(bot):
	print("Starting lounge loop")
	bot.loop.create_task(check_lounge(bot))
	
try:
	setup(cassandra)
except:
	pass

