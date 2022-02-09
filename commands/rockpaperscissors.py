from .bot import cassandra
import random
from discord import Message, Reaction
import time
import discord
from .db import CUser
from humanize import intcomma

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


def wait_for_react(player, message: Message):
	while True:
		for react in message.reactions:
			print(react)
			if str(react) in  ("🪨", "📃", "✂️"):
				print(react.users)
				if player in list(react.users):
					return str(react), player
			

def wait_for_thumb(player, bot, message, timeout = 10):
	elapsed = 0
	while True:
		for react in message.reactions:
			react = Reaction
			if str(react) == "👍":
				for user in react.users:
					if user not in (player, bot):
						return user
		time.sleep(.1)
		if elapsed >= timeout:
			raise TimeoutError("Timeout")
		elapsed += .1
	


def rock_paper_scissors(x, y):
	if x == 0:
		if y == 0:
			return 2
		elif y == 1:
			return 1
		else:
			return 0
	elif x == 1:
		if y == 0:
			return 0
		elif y == 1:
			return 2
		else:
			return 1
	else:
		if y == 0:
			return 1
		elif y == 1:
			return 0
		else:
			return 2
			
def rps_game(players, moves):
	player1, player2 = players
	move1, move2 = moves
	emoji = ("🪨", "📃", "✂️")
	result = rock_paper_scissors(move1, move2)
	out = str(player1.mention) + "   " +  emoji[move1] + "  -vs-  " + emoji[move2] + "   " + str(player2.mention) +"\n"
	winner = None
	loser = None
	if result == 2:
		out += "\nIts a Draw!"
	elif result == 0:
		out += f"\n{player1.mention} Wins!"
		winner = player1.id
		loser = player2.id
	elif result == 1:
		out += f"\n{player2.mention} Wins!"
		winner = player2.id
		loser = player1.id
	return winner, loser, out

@cassandra.command(name="rps", help="Play rock paper scissors")
async def rps(message, wager:int = 0):
	player1 = message.author
	if wager < 0:
		wager = 0
	try:
		g = CUser(player1).gbp
	except Exception as e:
		print(e)
		g = 0
		
	if g < wager:
		await message.reply("Insufficient Funds")
		await bs(message)
		return
		
	await bs(message)
	invite = await message.channel.send(f"{player1.mention} wants to play rock paper scissors, react with a thumbs up to play against them. the wager is ¥{intcomma(wager)}")
	await invite.add_reaction("👍")
	def check(reaction, user):
		u = CUser(user.id)
		can_cover = False
		try:
			if u.gbp >= wager:
				can_cover = True
		except:
			pass
			
		return user not in (player1, invite.author) and str(reaction.emoji) == '👍' and can_cover
	try:
		_, player2 = await cassandra.wait_for('reaction_add', timeout=10.0, check=check)
	except:
		player2 = message.guild.get_member(936763503300190249)
		
	await invite.delete()
	announce = await message.channel.send(f"{player1.mention} vs {player2.mention}")
	x = await player1.send("Select your move")
	await x.add_reaction("🪨")
	await x.add_reaction("📃")
	await x.add_reaction("✂️")
	def checkmove1(reaction, user):
		print(str(reaction.emoji))
		return user == player1 and str(reaction.emoji) in ("🪨", "📃", "✂️")
	move1, player1 = await cassandra.wait_for('reaction_add',  check=checkmove1)
	move1 = ("🪨", "📃", "✂️").index(str(move1))
			
			
	if player2 == invite.author:
		move2 = random.randint(0,2)
	else:
		x = await player2.send("Select your move")
		await x.add_reaction("🪨")
		await x.add_reaction("📃")
		await x.add_reaction("✂️")
		def checkmove2(reaction, user):
			return user == player2 and str(reaction.emoji) in ("🪨", "📃", "✂️")
		move2, player2 = await cassandra.wait_for('reaction_add',  check=checkmove2)
		move2 = ("🪨", "📃", "✂️").index(str(move2))
	
	winner, loser, msg = rps_game((player1, player2), (move1, move2))
		
	if loser is not None and wager > 0:
		u = CUser(loser)
		
		u.update(gbp=u.gbp - wager)
		msg += "\n" + cassandra.get_user(loser).display_name + ": ¥" + intcomma(u.gbp)
		try:
			if u.gbp <= 0 and loser == cassandra.user.id:
				u.update(gbp=69420)
				
		except Exception as e:
			print(e)
			
		if winner is not None:
			u = CUser(winner)
			u.update(gbp=u.gbp + wager)
			msg += "\n" + cassandra.get_user(winner).display_name + f": ¥{intcomma(u.gbp)}"
			
	
	
	await announce.delete()
	await message.channel.send(msg)
	
			
		
	
			
	