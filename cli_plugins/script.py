from bot import Cli
from pyrogram import filters
from pyrogram.types import MessageEntity 
from helper.db_tools import *
import emoji
import json
import re
import re
from pyrogram.types import InputMediaPhoto, InputMediaVideo
from pysondb import db 
ads_Setting_file_path = "/root/postchi/ads.json"
def get_ad_text(channel_id):
    with open(ads_Setting_file_path , "r") as f :
        data = json.load(f)
        print(data)
        if str(channel_id) not in data:
            return False
        channel_details = data[str(channel_id)]
        if channel_details['status']==False:
            return False
        
        if channel_details['text']==None:
            return False
        
        
        return channel_details['text']
        








def remove_telegram_links_and_usernames(text, replacement_username):
    pattern = r'\b(t\.me/[\w/]+)|(@\w+)\b'
    list_of_banned_emojis = ["🌐", "🆔", "✔️", "|", "LINK","🆑"]
    
    for i in list_of_banned_emojis:
        text = text.replace(i, '')

    cleaned_text = re.sub(pattern, "🆔 "+replacement_username, text)
    
    if cleaned_text==text:
        cleaned_text+="🆔 "+replacement_username
    return cleaned_text




async def check_filtered_keywords(_,__,message):
    # print(message)
    try:
        channel_id  = message.sender_chat.id
        data = get_mabda_chat_data(chat_id=int(channel_id))
        kw = data['keyword']
        
        
        list_of_words=[]

        if ',' in kw:
                list_of_words = kw.split(',')
                
        if message.text:
            if len(list_of_words)>0:
                for i in list_of_words:
                    if i in message.text:
                        print("Sending")
                        return True
                return False   
            else:
                if kw in message.text:
                    print("Sending")
                    return True 
        elif message.caption:
            if len(list_of_words)>0:
                for i in list_of_words:
                    if i in message.caption:
                        print("Sending")
                        return True
                return False 
            else:
                if kw in message.caption:
                    print("Sending")
                    return True
        else:
            return 
    except Exception as e :
        return False

async def check_quto(_,__,message):
    try:
        channel_id  = message.sender_chat.id
        data =get_mabda_chat_data(chat_id=int(channel_id))
        number_of_messages_per_day = data['message_per_day']
        sent_messages = data['sent_messages']
        if number_of_messages_per_day!='':
            if sent_messages==0:
                print("Sending")
                return True
            else:
                if sent_messages==number_of_messages_per_day:
                    return False
                elif number_of_messages_per_day>sent_messages:
                    print("Sending")
                    return True
        else:
            return True
    except:
        return False




def remove_mentions_and_links(text, entities, new_username: str="username") -> str:
    if not entities:
        return text+f'\n{new_username}'

    new_text = text
    for entity in sorted(entities, key=lambda e: e.offset):
      
        if str(entity.type) in ["MessageEntityType.MENTION","MessageEntityType.TEXT_MENTION"]:
            start_oft_text = int(entity.offset)
            end_oft_text = int(entity.offset+entity.length)
            new_text= text[:start_oft_text]+new_username+text[end_oft_text:]

            
    return new_text








async def check_if_channel_is_target(_,__,message):
    try:
        channel_id  = message.sender_chat.id
        for i in read_maghsad_chats():
            if channel_id in i['targets']:
                print("Sending")
                print("Channel is target")
                return True
        return False    
    except Exception as e:
        # print(e)
        return False
        



def remove_emojis(text):
    return emoji.demojize(text, delimiters=("", ""))

    
   
have_filtered_words = filters.create(func=check_filtered_keywords)
can_redirect = filters.create(func=check_quto)
is_target = filters.create(func=check_if_channel_is_target)


