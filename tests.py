import os
import pymongo
import json
from configs.configs import *
from pykeyboard import InlineKeyboard , InlineButton
client = pymongo.MongoClient(mongo_string)
db = client['postchi']
admin_collection = db["admin"]
mabda = db['chats']
bot_settings = db['settings']
maghsad = db['destination_chats']

#_______________________ mabda

maghsad.delete_many({})
mabda.delete_many({})
admin_collection.delete_many({})














