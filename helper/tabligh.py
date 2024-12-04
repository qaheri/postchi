import json
import os
from pykeyboard import InlineKeyboard, InlineButton

maghsad_file_path = "/root/postchi/maghsad_chats.json"
tabligh_settings_storage_file_path = "/root/postchi/ads.json"

# Create maghsads keyboard


def update_ads_file(json_data):
    with open(tabligh_settings_storage_file_path,"r") as f :
        data = json.load(f)
        
    for item in json_data:
        if str(item.get("_id")) not in data:
                
                    data[item.get("_id")] = {
                        "title": item.get("title"),
                        "status": False,
                        "text": None
                    }
                    with open(tabligh_settings_storage_file_path, "w") as f:
                        json.dump(data, f , indent = 2)
            
                    print(" tablicgh channels json updated")     


def show_maghsad_tab_kb():
    with open(maghsad_file_path, "r") as file:
        data = json.load(file)
        

    update_ads_file(data)
    lst = [InlineButton(item.get("title"), callback_data=f'tab:chat_{item.get("_id")}') for item in data]
    lst.append(InlineButton("بازگشت", "back-to-main"))
    
    kb = InlineKeyboard(row_width=1)
    kb.add(*lst)
    return kb

# Show maghsad tabligh info
def show_maghsad_tabligh_info(channel_id):
    if not os.path.exists(tabligh_settings_storage_file_path):
        tmp_dict = {}
        with open(maghsad_file_path, "r") as file:
            data = json.load(file)
            for item in data:
                tmp_dict[item.get("_id")] = {
                    "title": item.get("title"),
                    "status": False,
                    "text": None
                }
        with open(tabligh_settings_storage_file_path, "w") as f:
            json.dump(tmp_dict, f , indent = 2)
    
    with open(tabligh_settings_storage_file_path, "r") as f:
        data = json.load(f)
        if channel_id not in data:
            with open(maghsad_file_path, "r") as file:
                maghsad_data = json.load(file)
                channel_info = next((item for item in maghsad_data if item.get("_id") == channel_id), None)
                if channel_info:
                    data[channel_id] = {
                        "title": channel_info.get("title"),
                        "status": False,
                        "text": None
                    }
            with open(tabligh_settings_storage_file_path, "w") as f:
                json.dump(data, f , indent = 2)
        
        return data[channel_id]

# Update channel tabligh status
def update_channel_tabligh_status(channel_id):
    with open(tabligh_settings_storage_file_path, "r") as f:
        data = json.load(f)
    
    if channel_id in data:
        data[channel_id]['status'] = not data[channel_id]['status']
        with open(tabligh_settings_storage_file_path, "w") as f:
            json.dump(data, f , indent = 2)
        
        print("channel [{channel_id}] status updated [{status}]".format(
            channel_id=channel_id,
            status=data[channel_id]['status']
        ))
    else:
        print(f"Channel {channel_id} not found in the data")

# Update channel tabligh text
def update_channel_tabligh_text(channel_id, text):
    with open(tabligh_settings_storage_file_path, "r") as f:
        data = json.load(f)
    
    if channel_id in data:
        data[channel_id]['text'] = text
        with open(tabligh_settings_storage_file_path, "w") as f:
            json.dump(data, f , indent = 2)
        
        print("channel [{channel_id}] text updated [{text}]".format(
            channel_id=channel_id,
            text=text
        ))
    else:
        print(f"Channel {channel_id} not found in the data")

# Show tabligh panel of the chat
def channel_tabligh_buttons(channel_id):
    kb = InlineKeyboard(row_width=1)
    with open(tabligh_settings_storage_file_path, "r") as f:
        data = json.load(f)
    
    if channel_id in data:
        channel_details = data[channel_id]
        kb.add(
            InlineButton("فعال" if not channel_details['status'] else "غیرفعال", f"tab:status_{channel_id}"),
            InlineButton("تغییر متن تبلیغ", f"tab:text_{channel_id}"),
            InlineButton("بازگشت به لیست", "tab:back"),
        )
    else:
        print(f"Channel {channel_id} not found in the data")
    
    return kb
