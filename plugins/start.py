#(©)CodeXBotz




import os
import asyncio
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated

from bot import Bot
from helper import b64_to_str,str_to_b64, get_current_time, shorten_url
from config import ADMINS, FORCE_MSG, START_MSG, CUSTOM_CAPTION, DISABLE_CHANNEL_BUTTON, PROTECT_CONTENT
from helper_func import subscribed, encode, decode, get_messages
from database.database import *


async def _human_time_duration(seconds):
    if seconds == 0:
        return "inf"
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append(f'{amount} {unit}{"" if amount == 1 else "s"}')
    return ", ".join(parts)

@Bot.on_message(filters.command('start') & filters.private & subscribed)
async def start_command(client: Bot, message: Message):
    id = message.from_user.id
    if not await present_user(id):
        try:
            await add_user(id)
        except:
            pass

    if message.text.startswith("/start token_"):
        user_id = message.from_user.id
        try:
            ad_msg = b64_to_str(message.text.split("/start token_")[1])
            if int(user_id) != int(ad_msg.split(":")[0]):
                await client.send_message(
                    message.chat.id,
                    "This Token Is Not For You \nor maybe you are using 2 telegram apps if yes then uninstall this one...",
                    reply_to_message_id=message.id,
                )
                return
            if int(ad_msg.split(":")[1]) < get_current_time():
                await client.send_message(
                    message.chat.id,
                    "Token Expired Regenerate A New Token",
                    reply_to_message_id=message.id,
                )
                return
            if int(ad_msg.split(":")[1]) > int(get_current_time() + 72000):
                await client.send_message(
                    message.chat.id,
                    "Dont Try To Be Over Smart",
                    reply_to_message_id=message.id,
                )
                return
            query = {"user_id": user_id}
            collection.update_one(
                query, {"$set": {"time_out": int(ad_msg.split(":")[1])}}, upsert=True
            )
            await client.send_message(
                message.chat.id,
                "Congratulations! Ads token refreshed successfully! \n\nIt will expire after 24 Hour",
                reply_to_message_id=message.id,
            )
            return
        except BaseException:
            await client.send_message(
                message.chat.id,
                "Invalid Token",
                reply_to_message_id=message.id,
            )
            return

    uid = message.from_user.id    
    check = await present_premium(uid)
    if uid not in ADMINS and not check: 
        
        result = collection.find_one({"user_id": uid})
        if result is None:
            temp_msg = await message.reply("Please wait...")
            ad_code = str_to_b64(f"{uid}:{str(get_current_time() + 72000)}")
            ad_url = shorten_url(f"https://telegram.dog/{client.username}?start=token_{ad_code}")
            await client.send_message(
                message.chat.id,
                f"Konnichiva <b>{message.from_user.mention} 🪐</b> \n\nYour Ads token is expired, refresh your token and try again. \n\n<b>Token Timeout:</b> 24 hour \n\n<b><blockquote>What is token?</b> \nThis is an ads token. If you pass 1 ad, you can use the bot for 24 hour after passing the ad.</blockquote>\n\n<b>APPLE/IPHONE USERS COPY TOKEN LINK AND OPEN IN CHROME BROWSER</b>",
                disable_web_page_preview = True,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "Click Here To Generate Token",
                                url=ad_url,
                            )
                        ],[
                            InlineKeyboardButton(
                                "How To Open Links? ", url='https://t.me/+4haHAUyA7CozMmI1'                                                         
                                
                            )
                            
                        ],[
                            InlineKeyboardButton(
                                "Remove All Ads In One Click ", callback_data = "plan"                                                                
                                
                            )
                        ]
                    ]
                ),
                reply_to_message_id=message.id,
            )
            await temp_msg.delete()
            return
        elif int(result["time_out"]) < get_current_time():
            temp_msg = await message.reply("Please wait...")
            ad_code = str_to_b64(f"{uid}:{str(get_current_time() + 72000)}")
            ad_url = shorten_url(f"https://telegram.dog/{client.username}?start=token_{ad_code}")
            await client.send_message(
                message.chat.id,
                f"Hey <b>{message.from_user.mention}</b> \n\nYour Ads token is expired, refresh your token and try again. \n\n<b>Token Timeout:</b> 24 hour \n\n<b><blockquote>What is token?</b> \nThis is an ads token. If you pass 1 ad, you can use the bot for 24 hour after passing the ad.</blockquote>",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "Click Here To Refresh Token",
                                url=ad_url,
                            )
                        ],[
                            InlineKeyboardButton(
                                "How To Open Links? ", url='https://t.me/+4haHAUyA7CozMmI1'                                                         
                                
                            )
                            
                        ],[
                            InlineKeyboardButton(
                                " Remove All Ads In One Click ", callback_data = "plan"                                                                
                                
                            )
                        ]
                    ]
                ),
                reply_to_message_id=message.id,
            )
            await temp_msg.delete()
            return

    text = message.text
    if len(text)>7:
        try:
            base64_string = text.split(" ", 1)[1]
        except:
            return
        string = await decode(base64_string)
        argument = string.split("-")
        if len(argument) == 3:
            try:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
            except:
                return
            if start <= end:
                ids = range(start,end+1)
            else:
                ids = []
                i = start
                while True:
                    ids.append(i)
                    i -= 1
                    if i < end:
                        break
        elif len(argument) == 2:
            try:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
            except:
                return
        temp_msg = await message.reply("Please wait...")
        try:
            messages = await get_messages(client, ids)
        except:
            await message.reply_text("Something went wrong..!")
            return
        await temp_msg.delete()

        for msg in messages:

            if bool(CUSTOM_CAPTION) & bool(msg.document):
                caption = CUSTOM_CAPTION.format(previouscaption = "" if not msg.caption else msg.caption.html, filename = msg.document.file_name)
            else:
                caption = "" if not msg.caption else msg.caption.html

            if DISABLE_CHANNEL_BUTTON:
                reply_markup = msg.reply_markup
            else:
                reply_markup = None

            try:
                await msg.copy(chat_id=message.from_user.id, caption = caption, parse_mode = ParseMode.HTML, reply_markup = reply_markup, protect_content=PROTECT_CONTENT)
                await asyncio.sleep(0.5)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await msg.copy(chat_id=message.from_user.id, caption = caption, parse_mode = ParseMode.HTML, reply_markup = reply_markup, protect_content=PROTECT_CONTENT)
            except:
                pass
        return
    else:
        reply_markup = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Main Channel", url="https://t.me/+Kj9Ud4kzZX41MDE9")],
                [
                    InlineKeyboardButton("😊 About Me", callback_data = "about"),
                    InlineKeyboardButton("🔒 Close", callback_data = "close")
                ]
            ]
        )
        await message.reply_text(
            text = START_MSG.format(
                first = message.from_user.first_name,
                last = message.from_user.last_name,
                username = None if not message.from_user.username else '@' + message.from_user.username,
                mention = message.from_user.mention,
                id = message.from_user.id
            ),
            reply_markup = reply_markup,
            disable_web_page_preview = True,
            quote = True
        )
        return

    
