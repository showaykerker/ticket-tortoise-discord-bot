from discord import ApplicationContext
from ezcord import Bot
from ezcord import Cog
from ezcord.internal.dc import discord as dc


class Help(Cog, hidden=True):
    def __init__(self, bot: Bot):
        super().__init__(bot)

    @dc.slash_command(
        name="help", description="Shows the help message."
    )
    async def command_name(self, ctx: ApplicationContext) -> None:
        await ctx.send("hi")


def setup(bot: Bot):
    bot.add_cog(Help(bot))
