import discord
from discord.ext.commands import Context, Bot
from copy import deepcopy

class Choices():
	def __init__(self, prompt, choices = []):
		self.pages = []
		self.prompt = prompt
		page = []
		for choice in choices:
			page.append(choice)
			if len(page) >= 10:
				self.pages.append(deepcopy(page))
				page = []
		if len(page)>0:
			self.pages.append(deepcopy(page))
				
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
		
	async def send(prompt, choices, ctx:Context, bot:Bot, timeout=0):
		made = False
		while not made:
			pass
		
			
x=Choices("Pick 1", [1,2,3,4,5,6,7,8,9,10, 11])
			
print(x.page(0))
print()
			

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