#=====================================================================================##

WAIT_MSG = """"<b>Processing ...</b>"""

REPLY_ERROR = """<code>Use this command as a replay to any telegram message with out any spaces.</code>"""

#=====================================================================================##

    
    
@Bot.on_message(filters.command('start') & filters.private)
async def not_joined(client: Client, message: Message):
    buttons = [
        [
        InlineKeyboardButton(
                "• Join Channel •",
                url = client.invitelink)]
    ]
    try:
        buttons.append(
            [
                InlineKeyboardButton(
                    text = '• Now Click Here •',
                    url = f"https://t.me/{client.username}?start={message.command[1]}"
                )
            ]
        )
    except IndexError:
        pass

    await message.reply(
        text = FORCE_MSG.format(
                first = message.from_user.first_name,
                last = message.from_user.last_name,
                username = None if not message.from_user.username else '@' + message.from_user.username,
                mention = message.from_user.mention,
                id = message.from_user.id
            ),
        reply_markup = InlineKeyboardMarkup(buttons),
        quote = True,
        disable_web_page_preview = True
    )

@Bot.on_message(filters.command('users') & filters.private & filters.user(ADMINS))
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text=WAIT_MSG)
    users = await full_userbase()
    await msg.edit(f"{len(users)} users are using this bot")
    
@Bot.on_message(filters.command('pre') & filters.private & filters.user(ADMINS))
async def add_users(client: Bot, message: Message):
    user_id = int(message.command[1])
    await addpremium_user(user_id) 
    await message.reply_text("Premium access added to the user")
    await client.send_message(
        chat_id=user_id,
        text=f"<b>ᴘʀᴇᴍɪᴜᴍ ᴀᴅᴅᴇᴅ ᴛᴏ ʏᴏᴜʀ ᴀᴄᴄᴏᴜɴᴛ ᴇɴᴊᴏʏ😀\n</b>",
    ) 
                      
@Bot.on_message(filters.command('rem') & filters.private & filters.user(ADMINS))
async def del_users(client: Bot, message: Message):
    user_id = int(message.command[1])
    await delpremium_user(user_id)     
    await message.reply_text("Premium access removed ")
    await client.send_message(
        chat_id=user_id,
        text=f"<b>ᴘʀᴇᴍɪᴜᴍ ʀᴇᴍᴏᴠᴇᴅ ғʀᴏᴍ ʏᴏᴜʀ ᴀᴄᴄᴏᴜɴᴛ🥺\n</b>",
    )                  
    


@Bot.on_message(filters.private & filters.command('broadcast') & filters.user(ADMINS))
async def send_text(client: Bot, message: Message):
    if message.reply_to_message:
        query = await full_userbase()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0
        
        pls_wait = await message.reply("<i>Broadcasting Message.. This will Take Some Time</i>")
        for chat_id in query:
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                await del_user(chat_id)
                blocked += 1
            except InputUserDeactivated:
                await del_user(chat_id)
                deleted += 1
            except:
                unsuccessful += 1
                pass
            total += 1
        
        status = f"""<b><u>Broadcast Completed</u>

Total Users: <code>{total}</code>
Successful: <code>{successful}</code>
Blocked Users: <code>{blocked}</code>
Deleted Accounts: <code>{deleted}</code>
Unsuccessful: <code>{unsuccessful}</code></b>"""
        
        return await pls_wait.edit(status)

    else:
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        await msg.delete()
