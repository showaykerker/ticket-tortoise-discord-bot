import urllib.parse
from discord import ApplicationContext
from ezcord import Bot
from ezcord import Cog
from ezcord.internal.dc import discord as dc

class UI(Cog, hidden=True):
    def __init__(self, bot: Bot):
        super().__init__(bot)

    @dc.slash_command(
        name="watch", description="Creates a new request"
    )
    async def command_name(self, ctx: ApplicationContext) -> None:
        userId = ctx.author.id
        content = ctx.message.strip()
        parsed_url = urllib.parse.urlparse(content)
        if parsed_url.scheme and parsed_url.netloc:
            if not self.bot.mongo.has_user(userId):
                self.bot.mongo.register_user(userId, ctx.author.name)
            self.bot.mongo.create_user_request(userId, content)
            await ctx.send("The content is a valid web link.")
        else:
            await ctx.send("The content is not a valid web link.")


def setup(bot: Bot):
    bot.add_cog(UI(bot))
