from pykeyboard import InlineButton , InlineKeyboard

admin_dash_kb = InlineKeyboard(row_width=1)
admin_dash_kb.add(
            InlineButton(" ∙ مدیریت چنل های مبدا ∙ ","manage_mabda_chats"),
            InlineButton(" ∙ مدیریت چنل های مقصد ∙ ","manage_maghsad_chats"),
            InlineButton(" ∙ مدیریت ادمین ها ∙ ","manage_admins"),
            InlineButton(" ∙ مدیریت تبلیغ ها ∙ ","manage_tabs")
        )
manage_mabda_chats_kb = InlineKeyboard(row_width=1)
manage_mabda_chats_kb.add(
            
            InlineButton(" ∙ نمایش چنل های مبدا ∙ ","show-mabda-chats"),
            InlineButton(" ∙ افزودن چنل مبدا ","add-mabda-chat"),
            InlineButton(" ∙ بازگشت ∙ ","back-to-main")

        )

manage_maghsad_chats_kb = InlineKeyboard(row_width=1)
manage_maghsad_chats_kb.add(
            
            InlineButton(" ∙ نمایش چنل های مقصد ∙ ","show-chats-maghsad"),
            InlineButton(" ∙ افزودن چنل مقصد ∙","add-chat-maghsad"),
            InlineButton(" ∙ بازگشت ∙ ","back-to-main")

        )


back_to_manage_maghsad_chat_kb = InlineKeyboard()
back_to_manage_maghsad_chat_kb.add(
        InlineButton("🔙 بازگشت","back-manage-maghsad-chat")
    )


admin_managment_kb = InlineKeyboard(row_width=1)
admin_managment_kb.add(
    InlineButton(" ∙ نمایش ادمین ها ∙ ","show-admins"),
    InlineButton(" ∙ افزودن ادمین ∙ ","add-admin"),
    InlineButton("🔙 بازگشت","back-manage-chat")
)