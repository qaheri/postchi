from pykeyboard import InlineKeyboard , InlineButton
from bot import Api, Cli
from helper.utils import *
from helper.db_tools import *
from pykeyboard import InlineButton , InlineKeyboard
import jdatetime
from helper.kbs import *
from configs.configs import *
from asyncio import sleep
from pysondb import db 
settings_cache = db.getDb("/root/postchi/settings.json")



def get_current_jalali_datetime():
    return jdatetime.datetime.now().strftime('%Y-%m-%d ساعت  %H:%M')
admin_action = {}



@Api.on_message(is_admin & filters.command(['ads']))
async def handle_ad_text(c,m):
    await m.reply(
        """
ادمین محترم راهنمای بخش افزودن کپشن تبلیغ به شرح زیر هست  : 

اضافه کردن متن تبلیغ :
کافیه برای اینکار متن تبلیغ رو ارسال کنید و عبارت زیر روی اون ریپلای کنید تا متن تبلیغ شما تنظیم بشه 
/setad

حذف متن تبلیغ :
کافیه دستور زیر رو به ربات ارسال کنید 
/noad

 همچنین دیدن مجدد این پیام و راهنمای تبلیغ :
/ads
        
        """
    )
    

@Api.on_message(is_admin & filters.command(['noad']))
async def remove_ad(c,m):
    for i in settings_cache.getAll():
            settings_cache.deleteById(i.get("id"))
    await m.reply("متن تبلیغ با موفقیت حذف و غیرفعال شد !")        
    
    
    
    
@Api.on_message(is_admin & filters.command(['setad']))
async def set_new_ad(c,m):
    if not m.reply_to_message:
        await m.reply("روی متن مورد نظر این دستور را ریپلای کنید ")
        return
    
    current_add= settings_cache.getAll()
    if current_add==[]:
        settings_cache.add(
            {"ad_text" : m.reply_to_message.text}
        )
        await m.reply("متن بالا با موفقیت به عنوان متن تبلیغ تنظیم شد \n\n"+ m.reply_to_message.text)
    
    else:
        for i in settings_cache.getAll():
            settings_cache.deleteById(i.get("id"))
        
        
        settings_cache.add(
            {"ad_text" : m.reply_to_message.text}
        )
        await m.reply("متن بالا با موفقیت به عنوان متن تبلیغ تنظیم شد \n\n"+ m.reply_to_message.text)
                
    
        


   
