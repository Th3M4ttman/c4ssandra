import psycopg2
import os

PASS = os.environ['PASS']

CFG = {"host":"ec2-52-51-155-48.eu-west-1.compute.amazonaws.com",
    "port": 5432,
    "database":"d1a5os1go03lqu",
    "user":"lptycphsmjryri",
    "password":PASS}

def update(discord, gbp, inventory):
	""" update vendor name based on the vendor id """
	inventory = '{"inventory":!}'.replace("!", str(inventory))
	sql = f"""UPDATE accounts
SET GBP = {gbp},
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
			
	print(sql)
	user = get_user(discord)
	return user


def add_user(id, discord, gbp=0, inventory={"inventory":[]}):
	print("Adding", id)
	sql = """INSERT INTO accounts(ID, DISCORD, GBP, INVENTORY)
VALUES ({id}, {discord}, {gbp}, '{inventory}');"""
	sql = sql.format(id=id, discord=discord, gbp=gbp, inventory = inventory)
	
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
	
	print(sql)
	return get_user(discord)
	
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
		user = add_user(1, discord, 0, [])
	return user
	

if __name__ == '__main__':
	print(CFG)
	try:
		print(get_user(940014428752072765))
		print(add_user(0, 69, 420, {"inventory":[1,2,3]}))
		print(update(940014428752072765, 99, [4,5,6]))
	except:
		pass
		

