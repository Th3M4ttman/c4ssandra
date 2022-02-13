import discord
from discord.ext.commands import Context, Bot

async def choice(prompt, choices, ctx:Context, bot:Bot, timeout=0):
	nums = ["0️⃣", "1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣"]
	prompt = prompt + ":"
	for i, choice in enumerate(choices):
		prompt += f"\n\t{nums[i]} - {choice}"
	
	msg = await ctx.channel.send(prompt)
	for i, choice in enumerate(choices):
		await msg.add_reaction(nums[i])
		
	def check(reaction, user):
		return user.id == ctx.author.id and reaction.emoji in nums
	
	if timeout:
		reaction, user = await bot.wait_for('reaction_add', timeout=timeout, check=check)
	else:
		reaction, user = await bot.wait_for('reaction_add', check=check)
	
	await msg.delete()
	return nums.index(reaction.emoji)
	