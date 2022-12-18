from discord.ext import commands
from discord import app_commands, Interaction, Object, Member


class OwnerCog(commands.GroupCog, name="owner"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()


async def setup(bot: commands.Bot) -> None:
    """ Add this cog to the bot """
    await bot.add_cog(OwnerCog(bot), guilds=[Object(id=957867801119449109)])