@Api.on_message(is_admin)
async def handle_admin_messages(c,m):
    
    global admin_action
    user_id = m.from_user.id
    #if user_id not in admin_action:
        #admin_action[user_id]=''
    # print("Admin Action is [ {} ]".format(admin_action))
    user_id = m.from_user.id
    name = m.from_user.first_name
    user_name = f'[{name}](tg://user?id={user_id})'
    text= m.text
    if text=='/start':
        
        admin_action[user_id] ='' 
        await m.reply(text=admin_start,reply_markup=admin_dash_kb)
        
    elif admin_action[user_id]=='add-mabda-chat':
        # print("[ADD MABDA CHANNEL] admin sent a link to add a mabda channel")
        loading = await m.reply(loading_chat)
        if "/" in text:
            text = text.split('/')[-1]
        else:
            text = text.replace("@","")  
        try:      
            await Cli.join_chat(text)
            chat = await Cli.get_chat(text)
            numeral_chat_id = chat.id
            chat_title = chat.title
            add_mabda(chat_id=numeral_chat_id,title=chat_title)
            admin_action[user_id] = ''
            
            chat_setting_kb = InlineKeyboard(row_width=1)
            chat_setting_kb.add(
                InlineButton("⚙️ تنظیمات چنل","settings:{}".format(str(numeral_chat_id))),
                InlineButton("🔙 بازگشت","back-to-main")
            )
            await loading.delete()
            await m.reply(text=chat_added.format(chat_title),reply_markup=chat_setting_kb)
            
        except Exception as e :
            await loading.delete()
            await m.reply(f"خطایی رخ داد با ساپورت ارتباط بگیرید\n<code>{e}</code>",reply_markup=back_to_manage_chat_kb)      
    
    elif admin_action[user_id]=='add_maghsad_chat':
            loading = await m.reply(loading_chat)
            if "/" in text:
                text = text.split('/')[-1]
            else:
                text = text.replace("@","")  
            try:      
                await Cli.join_chat(text)
                chat = await Cli.get_chat(text)
                numeral_chat_id = chat.id
                chat_title = chat.title
                add_maghsad(chat_id=numeral_chat_id,title=chat_title,username=chat.username)
                admin_action[user_id] = ''
                
                chat_setting_kb = InlineKeyboard(row_width=1)
                chat_setting_kb.add(
                    InlineButton("🔙 بازگشت","show-chats-maghsad")
                )
                await loading.delete()
                await m.reply(text=chat_added.format(chat_title),reply_markup=chat_setting_kb)
                
            except Exception as e :
                await loading.delete()
                back_to_manage_chat_kb = InlineKeyboard()
                back_to_manage_chat_kb.add(
                    InlineButton("🔙 بازگشت","show-chats-maghsad")
                )
                await m.reply(f"خطایی رخ داد با ساپورت ارتباط بگیرید\n<code>{e}</code>",reply_markup=back_to_manage_chat_kb)      
        
        
    elif admin_action[user_id].split(":")[0]=='filter-words':
        await m.reply("فیلتر کلمات اعمال شد")
        chat = admin_action[user_id].split(":")[1] 
        mabda.update_one({"_id":int(chat)},{"$set":{"keyword":m.text}})
        save_mabda_chats()
        admin_action[user_id] = ''
    elif admin_action[user_id].split(":")[0]=='filter-numbers':
       await m.reply("فیلتر تعداد پیام های از این چنل اعمال شد")
       chat = admin_action[user_id].split(":")[1]  
       mabda.update_one({"_id":int(chat)},{"$set":{"message_per_day":int(m.text),"sent_messages":0}})
       save_mabda_chats()   
       admin_action[user_id] ='' 
    elif admin_action[user_id]=='add-admin':
        add_admin(m.text)
        a = await m.reply("ادمین با آیدی عددی {} با موفقیت اضافه شد".format(text))   
        admin_action[user_id] ='' 
        await sleep(2)
        await a.edit_text(text=admin_start,reply_markup=admin_dash_kb)
          
    elif admin_action[user_id].split(":")[0]=='set-emoji':
        chat_id = admin_action[user_id].split(":")[1]
        a = await m.reply("با موفقیت ایموجی تیتر اعمال شد")
        admin_action[user_id] = ''
        set_emoji_for_maghsad(maghsad_chat_id=int(chat_id),emoji=m.text)
        await sleep(2)
        await a.edit_text(text=admin_start,reply_markup=admin_dash_kb)
        
        



@Api.on_callback_query()
async def handle_btn(c,q):
    global admin_action
    query =q.data
    # print(query)
    user_id = q.from_user.id
    name = q.from_user.first_name
    user_name = f'[{name}](tg://user?id={user_id})'
    back_to_manage_chat_kb = InlineKeyboard()
    back_to_manage_chat_kb.add(
        InlineButton("🔙 بازگشت","back-manage-chat")
    )
    if user_id not in admin_action:
        admin_action[user_id] = ''
