import discord
from discord.ext import commands

from donutstats import DonutStats

class Stats(commands.Cog):
    def __init__(self, bot: commands.Bot):
        # Initialize donutstats when your cog gets initialized
        self.donutstats = DonutStats("Your DonutSMP api key (generate ingame with /api")

    @discord.app_commands.command()
    async def stats(self, interaction: discord.Interaction, username: str):
        # Returns a full stats embed
        embed: discord.Embed = await self.donutstats.get_stats_embed(username, discord.Color.blue())

        await interaction.response.send_message(embed=embed)

    async def cog_unload(self):
        await self.donutstats.close() # Cleanly close the aiohttp connection, aiohttp gets loud about unclosed connections

async def setup(bot: commands.Bot):
    await bot.add_cog(Stats(bot))