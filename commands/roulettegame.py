import random
from humanize import intcomma
import datetime
from .db import CUser
from asyncio import sleep

class Bet():
	def __init__(self, bet:str, user:CUser):
		self.bet = None
		self.amt = 0
		self.numbers = []
		self.colour = " "
		self.user = user
		
		if type(bet.split(" ")) == list:
			parts = bet.split(" ")
			
			if parts[0] in [str(i) for i in range(0, 37)]:
				self.bet = "number"
				self.numbers.append(int(parts[0]))
				self.colour = None
				self.amt = int(parts[1])
				self.pay_ratio = 36
				
			elif parts[0].lower() in ("red", "black", "green"):
				self.pay_ratio = 2
				self.bet = "colour"
				if parts[0].lower() == "red":
					self.colour = "Red"
				elif parts[0].lower() == "black":
					self.colour = "Black"
				elif parts[0].lower() == "green":
					self.colour = "Green"
				
				self.amt = int(parts[1])
				
			elif parts[0].lower() in ("high", "low"):
				self.pay_ratio = 2
				self.bet = "half"
				if parts[0].lower() == "high":
					self.numbers = range(19, 36)
				elif parts[0].lower() == "low":
					self.numbers = range(1, 19)
				
				
				self.amt = int(parts[1])
				
			elif parts[0].lower() in ("odds", "evens"):
				self.pay_ratio = 2
				self.bet = "half"
				if parts[0].lower() == "evens":
					self.numbers = [32, 4, 2, 34, 6, 36, 30, 8, 10, 24, 16, 20, 14, 22, 18, 28, 12, 26]
				elif parts[0].lower() == "odds":
					self.numbers = [15, 19, 21, 25, 17, 27, 13, 11, 23, 5, 33, 1, 31, 9, 29, 7, 35, 3]
				
				
				self.amt = int(parts[1])
				
			elif parts[0].lower() in ("third1", "third2", "third3"):
				self.bet = "third"
				self.pay_ratio = 3
				if parts[0].lower() == "third1":
					self.numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
				elif parts[0].lower() == "third2":
					self.numbers = [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
				elif parts[0].lower() == "third3":
					self.numbers = [25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36]
				
				self.amt = int(parts[1])
				
			elif parts[0].lower() in ("row1", "row2", "row3"):
				self.bet = "row"
				self.pay_ratio = 3
				if parts[0].lower() == "row3":
					self.numbers = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36]
				elif parts[0].lower() == "row2":
					self.numbers = [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35]
				elif parts[0].lower() == "row1":
					self.numbers = [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34]
				
				self.amt = int(parts[1])
		if self.user.gbp < self.amt:
			self.bet = None
			self.colour = ""
			self.numbers = []
			
		if self.bet is not None:
			self.user.add_gbp(-self.amt)
		self.won = None
		self.paid = -self.amt
					
	def payout(self, colour, number):
		p = self.amt
		p *= self.pay_ratio
		if number in self.numbers or str(colour).lower() == str(self.colour).lower():
			self.user.add_gbp(p)
			self.won = True
			self.paid += p
		else:
			self.won = False
		

class Roulette():
	def __init__(self):
		self.bets = []
		self.wheel = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]
		self.number = None
		self.colour = None
		
	
	def add_bet(self, bet):
		if bet.bet is not None:
			self.bets.append(bet)
	
	def spin(self):
		i = random.randint(0, len(self.wheel)-1)
		self.number = self.wheel[i]
		if self.number in [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]:
			self.colour = "Red"
		elif self.number in [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]:
			self.colour = "Black"
		elif self.number == 0:
			self.colour = "Green"
		
			
		
		for bet in self.bets:
			bet.payout(self.colour, self.number)
				
		
	def __str__(self):
		if self.number is not None:
			return f"\n{self.colour} {self.number}\n"
		return "Place your bets\n35:1 green / 0 - 36\n 1:1 red/black\n 1:1 high/low\n 1:1 odds/evens\n 2:1 third1/third2/third3 \n 2:1 row1/row2/row3\n\n(bet) (amount)\ne.g third1 50"

import discord
from .bot import cassandra
from .utils import trydelete

@cassandra.command(name="roulette")
async def roulette(ctx):
	await trydelete(ctx)
	wheel = Roulette()
	board = await ctx.channel.send(str(wheel))
	def check(message):
		return message.author.id != cassandra.user.id and message.reference.message_id == ctx.message.to_reference().message_id
	
	stop = datetime.datetime.now() + datetime.timedelta(minutes=1)
	while datetime.datetime.now() <= stop:
		try:
			msg = await cassandra.wait_for("message", check=check, timeout=5)
		except:
			continue
			
		try:
			u = CUser(msg.author.id)
			c = msg.content
			b = Bet(c, u)
			if b.bet is None:
				continue
			wheel.add_bet(b)
		except Exception as e:
			print(e)
	await board.edit(content="No More Bets!\nSpinning...")
	await sleep(6)
	wheel.spin()
	out = str(wheel.number)
	for bet in wheel.bets:
		if bet.bet:
			out += f"\n<@{bet.user.id}>: {bet.bet} ¥{intcomma(bet.paid)}"
	await board.edit(content=out)
	
			

