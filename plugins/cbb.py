#(©)Codexbotz

from pyrogram import __version__
from bot import Bot
from config import *
from pyrogram import enums
from pyrogram.types import Message, InputMediaPhoto, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

message_content = '''👋 Hey {first}\n
🎖️ Available Plans :\n
● 19 rs For 1 Month Prime Membership\n
● 59 rs For 6 Months Prime Membership\n
● 89 rs For 1 Year Prime Membership\n\n
💵 UPI ID - <code> adil013@fam</code>\n
<b>(Tap to copy UPI Id)</b>\n\n
📸 QR - <a href="https://envs.sh/Ksz.jpg">ᴄʟɪᴄᴋ ʜᴇʀᴇ ᴛᴏ ꜱᴄᴀɴ</a>\n\n
♻️ <b>If payment is not getting sent on above given QR code then inform admin, he will give you new QR code</b>\n\n
‼️ ᴍᴜsᴛ sᴇɴᴅ sᴄʀᴇᴇɴsʜᴏᴛ ᴀғᴛᴇʀ ᴘᴀʏᴍᴇɴᴛ\n\n
<b><blockquote>International Customers <u>Who are not from India</u> Dm directly to the <a href='t.me/DATTEBAYO56'>owner</a></blockquote></b>'''

@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data
    if data == "about":
        await query.message.edit_text(
            text = f"<b>○ Creator : <a href='t.me/faony'>This Person</a>\n○ 𝐎ᴡɴᴇʀ : <a href='https://t.me/DATTEBAYO56'>𝐃ᴀᴛᴛᴇʙᴀʏᴏ</a>\n○ 𝐀ɴɪᴍᴇ 𝐂ʜᴀɴɴᴇʟ : <a href='https://t.me/Anime_Raven'>𝐀ɴɪᴍᴇ 𝐑ᴀᴠᴇɴ</a>\n○ 𝐎ɴɢᴏɪɴɢ 𝐂ʜᴀɴɴᴇʟ : <a href='https://t.me/Ongoing_Anime_Raven'>𝐎ɴɢᴏɪɴɢ 𝐑ᴀᴠᴇɴ</a>\n○ 𝐀ɴɪᴍᴇ 𝐂ʜᴀᴛ : <a href='https://t.me/Anime_Chat_Raven'>𝐀ɴɪᴍᴇ 𝐂ʜᴀᴛ 𝐑ᴀᴠᴇɴ</a></b>",
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
            InlineKeyboardButton(' Send Payment Screenshot (ADMIN)', url="t.me/DATTEBAYO56")
        ],[
            InlineKeyboardButton(' ᴄʟᴏꜱᴇ ', callback_data='close')
        ]]
        reply_markup = InlineKeyboardMarkup(btn)
        await query.message.reply_photo(
            photo=("https://envs.sh/Ksz.jpg"),
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
