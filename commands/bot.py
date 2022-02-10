from discord.ext.commands import Bot
import discord
import os

ROOT = os.path.abspath("/".join(__file__.split("/")[0:-1]))

intents = discord.Intents.default()
intents.members = True

class Cassandra(Bot):
	
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.triggers = {}
		
	async def on_ready(self):
		print(f'{self.user} has connected to Discord!')
		
	
	async def on_message(self, message):
		await super().on_message(message)
		print(message.author.name, message.content, sep=": ")
		for trigger in self.triggers.keys():
			if trigger.lower() in message.content.lower() and message.author != self.user:
				await self.triggers[trigger](message)
		

async def fart(ctx):
	await ctx.reply("Pfffrt")

async def GK(ctx):
	await ctx.reply("General Kenobi")
	
	
cassandra = Cassandra(command_prefix="!", intents=intents)
cassandra.triggers["Fart"] = fart
cassandra.triggers["Hello there"] = GK

import discord

async def has_role(who: discord.Member, guild = discord.Guild, role="Admin", message = None):
	_role = discord.utils.find(lambda r: r.name == role, guild.roles)
	if _role in who.roles:
		return True
	if message is not None:
		await message.reply("Insufficient privileges")
	return False
	

	
		
async def bs(ctx:discord.ext.commands.Context):
	msg = ctx.message
	content = msg.content
	author = msg.author.display_name
	channel = msg.channel
	
	content = "⚙️" + f"\nUser: {author}\nChannel: {channel}\nCommand: {content}"
	
	
	try:
		await ctx.message.delete()
	except:
		pass
	channels = cassandra.get_all_channels()
	for ch in channels:
		if str(ch) == "bot_spam":
			return await ch.send(content=content)
	

await cassandra.get_user(941188857167245362).send("Rebooted")
