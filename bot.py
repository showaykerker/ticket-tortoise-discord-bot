import os
import re

import discord
import dotenv
import ezcord

from cogwatch import watch

from mongo_connection import MongoConnection

dotenv.load_dotenv()

class TicketTortoise(ezcord.Bot):
    def __init__(self):
        super().__init__(
            intents=discord.Intents.default(),
            language="en")
        self.mongo = MongoConnection()
        self.load_cogs("cogs")
        self.add_listener(self.on_events_forward, "on_message")

    @watch(path="cogs", preload=False, debug=False)
    async def on_ready(self):
        print("Bot ready.")

    async def on_events_forward(self, message):
        # Forward message from other robot
        if message.author.bot:
            return
        
        
client = TicketTortoise()
client.run(str(os.getenv("TOKEN")))
