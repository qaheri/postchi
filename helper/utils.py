from pyrogram import filters
from configs.configs import admins
from helper.db_tools import list_admins
import re



async def check_if_user_is_admin(_,__,m):
    try:
        user_id=m.from_user.id
        if user_id in admins:
            return True
        for i in list_admins():
            if int(i['_id'])==user_id:
                return True
        
    except Exception as e :
        print(e)
        return False    
        
    
is_admin = filters.create(func=check_if_user_is_admin)    




async def source_channel(_,__,m):
    pass
    

def remove_links(text):
    url_regex = r'\bhttps?://\S+\b|www\.\S+\b'
    text_without_links = re.sub(url_regex, '', text)
    return text_without_links    