async def transfer_media_group(client, message):
    # Check if the message is part of a media group
    if not message.media_group_id:
        print("This message is not part of a media group.")
        return
    m = message
    if m.entities or m.caption_entities:
        
        entities = ''
        if m.entities:
            entities= m.entities
        elif m.caption_entities:
            entities= m.caption_entities
        for entity in sorted(entities, key=lambda e: e.offset):
            if str(entity.type) in ["MessageEntityType.TEXT_LINK", "MessageEntityType.URL"]:
                return
        

    # Get all messages in the media group
    media_group = await client.get_media_group(message.chat.id, message.id)
    
    # Create a directory to store downloaded files
    if not os.path.exists("temp_downloads"):
        os.makedirs("temp_downloads")

    # Download and prepare media for sending

    channel_id = m.sender_chat.id
    chat_ids = []
    for i in read_maghsad_chats():
        
        if int(channel_id) in i['targets']:
            chat_ids.append(i)


    media_list = []
    for msg in media_group:
        
        if msg.photo:
            file_path = await msg.download("temp_downloads/")
            media_list.append(InputMediaPhoto(file_path))
        elif msg.video:
            file_path = await msg.download("temp_downloads/")
            media_list.append(InputMediaVideo(file_path))

    if m.caption:
                
                
                print("im in ")
                # Message is Media type and  Has a caption
                
                # for b in chat_ids:
                for i in chat_ids:
                            print(i)
                 
                            try:
                                   
                                chat_numeral_id = i['_id']
                                chat_username = get_maghsad_chat(chat_id=int(chat_numeral_id))['username']
                                caption = remove_mentions_and_links(m.caption,m.caption_entities,new_username=get_emoji(i['_id'])+' @'+chat_username)
                                cleaned_caption = caption
                                if get_ad_text(chat_numeral_id)!=False:
                                    cleaned_caption+="\n\n"+ get_ad_text(chat_numeral_id)
                                if media_list:
                                    media_list[0].caption = cleaned_caption
                                a = await client.send_media_group(i['_id'], media_list )
                                print("[✓] Message Album redirected to {}".format(chat_username))
                            except Exception as e :
                                print(f"[X ERROR REDIRECTING MESSAGE] {e}")    
                
     
     
     
    else:
        for i in chat_ids:
            try:
                await client.send_media_group(i, media_list)
            except Exception as e :
                print(e)  
                
            
                        
    for media in media_list:
        os.remove(media.media)
    return
    # Send the media group to the target chat
      

    # Clean up downloaded files


    # Remove the temporary directory
    os.rmdir("temp_downloads")

    await message.reply("Media group transferred successfully!")
    
    
@Cli.on_message(have_filtered_words & can_redirect & is_target)
async def redirect_message(c,m):
    print("redirecting message")
    # print(m.entities)
    # print(m.caption_entities)
    # print(m)
    
    if m.media_group_id:
        # print("Sending media group")
        await transfer_media_group(c,m)
        return
    
    
    # if m.entities or m.caption_entities:
    #     print("has entity")
    #     entities = ''
    #     if m.entities:
    #         entities= m.entities
    #     elif m.caption_entities:
    #         entities= m.caption_entities
    #     for entity in sorted(entities, key=lambda e: e.offset):
    #         if str(entity.type) in ["MessageEntityType.TEXT_LINK", "MessageEntityType.URL"]:
    #             return
        

    
    print("[New Message] : from {} | {} | {}".format(
        m.sender_chat.title,m.sender_chat.username,m.sender_chat.id
    ))
    
    channel_id = m.sender_chat.id
    chat_ids = []
    for i in read_maghsad_chats():
        
        if int(channel_id) in i['targets']:
            chat_ids.append(i['_id'])







    if m.caption:
                # Message is Media type and  Has a caption
                
                for b in chat_ids:
                    for i in read_maghsad_chats():
                        if b==i['_id']:
                            try:
                                chat_numeral_id = i['_id']
                                chat_username = get_maghsad_chat(chat_id=int(chat_numeral_id))['username']
                                caption = remove_mentions_and_links(m.caption,m.caption_entities,new_username=get_emoji(i['_id'])+' @'+chat_username)
                                cleaned_caption = caption
                                if get_ad_text(chat_numeral_id)!=False:
                                    cleaned_caption+="\n\n"+ get_ad_text(chat_numeral_id)
                                await m.copy(chat_id=i['_id'],caption=cleaned_caption)
                                print("[✓] Message redirected to {}".format(chat_username))
                            except Exception as e :
                                print(f"[X ERROR REDIRECTING MESSAGE] {e}")    
                        # current_sent_messages = get_mabda_chat_data(chat_id=m.sender_chat.id)['sent_messages']
                        # new_sent_messages = int(current_sent_messages)+1
                        # mabda.update_one({"_id":m.sender_chat.id},{"$set":{"sent_messages":new_sent_messages}})
                        # save_mabda_chats()

            
    elif m.text:
                

                             
                for b in chat_ids:
                    for i in read_maghsad_chats():
                        if b==i['_id']:
                            try:
                                chat_numeral_id = i['_id']
                                
                                chat_username = get_maghsad_chat(chat_id=int(chat_numeral_id))['username']
                                text= remove_mentions_and_links(m.text,m.entities,new_username=get_emoji(i['_id'])+' @'+chat_username)
                                message_cleaned_text = text
                                if get_ad_text(chat_numeral_id)!=False:
                                    message_cleaned_text+="\n\n"+ get_ad_text(chat_numeral_id)
                                await c.send_message(chat_id=chat_numeral_id,text=get_emoji(i['_id'])+' '+message_cleaned_text)
                                print("[✓] Message redirected to {}".format(chat_username))
                            except Exception as e :
                                print(f"[X ERROR REDIRECTING MESSAGE] {e}")   
                                pass 
                            
                            # current_sent_messages = get_mabda_chat_data(chat_id=m.sender_chat.id)['sent_messages']
                            # new_sent_messages = int(current_sent_messages)+1
                            # mabda.update_one({"_id":m.sender_chat.id},{"$set":{"sent_messages":new_sent_messages}})
                            # save_mabda_chats() 
            
