#(©)Codexbotz

from pyrogram import __version__
from bot import Bot
from config import *
from pyrogram import enums
from pyrogram.types import Message, InputMediaPhoto, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

message_content = '''👋 Hey {first} 🏆\n
🎖️ Available Plans :\n
● 149 rs For 1 Month Prime Membership\n
● 399 rs For 3 Months Prime Membership\n
● 699 rs For 6 Year Prime Membership\n\n
💵 UPI ID - <a href="https://t.me/Syfer_Admin_Bot">Contact Syfer</a>\n\n
📸 QR - <a href="https://envs.sh/UvX.jpg">ᴄʟɪᴄᴋ ʜᴇʀᴇ ᴛᴏ ꜱᴄᴀɴ</a>\n\n
♻️ <b>Please Contact Admin For Any Type Of Support You Want From Us !!\n\n
‼️ ᴍᴜsᴛ sᴇɴᴅ sᴄʀᴇᴇɴsʜᴏᴛ ᴀғᴛᴇʀ ᴘᴀʏᴍᴇɴᴛ</b>'''

@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data
    if data == "about":
        await query.message.edit_text(
            text = f"<b>○ 𝐎ᴡɴᴇʀ : <a href='https://t.me/Syfer_Admin_Bot'>Syfer</a></b>\n\nBaaki Kuch Nahi Batane wala 👽👍😂",
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
            InlineKeyboardButton('📬Contact OWNER to Buy a Plan 📬', url="https://t.me/Syfer_Admin_Bot")
        ],[
            InlineKeyboardButton(' ᴄʟᴏꜱᴇ ', callback_data='close')
        ]]
        reply_markup = InlineKeyboardMarkup(btn)
        await query.message.reply_photo(
            photo=("https://envs.sh/UvX.jpg"),
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
