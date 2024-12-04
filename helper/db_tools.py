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

#save and get all saved mabda chats from db
def save_mabda_chats():
    with open('mabda.json','w') as mabda_json_file :
        cursor = mabda.find()
        mabda_chats = list(cursor)
        json.dump(mabda_chats,mabda_json_file,indent=2)
  
#read mabda chats        
def read_mabda_chats():
    if not os.path.exists("mabda.json"):
        save_mabda_chats()
    
    with open("mabda.json",'r') as file :
        data = json.load(file)
    
    return data    


#add aa mabda chat in db      
def add_mabda(chat_id,title):
    try:
        mabda.insert_one({
            "_id":chat_id,
            "title":title,
            "keyword" :"",
            "message_per_day":"",
            "status":False,
            "sent_messages":0,
            "renewal_time":"",
        })
        save_mabda_chats()
    except :
        pass    


#delete a mabda chat
def delete_mabda_chat(chat_id):
  try:
      mabda.delete_one({'_id':chat_id})
      save_mabda_chats()
  except:
      pass


#get info of a mabda chat
def get_mabda_chat_data(chat_id):
    for chat in read_mabda_chats():
        # print(chaprintt)
        # ('chat id : {}'.format(chat['_id']))
        if chat['_id']==chat_id:
            return chat

#get kb of list of mabda chats
def make_mabda_keyboard()->list:
    kb = InlineKeyboard(row_width=2)
    list_of_buttons = []
    mabdaa_chats = read_mabda_chats()
    if len(mabdaa_chats)==0:
         list_of_buttons.append(
            InlineButton(" ∙ هنوز چتی اضافه نشده ∙ ","manage_mabda_chats")
        )       
    else:
        for i in mabdaa_chats:
            chat_title = '∙ '+i['title']+' ∙' if len(i['title'])<=21 else  '∙ '+i['title'][:21]+' ∙'
            list_of_buttons.append(
            InlineButton(chat_title,'mabda_chat:'+str(i['_id']))
            )
        
    kb.add(*list_of_buttons)
    kb.row(

            InlineButton(' بازگشت ❯',"manage_mabda_chats")

    )
    
    return kb
                
                
                
                
#setting of mabda chats

def save_mabdachat_settings():
    with open('settings.json','w') as bot_users_file :
        cursor = bot_settings.find()
        users = list(cursor)
        json.dump(users,bot_users_file,indent=2)
    
def read_mabdachat_settings():
    if not os.path.exists("settings.json"):
        save_mabdachat_settings()
    
    with open("settings.json",'r') as file :
        data = json.load(file)
    
    return data   


def get_mabdachat_settings():
    for i in read_mabdachat_settings():
        return i
    











def save_admins():
    with open('admins.json','w') as bot_users_file :
        cursor = admin_collection.find()
        users = list(cursor)
        json.dump(users,bot_users_file,indent=2)
        

def read_admins():
    if not os.path.exists("admins.json"):
        save_admins()
    
    with open("admins.json",'r') as file :
        data = json.load(file)
    
    return data   
     
def add_admin(admin_id):
    try:
        admin_collection.insert_one({
            "_id":admin_id
        })
        save_admins()
    except :
        pass  

def delete_admin(admin_id):
  try:
      admin_collection.delete_one({'_id':admin_id})
      save_admins()
  except:
      pass    


def list_admins():
    list_of_admins = []
    for admin in read_admins():
        list_of_admins.append(admin)
        
    return list_of_admins   


def make_admins_kb():
    kb = InlineKeyboard(row_width=1)
    if len(read_admins())==0:
        kb.add(
            InlineButton(" ∙ ادمینی اضافه نشده ∙ ","meow"),
            InlineButton("🔙 بازگشت","back-manage-chat")
        )
        return kb
    for i in read_admins():
        kb.row(
            InlineButton(" ∙ {} ∙ ".format(i['_id']),"delete-admin:{}".format(i['_id']))
        )
    kb.row(
        InlineButton("🔙 بازگشت","back-manage-chat")
    )    

    return kb





















#________________ maghsad
# show ->read

def save_maghsad_chats():
    with open('maghsad_chats.json','w') as maghsad_json_file :
        cursor = maghsad.find()
        users = list(cursor)
        json.dump(users,maghsad_json_file ,indent=2)
        
        
def read_maghsad_chats():
    if not os.path.exists("maghsad_chats.json"):
        save_maghsad_chats()
    
    with open("maghsad_chats.json",'r') as file :
        data = json.load(file)
    
    return data        

#write
def add_maghsad(chat_id,title,username):
    try:
        maghsad.insert_one({
            "_id":chat_id,
            "title":title,
            "username":username,
            "targets":[],
            "emoji":""
        })
        save_maghsad_chats()
    except Exception as e:
        pass

# delete 
def delete_maghsad_chat(chat_id):
    maghsad.delete_one({"_id":chat_id})
    save_maghsad_chats()



