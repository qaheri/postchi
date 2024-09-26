import yaml
with open("configs/configs.yml",'r',encoding='utf-8') as file :
    data = yaml.safe_load(file)

api_id = data['API_ID']
api_hash = data['API_HASH']
bot_token =  data['BOT_TOKEN']
session_string =  data['SESSION_STRING']
admins = data['ADMINS']
mongo_string = data['MONGO_STRING']


#messages

admin_start = data['START_MESSAGE']
chat_added = data['CHAT_ADDED']
loading_chat = data['LOADING_ADD_CHAT']
owner = data['OWNER']