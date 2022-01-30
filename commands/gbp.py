
import json
from .bot import cassandra, has_role
import discord
import humanize

def load():
	with open("/storage/emulated/0/C4ssandra/Bot/commands/gbp.json") as f:
		return json.loads("".join(f.readlines()))

def save(points):
	with open("/storage/emulated/0/C4ssandra/Bot/commands/gbp.json", "w") as f:
		f.write(json.dumps(points, indent=4))


def get_gbp(id):
	points = load()
	try:
		return points[id.mention]
	except:
		return 0

def add_gbp(id, value):
	points = load()
	if id not in points.keys():
		points[id] = value
	else:
		points[id] += int(value)
	save(points)

@cassandra.command(name="gbp")
async def gbp(ctx, all = None):
	points = load()
	out = "Good Boi Points:\n"
	if all == "all":
		for k, i in points.items():
			out += f"{str(await cassandra.fetch_user(k.split('@')[1][0:-1])).split('#')[0]} - ¥{humanize.intcomma(i)}\n"
	else:
		try:
			out += str(ctx.message.author).split('#')[0] + f" - ¥{humanize.intcomma(points[ctx.message.author.mention])}\n"
		except Exception:
			out += str(ctx.message.author).split('#')[0] + f" - ¥0\n"
		for mention in ctx.message.mentions:
			try:
				out += f"{mention.display_name} - ¥{humanize.intcomma(points[mention.mention])}\n"
			except Exception:
				out += mention.display_name + f" - ¥0\n"
				
	
	await ctx.channel.send(out)
	
@cassandra.command(name="givegbp")
async def givegbp(ctx, value: int, god = None):
	m = list(ctx.message.mentions)
	if god == "god":
		if not await has_role(ctx.message.author, ctx.guild, "Admin", ctx.message):
			return
	for i, mention in enumerate(m):
		if god != "god":
			if value < 0 or get_gbp(ctx.message.author.mention):
				if value <= 0:
					await ctx.channel.send("Value must be > 0")
				else:
					await ctx.channel.send("Insufficient funds")
				return
				
		add_gbp(mention.mention, value=value)
		if god != "god":
			add_gbp(ctx.message.author.mention, value=-value)
		m[i] = mention.display_name
	m = ", ".join(m)
	v = humanize.intcomma(value)
	
	await ctx.channel.send(f"{str(ctx.message.author).split('#')[0]} Sent {v} Good Boi Points to {m}"if value > 0 else f"Took {v} Good Boi Points from {m}")
	await ctx.message.delete()

@cassandra.command(name="buy")
async def buy(ctx):
	cost = 100
	if get_gbp(ctx.message.author) >= cost:
		await ctx.channel.send(f"{ctx.message.author} bought fuck all for ¥100")
		add_gbp(ctx.message.author.mention, -100)
		await get_gbp(ctx)
	else:
		await ctx.channel.send("you cannot afford it")
	