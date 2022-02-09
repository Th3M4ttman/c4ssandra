from discord.ext import commands
from levels import CUser, get_level

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
