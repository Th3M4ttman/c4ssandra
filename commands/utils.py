import discord
from discord.ext.commands import Context, Bot
from copy import deepcopy

class Choices():
	def __init__(self, prompt, choices = []):
		self.pages = []
		self.prompt = prompt
		page = []
		for choice in choices:
			if len(page) >= 10:
				self.pages.append(deepcopy(page))
				page = []
			page.append(choice)
			
		if len(page)>0:
			self.pages.append(deepcopy(page))
			
	def __len__(self):
		i = 0
		for p in self.pages:
			for c in p:
				i += 1
		return i
				
	def page(self, _page):
		nums = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣", "🔟"]
		nextpage = "⬇️"
		page = self.pages[_page]
		out = f"{self.prompt}"
		if len(self.pages) >1:
			out += f" Page {_page+1}"
		for i, ch in enumerate(page):
			out += f'\n\t{nums[i]} - {ch}'
		if len(self.pages) > 1:
			p = _page + 1
			if p + 1 > len(self.pages):
				p = 0
			out += f"\n\t{nextpage} - Page {p+1}"
		return out
	
	def get_choice(self, page, item):
		return self.pages[page][item]
		
	async def send(self, ctx:Context, bot:Bot, timeout=0):
		made = False
		nums = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣", "🔟", "⬇️"]
		msg = None
		page = 0
		while not made:
			if msg is not None:
				try:
					await msg.delete()
				except:
					pass
			
			if page >= len(self.pages):
				page = 0
			
			prompt = self.prompt + ":"
			
			msg = await ctx.channel.send(prompt + self.page(page))
			
			for num in nums:
				for m in ctx.message.guild.members:
					try:
						msg.remove_reaction(num, m)
					except:
						pass
			for i, choice in enumerate(self.pages[page]):
				await msg.add_reaction(nums[i])
				
			def check(reaction, user):
				return user.id == ctx.author.id and reaction.emoji in nums
				
			if timeout:
				reaction, user = await bot.wait_for('reaction_add', timeout=timeout, check=check)
			else:
				reaction, user = await bot.wait_for('reaction_add', check=check)
				
			c = nums.index(str(reaction)) + 1
			await msg.delete()
			return self.get_choice(page, c)
		
			
		


async def choice(prompt, choices, ctx:Context, bot:Bot, timeout=0):
	nums = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣", "🔟"]
	nextpage = "⬇️"
	if len(choices) > 10:
		...
	
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
	return nums.index(reaction.emoji) + 1

