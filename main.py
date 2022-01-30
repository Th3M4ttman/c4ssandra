#pylint:disable=E0401
""" C4ssandra Discord bot """


import discord
from commands.bot import cassandra

import os
KEY = os.environ['BOTKEY']


cassandra.run(KEY)



