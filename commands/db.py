import psycopg2
import os
import humanize

PASS = os.environ['PASS']

CFG = {"host":"ec2-52-51-155-48.eu-west-1.compute.amazonaws.com",
    "port": 5432,
    "database":"d1a5os1go03lqu",
    "user":"lptycphsmjryri",
    "password":PASS}

def update(discord, gbp, exp, _inventory):
	""" update vendor name based on the vendor id """
	inventory = '{"inventory":!}'.replace("!", str(_inventory))
	sql = f"""UPDATE accounts
SET GBP = {gbp},
    EXP = {exp},
	INVENTORY = '{inventory}'
WHERE DISCORD = {discord};"""
	
	conn = None
	
	try:
		# read database configuration
		params = {}
		# connect to the PostgreSQL database
		conn = psycopg2.connect(**CFG)
		# create a new cursor
		cur = conn.cursor()
		# execute the UPDATE  statement
		cur.execute(sql)
		# get the number of updated rows
		# Commit the changes to the database
		conn.commit()
		# Close communication with the PostgreSQL database
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()
			
	#print(sql)
	user = get_user(discord, create=False)
	return user


def add_user(discord, gbp=0, exp=0, _inventory=[]):
	print("Adding", discord)
	inventory = """{"inventory":!}""".replace("!", str(_inventory))
	sql = """INSERT INTO accounts(DISCORD, GBP, EXP, INVENTORY)
VALUES ({discord}, {gbp}, {exp}, '{inventory}');"""
	sql = sql.format(discord=discord, gbp=gbp, exp=exp, inventory = inventory)
	
	conn = None
	
	try:
		# connect to the PostgreSQL database
		conn = psycopg2.connect(**CFG)
		# create a new cursor
		cur = conn.cursor()
		# execute the UPDATE  statement
		cur.execute(sql)
		# get the number of updated rows
		# Commit the changes to the database
		conn.commit()
		# Close communication with the PostgreSQL database
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()
	
	#print(sql)
	return get_user(discord, create=False)
	
def get_user(discord, create=True):
	sql = f'select * from "public"."accounts" where DISCORD = {discord}'
	conn = None
	user = None
	
	try:
		# connect to the PostgreSQL database
		conn = psycopg2.connect(**CFG)
		# create a new cursor
		cur = conn.cursor()
		# execute the UPDATE  statement
		cur.execute(sql)
		try:
			user = cur.fetchone()
		except:
			user = None
		
		if user == None and create:
			user = add_user(discord, 0, 0, [])
			print("added user", user[0], ":", discord)
			if conn is not None:
				conn.close()
			return user
		# Commit the changes to the database
		conn.commit()
		# Close communication with the PostgreSQL database
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()
	
	return user

from .bot import cassandra

class CUser():
	def __init__(self, discord):
		self.id = 0
		self.discord = discord
		self.exp = 0
		self.gbp = 0
		self.inventory = []
		self.exists = True
		self.refresh()
	
	def refresh(self):
		try:
			self.id, _, self.exp, self.gbp, self.inventory = get_user(self.discord)
		except Exception as e:
			print(e)
			self.exists = False
		print("user:", self.id, "¥", self.gbp)
		return self
		

def ensure_table():
	count = 0
	try:
			sql = """CREATE TABLE IF NOT EXISTS accounts (
	ID serial PRIMARY KEY,
	DISCORD bigint NOT NULL,
	
	EXP bigint NOT NULL,
	GBP bigint NOT NULL,
	INVENTORY jsonb
	);"""
			# connect to the PostgreSQL database
			conn = psycopg2.connect(**CFG)
			# create a new cursor
			cur = conn.cursor()
			# execute the UPDATE  statement
			cur.execute(sql)
			# Commit the changes to the database
			conn.commit()
			cur.execute('select * from "public"."accounts";')
			count = cur.rowcount
			if count == 0:
				cur.execute("""INSERT INTO accounts(ID, DISCORD, GBP, EXP, INVENTORY)
VALUES (0, 940014399719108638, 69420, 9001, '{"inventory":[]}');
""")
				conn.commit()
				cur.execute('select * from "public"."accounts";')
				count = cur.rowcount
			# Close communication with the PostgreSQL database
			cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()
		return count
			
			
entries = ensure_table()
print("Database Loaded", humanize.intcomma(entries), "entries present")

@cassandra.command(name="gbp", help="Get your gbp total")
async def gbp(ctx):
	uid = ctx.message.author.id
	u = CUser(uid)
	if not u.exists:
		await ctx.message.channel.send("No such user")
		await ctx.message.delete()
		return
	await ctx.message.channel.send(f"{ctx.message.author.display_name}: ¥{humanize.intcomma(u.gbp)}")
	await ctx.message.delete()

from discord import User
from .bot import has_role

@cassandra.command(name="givegbp", help="Give someone gbp")
async def givegbp(ctx, recipient:User, n:int, remove=None):
	if remove != None and has_role(ctx.message.author):
		remove = False
	else:
		remove = True
		
	uid = ctx.message.author.id
	u = CUser(uid)
	if not u.exists:
		await ctx.message.channel.send("No such user")
		await ctx.message.delete()
		return
		
	if n <= 0 and remove:
		await ctx.message.channel.send(f"Value must be > ¥0")
		await ctx.message.delete()
		return 
		
	if u.gbp < n and remove:
		await ctx.message.channel.send(f"Insufficient Funds {u.gbp}")
		await ctx.message.delete()
		return 
	
	r = CUser(recipient.id)
	if not r.exists:
		await ctx.message.channel.send(f"No such user {recipient.id}")
		await ctx.message.delete()
		return
	
	update(u.discord, (u.gbp-n) if remove else u.gbp, u.exp, u.inventory)
	update(r.discord, r.gbp+n, r.exp, r.inventory)
	
	await ctx.message.channel.send(f"{ctx.message.author.display_name} gave {recipient.display_name} ¥{humanize.intcomma(n)}")
	await ctx.message.delete()

if __name__ == '__main__':
	#print(CFG)
	try:
		print("get user:", get_user(940014428752072765))
		print("update user:", update(940014428752072765, 69420, 0, [6,7,8]))
	except:
		pass
		