def set_emoji_for_maghsad(maghsad_chat_id, emoji):
    try:

        result = maghsad.update_one({"_id": maghsad_chat_id}, {"$set": {"emoji": emoji}})
        save_maghsad_chats()
    except Exception as e:
        print("An error occurred:", e)


def get_emoji(chat_id):
    for i in read_maghsad_chats():
        if i['_id']==chat_id:
            print(i['emoji'])
            return i['emoji']


#make keyboard of the mah=ghsad chats 
def make_maghsad_keyboard():
    kb = InlineKeyboard(row_width=2)
    list_of_buttons = []

    maghsad_chats = read_maghsad_chats()
    # print(maghsad_chats)
    if len(maghsad_chats)==0:
         list_of_buttons.append(
            InlineButton(" ∙ هنوز چتی اضافه نشده ∙ ","manage_maghsad_chats")
        )
         
         

    else:
        for i in maghsad_chats:
            chat_title = '∙ '+i['title']+' ∙' if len(i['title'])<=21 else  '∙ '+i['title'][:21]+' ∙'
            list_of_buttons.append(
            InlineButton(chat_title,'maghsad_chat:'+str(i['_id']))
            )
        

    
    
    kb.add(*list_of_buttons)
    kb.row(

            InlineButton(' بازگشت ❯',"manage_maghsad_chats")

    )
    
    return kb
    
    
#get a maghsad chat info                
def get_maghsad_chat(chat_id):
    for chat in read_maghsad_chats():
        if chat['_id']==chat_id:
            return chat        
        
        
        
        
        
        
        
        
        

#__________________________TARGETS BITCHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH




def add_target(maghsad_chat_id,target_chat_id):
    target_chat_id = int(target_chat_id)
    maghsad_chat_id = int(maghsad_chat_id)
    newvalues = {"$push": {"targets": {"$each": [int(target_chat_id)]}}}
    maghsad.update_one({"_id": maghsad_chat_id}, newvalues)
    save_maghsad_chats()

def remove_target(maghsad_chat_id, target_chat_id):
    target_chat_id = int(target_chat_id)
    maghsad_chat_id = int(maghsad_chat_id)
    myquery = {"_id": maghsad_chat_id}
    newvalues = {"$pull": {"targets": int(target_chat_id)}}
    maghsad.update_one(myquery, newvalues)
    save_maghsad_chats()

def get_targets(maghsad_chat_id)->list:
    maghsad_chat_id = int(maghsad_chat_id)
    for i in read_maghsad_chats():
        # print(i)
        if i['_id']==maghsad_chat_id:
            return i['targets'] 
        
        
        
          
    
def make_targets_kb(maghsad_chat_id):
    maghsad_chat_id = int(maghsad_chat_id)
    list_of_maghsad_targets = get_targets(maghsad_chat_id)
    kb = InlineKeyboard(row_width=2)
    list_of_buttons = []
    mabdaa_chats = read_mabda_chats()
    if len(mabdaa_chats)==0:
         list_of_buttons.append(
            InlineButton(" ∙ هنوز چتی اضافه نشده ∙ ","manage_mabda_chats")
        )       
    else:
        for i in mabdaa_chats:
            if i["_id"] in list_of_maghsad_targets:
                
                chat_title = '∙ ☑️ '+i['title']+' ∙' if len(i['title'])<=10 else  '∙ ☑️ '+i['title'][:10]+' ∙'
                list_of_buttons.append(
            InlineButton(chat_title,'remove-target:'+str(maghsad_chat_id)+'*'+str(i['_id']))
            )
            else:
                chat_title = '∙ '+i['title']+' ∙' if len(i['title'])<=21 else  '∙ '+i['title'][:21]+' ∙'    
                list_of_buttons.append(
            InlineButton(chat_title,'add-target:'+str(maghsad_chat_id)+'*'+str(i['_id']))
            )
            
        
    kb.add(*list_of_buttons)
    kb.row(

            InlineButton(' بازگشت ❯',"manage_mabda_chats")

    )
    
    return kb
        
        
        
# ---------------- shwoing magjad chats for adding to add texts 
def make_ads_maghsad():
    kb = InlineKeyboard(row_width=2)
    list_of_buttons = []

    maghsad_chats = read_maghsad_chats()
    # print(maghsad_chats)
    if len(maghsad_chats)==0:
         list_of_buttons.append(
            InlineButton(" ∙ هنوز چتی اضافه نشده ∙ ","manage_maghsad_chats")
        )
         
         

    else:
        for i in maghsad_chats:
            chat_title = '∙ '+i['title']+' ∙' if len(i['title'])<=21 else  '∙ '+i['title'][:21]+' ∙'
            list_of_buttons.append(
            InlineButton(chat_title,'add_to_ads_chat:'+str(i['_id']))
            )
        

    
    
    kb.add(*list_of_buttons)
    kb.row(

            InlineButton(' بازگشت ❯',"manage_maghsad_chats")

    )
    
    return kb
            