#______________________________________________________________________________________________________
# _________________________________دکمه های مربوط به مدیریت چنل های مقصد _______________________________  
#______________________________________________________________________________________________________
    if query=='manage_maghsad_chats':
        
       
        text_manage = "برای ادامه یکی از گزینه های زیر رو انتخاب کنید \n"
        await q.edit_message_text(text=text_manage,reply_markup=manage_maghsad_chats_kb)
        
    elif  query.split(':')[0]=='maghsad_chat':    
        maghsade_chat =query.split(':')[1]
        data = get_maghsad_chat(chat_id=int(maghsade_chat))
        # print(data)
        maghsad_chat_data_text = 'آیدی عددی : {}\nیوزرنیم : {}\nعنوان : {}\nایموجی : {}'.format(
            data['_id'],
            data['username'],
            data['title'],
            data['emoji']
        )
        
        maghsade_chat_kb = InlineKeyboard(row_width=1)
        maghsade_chat_kb.add(
            InlineButton(" ⁃ چنل های متصل ⁃ ","show-target-chats:{}".format(maghsade_chat)),
            InlineButton(" ⁃ حذف ⁃ ","delete-maghsade_chat:{}".format(maghsade_chat)),
            InlineButton("تعیین ایموجی تیتر","set-emoji:{}".format(maghsade_chat)),
            InlineButton("❯ بازگشت","show-chats-maghsad"),
        )
        await q.edit_message_text(text=maghsad_chat_data_text,reply_markup=maghsade_chat_kb)
    elif query.split(":")[0]=='set-emoji': 
        back_to_manage_chat_kb = InlineKeyboard()
        back_to_manage_chat_kb.add(
        InlineButton("🔙 بازگشت","back-manage-chat")
        )
        admin_action[user_id] = query
        await q.edit_message_text(text="ایموجی مورد نظرتون رو بفرستید : ",reply_markup=back_to_manage_chat_kb)
    elif query.split(":")[0]=='show-target-chats':
        maghsad_chat_id=query.split(":")[1]
        await q.edit_message_text("لیست پنل های مرتبط با مقصد",reply_markup=make_targets_kb(maghsad_chat_id))
    elif query.split(":")[0]=='remove-target':
        maghsad_chat_id = query.split(":")[1].split('*')[0]
        # print("maghsad chat id : {}".format(maghsad_chat_id))
        target_chat_id = query.split(":")[1].split('*')[1]
        # print("target_chat_id : {}".format(target_chat_id))
        remove_target(maghsad_chat_id,target_chat_id)
        await q.edit_message_text("لیست پنل های مرتبط با مقصد",reply_markup=make_targets_kb(maghsad_chat_id))
    
    
    elif query=='add-admin':
        admin_action[user_id] = 'add-admin'
        back_menu = InlineKeyboard()
        back_menu.add(
            InlineButton("✹ بازگشت","back-manage-chat")
        )
        await q.edit_message_text(text='✤ آیدی عددی ادمین مورد نظر رو برای افزودن به لیست ادمین ها وارد کنید',reply_markup=back_menu)
    elif query=='manage_admins':
        if user_id not in owner:
            await q.answer("فقد مالک میتونه")
            return
        await q.edit_message_text(text="✤ برای  ادامه یکی از گزینه ای زیر رو انتخاب کنید",reply_markup=admin_managment_kb)
    
    elif query.split(":")[0]=='delete-admin':
        if user_id not in owner:
            await q.answer("فقد مالک میتونه")
            return 
        admin_id = query.split(":")[1]
        
        await q.answer(text="ادمین مورد نظر با موفقیت حذف شد",show_alert=True)
        
        await q.edit_message_text(text="✤ برای  ادامه یکی از گزینه ای زیر رو انتخاب کنید",reply_markup=admin_managment_kb)
        delete_admin(admin_id)
    
    elif query=='show-admins':
        if user_id not in owner:
            await q.answer("فقد مالک میتونه")
            return
        await q.edit_message_text(text='◆ برای حذف ادمین روی آیدی عددی ادمین کلیک کنید',reply_markup=make_admins_kb())
    
    elif query.split(":")[0]=='add-target':
        maghsad_chat_id = query.split(":")[1].split('*')[0]
        # print("maghsad chat id : {}".format(maghsad_chat_id))
        target_chat_id = query.split(":")[1].split('*')[1]
        # print("target_chat_id : {}".format(target_chat_id))
        add_target(maghsad_chat_id,target_chat_id)
        await q.edit_message_text("لیست پنل های مرتبط با مقصد",reply_markup=make_targets_kb(maghsad_chat_id))
    # elif  query.split(':')[0]=="show-target-chats":    
    #     maghsad =query.split(':')[1]   
    #     pass 
    elif query.split(':')[0]=='delete-maghsade_chat':
       maghsade_chat_to_delete = query.split(':')[1]
       await q.edit_message_text("چنل مقصد حذف شد",reply_markup=back_to_manage_maghsad_chat_kb)
       delete_maghsad_chat(chat_id=int(maghsade_chat_to_delete))
       
    

    elif query.split(":")[0]=='filter-words':
        kb = InlineKeyboard(row_width=1)
        kb.add(
            InlineButton("همه پیام ها","2all:{}".format(query.split(":")[1])),
            InlineButton("🔙 بازگشت","show-mabda-chats")
        )
        text = 'کلمات مورد نظر برای فیلتر شدن در انتسار پیام رو وارد کنید برای بیش از یک کلمه اونها رو با کاما یا ویرگول از هم جدا کنید'      
        await q.edit_message_text(text=text,reply_markup=kb)
        admin_action[user_id] = query
        
    elif query.split(":")[0]=='filter-numbers':
        text = 'تعداد پیام هایی که در روز قصد دارید انتشار داده بشن تو چنل مقصد رو وارد کنید'  
        kb = InlineKeyboard(row_width=1)
        kb.add(
            InlineButton("همه پیام ها","1all:{}".format(query.split(":")[1])),
            InlineButton("🔙 بازگشت","show-mabda-chats")
        )
        await q.edit_message_text(text=text,reply_markup=kb)
        admin_action[user_id] = query
        
    elif query.split(':')[0]=='1all':
        await q.answer("همه پیام های جدید از حالا از پنل مبدا به مقصد ارسال خواهند شد",show_alert=True)
        text = "یکی از گزینه های زیر رو انتخاب کنید"
        admin_action[user_id] = ''
        await q.edit_message_text(text=text,reply_markup=admin_dash_kb)  
        mabda.update_one({"_id":int(query.split(':')[1])},{"$set":{"message_per_day":''}})
        save_mabda_chats()  
        
        
    elif query.split(':')[0]=='2all':
        await q.answer("همه پیام های جدید از حالا از پنل مبدا به مقصد ارسال خواهند شد",show_alert=True)
        text = "یکی از گزینه های زیر رو انتخاب کنید"
        admin_action[user_id] = ''
        await q.edit_message_text(text=text,reply_markup=admin_dash_kb)  
        mabda.update_one({"_id":int(query.split(':')[1])},{"$set":{"keyword":''}})
        save_mabda_chats()     
    
        
    elif query=='add-chat-maghsad':
       
        add_chat_text= """‏ℹ️ بخش افزودن چنل مقصد 
‏ادمین محترم لینک چت مورد نظر یا آیدی چت رو ارسال کنید  """
        admin_action[user_id] = 'add_maghsad_chat'
        await q.edit_message_text(text=add_chat_text,reply_markup=back_to_manage_maghsad_chat_kb)   
        
             

        
        
    elif query.split(":")[0]=='delete-mabda':
        chat = int(query.split(":")[1])
        await q.answer("با موفقیت حذف شد",show_alert=True)
        delete_mabda_chat(chat_id=chat)
        try:
            await Cli.leave_chat(chat, delete=True)
        except:
            pass
        text_manage = "برای ادامه یکی از گزینه های زیر رو انتخاب کنید \n"
        await q.edit_message_text(text=text_manage,reply_markup=make_maghsad_keyboard())
    
    
    elif query=='show-chats-maghsad':
        show_chats_text= """❯ لیست چنل های مقصد | برای ادامه انتخاب کنید

➖➖➖➖➖➖➖"""
        
        await q.edit_message_text(text=show_chats_text,reply_markup=make_maghsad_keyboard())    
    
