from typing import Optional
from discord import app_commands, Interaction, Object, Member, Embed
from discord.ext import commands
from models.profile import Profile
from util.database_utils import fetch_user


class PlayerCog(commands.GroupCog, name="player"):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="setup", description="Initiates the setup of the user's player")
    async def player_setup(self, interaction: Interaction):
        """ Initiates the setup of the user's player """
        if interaction.user.bot:
            return await interaction.response.send_message("Bots cannot make profiles")

        async with self.bot.pool.acquire() as conn:
            async with conn.transaction():
                result = await conn.fetchrow("SELECT * FROM profile WHERE profile_id = $1", interaction.user.id)
                if result is not None:
                    await interaction.response.send_message("Already registered as a player, no need to re-register.")
                    return
                await conn.execute("INSERT INTO profile (profile_id) VALUES ($1)", interaction.user.id)
                return await interaction.response.send_message(f"Created profile for {interaction.user.name}")

    @app_commands.command(name="profile", description="Shows you yours/other's profiles")
    async def player_profile(self, interaction: Interaction, member: Optional[Member] = None):
        member = member or interaction.user

        if member.bot:
            return await interaction.response.send_message("Bots cannot make profiles")

        async with self.bot.pool.acquire() as conn:
            async with conn.transaction():
                result = await fetch_user(profile_id=member.id, client=self.bot)
                if result is None:
                    return await interaction.response.send_message(f"{member.name} does not have a profile. {member.name} needs to run /player setup")
                profile = Profile(dict(result))
                embed = Embed(
                    description='Here is the profile you asked for!',
                    color=0x32cd32
                )
                embed.set_author(name=f"{member.name} | Profile", icon_url=member.avatar.url)
                embed.add_field(name='**Profile ID:**', value=profile.profile_id)
                embed.add_field(name='**Class: **', value=profile.class_name, inline=True)
                embed.add_field(name='**Balance:**', value=profile.balance)
                embed.add_field(name='**Rank:**', value=profile.rank_name, inline=True)
                return await interaction.response.send_message(embed=embed)

    @app_commands.command(name="inventory", description="Allows player to view their inventory")
    async def inventory(self, interaction: Interaction):
        return await interaction.response.send_message("Hello, World")


async def setup(bot: commands.Bot):
    """ Add this cog to the bot """
    await bot.add_cog(PlayerCog(bot), guilds=[Object(id=957867801119449109)])
