from discord.ext import commands
import json


async def fetch_user(profile_id: int, client: commands.bot) -> dict | None:
    data = client.redis.get(profile_id)

    if data is None:
        async with client.pool.acquire() as conn:
            async with conn.transaction():
                result = await conn.fetchrow("SELECT * FROM profile WHERE profile_id =  $1", profile_id)

                if result is None:
                    return None

                client.redis.set(profile_id, json.dumps(dict(result)))

                data = client.redis.get(profile_id)

    return json.loads(data)