#______________________________________________________________________________________________________
# _________________________________دکمه های مربوط به مدیریت چنل های مبدا ________________________________   
#______________________________________________________________________________________________________
    elif query=='manage_mabda_chats':
        
        
        text_manage = "برای ادامه یکی از گزینه های زیر رو انتخاب کنید \n"
        await q.edit_message_text(text=text_manage,reply_markup=manage_mabda_chats_kb) 
    
    

    
    elif query=='show-mabda-chats':
        
        show_chats_text= """❯ لیست چنل های مبدا \n برای ادامه انتخاب کنید

➖➖➖➖➖➖➖"""
        
        await q.edit_message_text(text=show_chats_text,reply_markup=make_mabda_keyboard())
    
    elif query=="add-mabda-chat":
        add_mabda_chat_text= """‏ℹ️ بخش افزودن چنل مبدا 
‏ادمین محترم لینک چت مورد نظر یا آیدی چت رو ارسال کنید  """
        # print('changin admin action to add - mabda - chat')
        admin_action[user_id] = 'add-mabda-chat'
        await q.edit_message_text(text=add_mabda_chat_text,reply_markup=back_to_manage_chat_kb)
    
    elif query.split(':')[0]=='mabda_chat':
            data = get_mabda_chat_data(chat_id=int(query.split(':')[1]))
            numeral_id = data['_id']
            title = data['title']
            per_message = data['message_per_day'] if data['message_per_day']!='' else 'همه پیام ها'
            word_filter = data['keyword'] if data['keyword']!='' else "همه پیام ها"
            text ="""• عنوان چنل : {}

• آیدی عددی چنل : {}

• تعداد پیام تنظیم شده : {}

• فیلتر اعمال شده روی پیام ها : {}

📟 برای تنظیمات این چنل از گزینه های زیر میتونید استفاده کنید  : 

➖➖➖➖➖➖➖➖""".format(
    
    title,
    numeral_id,
    per_message,
    word_filter
    
    
    
    
)
            
            chat_setting_kb = InlineKeyboard(row_width=1)
            chat_setting_kb.add(
                InlineButton("⚙️ تنظیمات چنل","settings:{}".format(query.split(':')[1])),
                InlineButton("🔙 بازگشت","show-mabda-chats")
            )
        
            await q.edit_message_text(text=text,reply_markup=chat_setting_kb)    
    

    
    elif query=='back-to-main':
        
        
        admin_dash_text = """سلام ادمین عزیز 👋🏻
ادمین محترم برای ادامه یکی از گزینه های زیر رو انتخاب کنید

[‎ ](https://telegra.ph/file/7dbf04b6aa0c6edb6b143.jpg)""".format(user_name)
        
        await q.edit_message_text(text=admin_dash_text,reply_markup=admin_dash_kb)
    elif query=='back-manage-chat':
        text_manage = "برای ادامه یکی از گزینه های زیر رو انتخاب کنید \n"
        await q.edit_message_text(text=admin_start,reply_markup=admin_dash_kb) 
        admin_action[user_id] = ''
        
        
    elif query=='back-manage-mabda-chat':
        text_manage = "برای ادامه یکی از گزینه های زیر رو انتخاب کنید \n"
        await q.edit_message_text(text=text_manage,reply_markup=manage_maghsad_chats_kb)     
         
         
    elif query.split(':')[0]=='settings':
        chat  = query.split(':')[1]
        chat_setting_kb = InlineKeyboard(row_width=1)
        text = "میتونید اینجا چنل رو مدیریت کنید : "
        chat_setting_kb.row(
            InlineButton("فیلتر کلمات","filter-words:{}".format(chat))
        )  
        chat_setting_kb.row(
            InlineButton("فیلتر تعداد","filter-numbers:{}".format(chat))
        )      
        chat_setting_kb.row(
            InlineButton("حذف","delete-mabda:{}".format(chat))
        ) 
        chat_setting_kb.row(
            InlineButton("🔙 بازگشت","show-mabda-chats")
        )
        await q.edit_message_text(text=text,reply_markup=chat_setting_kb)     
             



