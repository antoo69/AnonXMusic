from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from config import LOGGER_ID, LOG  # Menggunakan LOGGER_ID
from AnonXMusic import app
from AnonXMusic.utils.database import delete_served_chat, get_assistant
from html import escape

async def is_on_off(log_status):
    log_value = getattr(log_status, "value", log_status)  # Hindari None
    print(f"LOG value at runtime: {log_value}")  # Debugging
    return bool(log_value)

@app.on_message(filters.new_chat_members)
async def join_watcher(_, message: Message):
    try:
        if not await is_on_off(LOG):
            print("LOG is turned off. Skipping join_watcher...")
            return

        print("New chat member detected.")
        userbot = await get_assistant(message.chat.id)
        if not userbot:
            print("Userbot not found for this chat.")
            return

        chat = message.chat
        for member in message.new_chat_members:
            if member.id == app.id:
                print("Bot added to a new group.")
                count = await app.get_chat_members_count(chat.id)
                username = message.chat.username if message.chat.username else "Private Chat"
                added_by = message.from_user.mention if message.from_user else "Unknown User"

                button_url = f"tg://user?id={message.from_user.id}" if message.from_user else "#"
                chat_username = f"@{message.chat.username}" if message.chat.username else "no username"

                msg = (
                    f"**Music Bot Added in a New Group #New_Group**\n\n"
                    f"**Chat Name:** {message.chat.title}\n"
                    f"**Chat ID:** {message.chat.id}\n"
                    f"**Chat Username:** {chat_username}\n"
                    f"**Chat Member Count:** {count}\n"
                    f"**Added By:** {added_by}"
                )

                await app.send_message(
                    LOGGER_ID,  # Menggunakan LOGGER_ID
                    text=msg,
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton("Added By", url=button_url)]]
                    ),
                )
                print("Log message sent to LOGGER_ID.")

                if username != "Private Chat":
                    await userbot.join_chat(f"{username}")
    except Exception as e:
        print(f"Error in join_watcher: {e}")

@app.on_message(filters.left_chat_member)
async def on_left_chat_member(_, message: Message):
    try:
        if not await is_on_off(LOG):
            print("LOG is turned off. Skipping on_left_chat_member...")
            return
        print("A member left the chat.")

        userbot = await get_assistant(message.chat.id)
        if not userbot:
            print("Userbot not found for this chat.")
            return

        left_chat_member = message.left_chat_member
        if left_chat_member and left_chat_member.id == app.id:
            print("Bot removed from the group.")

            remove_by = message.from_user.mention if message.from_user else "Unknown User"
            title = message.chat.title
            username = f"@{message.chat.username}" if message.chat.username else "Private Chat"
            chat_id = message.chat.id
            left = (
                f"✫ <b><u>#Left_group</u></b> ✫\n"
                f"Chat Name: {title}\n"
                f"Chat ID: {chat_id}\n\n"
                f"Removed By: {remove_by}"
            )
            await app.send_message(LOGGER_ID, text=left)  # Menggunakan LOGGER_ID
            print("Log message sent to LOGGER_ID.")

            await delete_served_chat(chat_id)
            await userbot.leave_chat(chat_id)
    except Exception as e:
        print(f"Error in on_left_chat_member: {e}")
