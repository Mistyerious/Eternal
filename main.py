import os
from json import load
from discord import Intents
from discord.ext import commands
import asyncpg
import redis


class EternalClient(commands.Bot):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pool = None

        with open('./settings.json', encoding='utf_8') as content:
            self.settings = load(content)

        self.redis = redis.Redis()

    async def init_db(self):
        """ Initiates the database data and pool """

        self.pool = await asyncpg.create_pool(self.settings["db_url"])

        async with self.pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS profile
                    (
                        id              BIGSERIAL,
                        profile_id      BIGINT NOT NULL UNIQUE,
                        balance         BIGINT DEFAULT 1000,
                        class_id        SMALLINT DEFAULT 1,
                        rank_id         SMALLINT DEFAULT 0
                    );
                    """
                )

    async def setup_hook(self) -> None:
        await self.init_db()
        cogs_folder = f"{os.path.abspath(os.path.dirname(__file__))}/commands"
        for filename in os.listdir(cogs_folder):
            if filename.endswith(".py"):
                await client.load_extension(f"commands.{filename[:-3]}")

    async def on_ready(self):
        """ Event that is processed when bot is ready and runs needed functions"""
        print(f'{self.user.name} has successfully logged in.')


intents = Intents(value=33539)


client = EternalClient(command_prefix="$", intents=intents)

client.run(client.settings['token'])
