from asyncio import sleep
from .bot import cassandra, has_role
import random
from discord import Message, Reaction
import time
from . import rockpaperscissors
from . import gbp

@cassandra.command(name="test", help="Simple test")
async def test(ctx):
	await ctx.channel.send("Test success")

import discord
@cassandra.command(name="clear", help="Clear the log")
async def clear(ctx):
	if not await has_role(ctx.message.author, ctx.guild, "clear", ctx.message):
		return
	messages = await ctx.channel.history().flatten()
	await ctx.channel.purge()
	
@cassandra.command(name="python", help="run python")
async def python(ctx):
	out = str(ctx.message.content)[8:]
	try:
		if eval(out):
			await ctx.channel.send(eval(out))
	except Exception as e:
		await ctx.channel.send(e)

class Decisions(discord.ext.commands.Cog):
	""" decide upon things """
		
		
	@discord.ext.commands.command(name="decide", )
	async def decide(self, ctx):
		""" decide between supplied list seperated by "/" """
		choices = ctx.message.content.split("decide")[1].split("/")
		choices_str = " | ".join(choices)
		result = await ctx.channel.send(f"Deciding between:  {choices_str}")
		remaining = result.content.split("  ")[1].split(" | ")
		await ctx.message.delete()
		while len(remaining) > 1:
			
			time.sleep(1)
			remaining = result.content.split("  ")[1].split(" | ")
			remaining.pop(random.randint(0, len(remaining)-1))
			choices_str = " | ".join(remaining)
			await result.edit(content=f"Deciding between:  {choices_str}")
		await result.edit(content=f"Decided on: {remaining[0]}")
		
	@discord.ext.commands.command(name="vote")
	async def vote(self, ctx):
		""" votes between 2-9 options """
		msg = ctx.message.content
		if " time=" in msg:
			t = msg.split(" time=")[1]
			try:
				t = float(t)
			except:
				t = 60
		else:
			t = 60
		subjects = msg.split("vote ")[1].split("/")
		if "time=" in subjects[-1]:
			subjects[-1] = subjects[-1].split(" time=")[0]
		
		nums = ("1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣")
		
		out = ""
		for i, subject in enumerate(subjects):
			out += f"\n{subject} - {nums[i]}"
			
		v = await ctx.channel.send(out)
		for i, subject in enumerate(subjects):
			await v.add_reaction(nums[i])
			
		elapsed = 0
		while elapsed < t:
			await sleep(1)
			elapsed += 1
			
			await v.edit(content=f"Time Remaining: {int(t-elapsed)}\n" + out)
		
		v = await v.channel.fetch_message(v.id)
		
		reacts = v.reactions
		highest = None
		
		out = ""
		
		i = 0
		for react in reacts:
			if str(react) not in nums:
				print(react)
				continue
			
			users = await react.users().flatten()
			users = len(users) - 1
			
			if highest is None:
				highest = [react, len(await react.users().flatten())]
			else:
				if users > highest[1]:
					highest = [react, len(await react.users().flatten())-1]
					
					
			out += subjects[i] + " - " + str(users) + "\n"
			i += 1
		await v.edit(content=out)
		for react in v.reactions:
			for user in await react.users().flatten():
				await react.remove(user)
		
		
		
cassandra.add_cog(Decisions())

@cassandra.command(name="cs")
async def cs(ctx):
	messages = await ctx.channel.history().flatten()
	for message in messages:
		if message.author == cassandra.user or message.content.startswith("!"):
			await message.delete()
	

@cassandra.command(name="game")
async def game(ctx):
	try:
		role = ctx.guild.roles
		no_role = True
		for i, r in enumerate(role):
			if str(r) == "game?":
				role = role[i]
				no_role = False
				break
		if no_role:
			raise ValueError("No game? role exists")
		
	except Exception as e:
		print(e)
	
	if role == ctx.guild.roles:
		pass
	elif role not in ctx.message.author.roles:
		print(ctx.message.author, "Doesent have role:", role)
		return
			
	allowed_mentions = discord.AllowedMentions(everyone = True)
	game = await ctx.send(content = f"{ctx.message.author.mention}:\nGame‽ @everyone :regional_indicator_g::regional_indicator_a::regional_indicator_m::regional_indicator_e::interrobang:", allowed_mentions = allowed_mentions, file=discord.File("/storage/emulated/0/C4ssandra/Bot/commands/game.jpeg"))
	await ctx.message.delete()
	await game.add_reaction("👍")
	await game.add_reaction("👎")
	await game.add_reaction("⏰")

@cassandra.command(name="spam")
async def spam(ctx, member: discord.Member):
	if not await has_role(ctx.message.author, ctx.guild, "Admin", ctx.message.channel):
		return
	i = 0
	while True:
		i += 1
		if i >= 60:
			return
		msg = await member.send(f"Game? {member.mention}", file=discord.File("/storage/emulated/0/C4ssandra/Bot/commands/game.jpeg"))
		await msg.add_reaction("👍")
		await msg.add_reaction("👎")
		def check(reaction, user):
			return user != msg.author and str(reaction.emoji) in ('👍', "👎")
		try:
			react, _ = await cassandra.wait_for('reaction_add', timeout=2.0, check=check)
			await ctx.message.add_reaction(react)
			return 
		except:
			continue

async def lads(message):
	await message.reply("Lads Lads Lads!")
	
async def minrals(message):
	await message.reply("You aint got the minrals m8!")
	
cassandra.triggers["lad"] = lads
cassandra.triggers["minerals"] = minrals
cassandra.triggers["minrals"] = minrals
