from copy import deepcopy
from .bot import cassandra
from .db import CUser
level_range = []

required = 100
for _ in range(1, 501):
	level_range.append(deepcopy(required))
	required = int((required * 1.3))

def get_level(exp):
	req = 0
	lvl = 1
	for level in level_range:
		if req + level > exp:
			return lvl
		req += level
		lvl += 1
	return "Max Lvl"


@cassandra.command(name="lvl")
async def lvl(ctx):
	u = CUser(ctx.message.author.id)
	await ctx.message.channel.send(f"{ctx.message.author.display_name}: Level {get_level(u.exp)}")
	await ctx.message.delete()
	