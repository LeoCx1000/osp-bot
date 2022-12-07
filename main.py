from __future__ import annotations
import os
import io
import logging
import traceback
import asyncio

import asyncpg
import discord
import yaml

from discord.ext import commands
from dotenv import load_dotenv


with open(r"files/config.yaml") as file:
    yaml_data = yaml.full_load(file)

PSQL_CREDENTIALS = {
    "user": f"{yaml_data['PSQL_USER']}",
    "password": f"{yaml_data['PSQL_PASSWORD']}",
    "database": f"{yaml_data['PSQL_DB']}",
    "host": f"{yaml_data['PSQL_HOST']}",
}

_log = logging.getLogger("OSPBot")


class OSPBot(commands.Bot):
    def __init__(self, pool: asyncpg.Pool[asyncpg.Record]):

        self.db = pool
        self.noprefix: bool = False
        self.maintenance: bool = False
        self.started: bool = False
        super().__init__(
            command_prefix=commands.when_mentioned_or("o.", "."),
            intents=discord.Intents.all(),
            status=discord.Status.online,
            activity=discord.Activity(
                type=discord.ActivityType.playing, name="DM me to contact staff"
            ),
            owner_ids=[326147079275675651, 349373972103561218, 438513695354650626],
            case_insensitive=True,
        )

    async def on_message(self, message):
        prefixes = (".",)
        if self.maintenance is True:
            if message.author.id in self.owner_ids:
                await self.process_commands(message)
                return
            if message.content.startswith(prefixes):
                return
            return
        if (
            not message.content.startswith(prefixes)
            and message.author.id in self.owner_ids
            and self.noprefix is True
        ):
            edited_message = message
            edited_message.content = f".{message.content}"
            await self.process_commands(edited_message)
        else:
            await self.process_commands(message)

    async def setup_hook(self) -> None:
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                try:
                    if not str(filename[:-3]) in yaml_data["DelayedLoadCogs"]:
                        await self.load_extension("cogs.{}".format(filename[:-3]))
                        _log.info(f"successfully loaded {filename[:-3]}")
                except:
                    _log.error(f"An error occurred while loading '{filename}'")
                    traceback.print_exc()

        await self.load_extension("jishaku")

    async def on_ready(self):
        if not self.started:
            self.started = True
            for cog in yaml_data["DelayedLoadCogs"]:
                try:
                    await self.load_extension("cogs.{}".format(cog))
                    _log.info(f"successfully loaded {cog}")
                except:
                    _log.error(f"An error occurred while loading '{cog}'")
                    traceback.print_exc()

    async def on_error(self, event_method: str, /, *args, **kwargs) -> None:
        traceback_string = traceback.format_exc()
        _log.error("Error in event %s", event_method)
        await self.wait_until_ready()
        error_channel: discord.TextChannel = self.get_channel(880181130408636456)  # type: ignore
        to_send = (
            f"```yaml\nAn error occurred in an {event_method} event```"
            f"```py\n{traceback_string}\n```"
        )
        if len(to_send) <= 2000:
            await error_channel.send(to_send)
        else:
            await error_channel.send(
                f"```yaml\nAn error occurred in an {event_method} event```",
                file=discord.File(
                    io.BytesIO(traceback_string.encode()), filename="traceback.py"
                ),
            )


async def startup():
    async with asyncpg.create_pool(**PSQL_CREDENTIALS) as pool, OSPBot(pool) as bot:
        discord.utils.setup_logging()
        await pool.execute(
            "CREATE TABLE IF NOT EXISTS userinfo(user_id bigint PRIMARY KEY, birthdate date);"
        )
        await bot.start(yaml_data["botToken"])


if __name__ == "__main__":
    asyncio.run(startup())
