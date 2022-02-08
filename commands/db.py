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


def add_user(id, discord, gbp=0, exp=0, _inventory=[]):
	print("Adding", id)
	inventory = """'{"inventory":!}'""".replace("!", str(_inventory))
	sql = """INSERT INTO accounts(ID, DISCORD, GBP, EXP, INVENTORY)
VALUES ({id}, {discord}, {gbp}, {exp} {inventory});"""
	sql = sql.format(id=id, discord=discord, gbp=gbp, exp=exp, inventory = inventory)
	
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
		user = cur.fetchone()
		# Commit the changes to the database
		conn.commit()
		# Close communication with the PostgreSQL database
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()
			
	if user is None and create:
		user = add_user(1, discord, 0, 0, [])
	return user

from .bot import cassandra

class CUser():
	def __init__(self, discord):
		self.id = 0
		self.discord = discord
		self.gbp = 0
		self.exp = 0
		self.inventory = {}
		self.refresh()
	
	def refresh(self):
		self.id, _, self.gbp, self.exp, self.inventory = get_user(self.discord)

def ensure_table():
	count = 0
	try:
			sql = """CREATE TABLE IF NOT EXISTS accounts (
	ID serial PRIMARY KEY,
	DISCORD bigint NOT NULL,
	
	EXP bigint NOT NULL,
	GBP bigint NOT NULL,
	INVENTORY json NOT NULL
	);
INSERT INTO accounts(ID, DISCORD, GBP, EXP, INVENTORY)
VALUES (0, 940014399719108638, 69420, 9001, '{"inventory":[]}');"""
			# connect to the PostgreSQL database
			conn = psycopg2.connect(**CFG)
			# create a new cursor
			cur = conn.cursor()
			# execute the UPDATE  statement
			cur.execute(sql)
			# Commit the changes to the database
			conn.commit()
			
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
	if u is None:
		await ctx.message.channel.send("Fuck")
		await ctx.message.delete()
	await ctx.message.channel.send(f"{ctx.message.author.display_name}: ¥{humanize.intcomma(u.gbp)}")
	await ctx.message.delete()
	

if __name__ == '__main__':
	#print(CFG)
	try:
		print("get user:", get_user(940014428752072765))
		print("add user:", add_user(69420, 940014456207966232, 69420, 0, []))
		print("update user:", update(940014428752072765, 69420, 0, [6,7,8]))
	except:
		pass
		

