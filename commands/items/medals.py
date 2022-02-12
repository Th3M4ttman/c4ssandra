from .shop import SHOP, Item, define_item
import datetime

class Award(Item):
	def __init__(self, name, recipient, reason):
		super().__init__({"name":name, "value":1000, "cls":"Award", "reason": reason, "awarded":str(datetime.datetime.now().timestamp()), "recipient":recipient})
		
	def inspect(self, ctx, bot, user):
		name = bot.get_user(user.discord).display_name
		awarded = str(datetime.datetime.fromtimestamp(self.data["awarded"]))
		return f"{name} shows off their {self.name}:\n\tReason: {self.data['reason']}\n\tAwarded on: {awarded.split('.')[0]}"
		
	async def use(self, ctx, bot,  user, *args, **kwargs):
		return False, self.inspect(ctx, bot, user)


define_item("Award", Award)
