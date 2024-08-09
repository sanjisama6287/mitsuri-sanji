#(©)Codexbotz

from pyrogram import __version__
from bot import Bot
from config import *
from pyrogram import enums
from pyrogram.types import Message, InputMediaPhoto, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

message_content = '''👋 Hey {first}\n
🎖️ Available Plans :\n
● 30 rs For 7 Days Prime Membership\n
● 110 rs For 1 Month Prime Membership\n
● 299 rs For 3 Months Prime Membership\n
● 550 rs For 6 Months Prime Membership\n
● 999 rs For 1 Year Prime Membership\n\n
💵 UPI ID - <code> LaysLinks@axl</code>\n
<b>(Tap to copy UPI Id)</b>\n\n
📸 QR - <a href="https://graph.org/file/e9cb7102773a93cd043f2.jpg">ᴄʟɪᴄᴋ ʜᴇʀᴇ ᴛᴏ ꜱᴄᴀɴ</a>\n\n
♻️ <b>If payment is not getting sent on above given QR code then inform admin, he will give you new QR code</b>\n\n
‼️ ᴍᴜsᴛ sᴇɴᴅ sᴄʀᴇᴇɴsʜᴏᴛ ᴀғᴛᴇʀ ᴘᴀʏᴍᴇɴᴛ'''

@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data
    if data == "about":
        await query.message.edit_text(
            text = f"<b>○ Creator : <a href='t.me/wtf69kartik'>This Person</a>\n○ Channel : @LaysLinks \n○ Channel 2  : @Hubxe</b>",
            disable_web_page_preview = True,
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🔒 Close", callback_data = "close")
                    ]
                ]
            )
        )
    
    elif query.data == "plan":
        btn = [[
            InlineKeyboardButton(' Send Payment Screenshot (ADMIN)', url="t.me/TokenPaymentBot")
        ],[
            InlineKeyboardButton(' ᴄʟᴏꜱᴇ ', callback_data='close')
        ]]
        reply_markup = InlineKeyboardMarkup(btn)
        await query.message.reply_photo(
            photo=("https://graph.org/file/e9cb7102773a93cd043f2.jpg"),
            caption=message_content.format(
                first = query.from_user.mention, 
                second = query.from_user.mention
        ),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

        
    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass
