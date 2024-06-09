import os
import time
import asyncio 
import datetime
from bot import ADMIN
from helper.database import db
from pyrogram.types import Message
from pyrogram import Client, filters

@app.on_message(filters.command("users") & filters.user(ADMIN))
async def get_stats(bot, message):
    mr = await message.reply('**𝙰𝙲𝙲𝙴𝚂𝚂𝙸𝙽𝙶 𝙳𝙴𝚃𝙰𝙸𝙻𝚂.....**')
    total_users = await db.total_users_count()
    await mr.edit( text=f"🔍 TOTAL USER'S = `{total_users}`")

@app.on_message(filters.command("broadcast") & filters.user(ADMIN) & filters.reply)
async def broadcast_handler(bot: Client, m: Message):
    all_users = await db.get_all_users()
    broadcast_msg = m.reply_to_message
    sts_msg = await m.reply_text("broadcast started !") 
    done = 0
    failed = 0
    success = 0
    start_time = time.time()
    total_users = await db.total_users_count()
    async for user in all_users:
        sts = await send_msg(user['id'], broadcast_msg)
        if sts == 200:
           success += 1
        else:
           failed += 1
        if sts == 400:
           await db.delete_user(user['id'])
        done += 1
        if not done % 20:
           await sts_msg.edit(f"Broadcast in progress:\nnTotal Users {total_users}\nCompleted: {done} / {total_users}\nSuccess: {success}\nFailed: {failed}")
    completed_in = datetime.timedelta(seconds=int(time.time() - start_time))
    await sts_msg.edit(f"Broadcast Completed:\nCompleted in `{completed_in}`.\n\nTotal Users {total_users}\nCompleted: {done} / {total_users}\nSuccess: {success}\nFailed: {failed}")
 
         









