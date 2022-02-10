from discord.ext import commands
from bot.commands.levels import CUser, get_level
from bot.commands.db import update

class LevelCog(commands.Cog):
    def __init__(self, bot):
       self.bot = bot
       super().__init__()
      
    @commands.Cog.listener()
    async def on_message(self, message):
        u = CUser(message.author.id)
        c = len(message.content)
        before = get_level(u.exp)
        after = get_level(u.exp + c)
        print("exp added:", c)
        update(u.discord, gbp=u.gbp, _inventory=u.inventory, exp=u.exp + c)
        
        if before != after:
        	nl = str(get_level(u.exp))
        	if nl.isnumeric():
        		nl = f"Level {nl}"
        	await message.reply(f"Congratulations You Reached {nl}")
        

def setup(bot):
    print("Loading Level Extension")
    bot.add_cog(LevelCog(bot))
