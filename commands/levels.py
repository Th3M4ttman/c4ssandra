from copy import deepcopy
from .bot import cassandra
from .db import CUser, update
from humanize import intcomma
from .utils import trydelete
level_range = []

required = 100
for _ in range(1, 501):
	level_range.append(deepcopy(required))
	required = int((required * 1.3)) + required

def get_level(exp):
	req = 0
	lvl = 1
	for level in level_range:
		if req + level > exp:
			return lvl
		req += level
		lvl += 1
	return "Max Lvl"
	
def level_bounds(exp):
	lvl = get_level(exp)
	if lvl == "Max Lvl":
		return 0, 0
	if lvl == 1:
		return 0, level_range[0]
	
	cur = level_range[lvl-2] 
	next = level_range[lvl-1]
	return cur, next	

def level_str(exp):
	cur, next = level_bounds(exp)
	lvl = get_level(exp)
	xp = int(exp)
	for i, k in enumerate(level_range):
		if i+1 == lvl:
			break
		xp -= k
	
	if cur == 0 and next == 0:
		return "Max Level"
	return f"Level {lvl}\n[{intcomma(xp)} | {intcomma(next)}] exp"
	
	

@cassandra.command(name="lvl")
async def lvl(ctx):
	u = CUser(ctx.message.author.id)
	await ctx.message.channel.send(f"{ctx.message.author.display_name}: {level_str(u.exp)}")
	await trydelete(ctx)
		
@cassandra.command(name="lvls")
async def lvls(ctx):
	out = ""
	for guild in cassandra.guilds:
		for member in guild.members:
			try:
				u = CUser(member.id)
				out += f"\n{u.name}: {level_str(u.exp)}"
			except:
				pass
	
	if out:
		await ctx.message.channel.send(out)
	await trydelete(ctx)
	
from discord.ext import commands

class LevelCog(commands.Cog):
    def __init__(self, bot):
       self.bot = bot
       super().__init__()
       
    async def on_message(self, message):
        u = CUser(message.author.id)
        c = len(message.content)
        before = get_level(u.exp)
        after = get_level(u.exp + c)
        
        u.update(exp=u.exp + c)
        if before != after:
        	await message.reply(f"Congratulations You Reached {get_level(u.exp)}")
        

def setup(bot):
    print("Loading Level Extension")
    bot.add_cog(LevelCog(bot))

