

##########Import##########

from pyrogram import Client
from configs.configs import *
from time import time
import os
print(os.path.abspath("cli_plugins"))
##########Client##########

Cli = Client(
  name = "Cli",
  api_id = api_id,
  api_hash = api_hash,
  app_version = "1.0.0",
  device_model = "Postchi",
  session_string = session_string,
  plugins = dict(root="cli_pluginsa")
  workers = 1
)

class Api(Client):
  def __init__(self):
    super().__init__(
      name = "Api",
      api_id = api_id,
      api_hash = api_hash,
      app_version = "1.0.0",
      device_model = "Postchi",
      bot_token = bot_token,
      plugins = {"root": "api_plugins"},
      workers = 20
    )

  async def start(self):
    await super().start()
    self.uptime = time()
    me = await self.get_me()
    api_id = me.id
    await Cli.start()
    me2 = await Cli.get_me()
    cli_id = me2.id
    await Cli.send_message(me.username, "/start")
    print("Bots are started!")

  async def stop(self, *args):
    await super().stop()
    await Cli.stop()
    print("Bots are stopped!")