import sys
import asyncio

from telethon import TelegramClient, events
from VoiceRecognize import recognizeMessage

from config import *
import logger
import sqlmanager
import chat


selfbot = TelegramClient("session_id", API_ID, API_HASH)
selfbot.start(PHONE_NUMBER,first_name="Andrew", last_name="Pstvt")
# If you have a cloud password, just set field like selfbot.start("PHONE NUMBER", "CLOUD PASSWORD")

#параметры для пользователя по умолчанию
defaultChatParam = chat.Chat(-1, 10, 0)

#проверка получения всех диалогов 
isdialogsinit = False

#получить все диалоги
async def initDialogs():
    global isdialogsinit
    if(isdialogsinit == False):
        try:
            await selfbot.get_dialogs()
            isdialogsinit = True
        except:
            pass

#отлов входящих сообщений
@selfbot.on(events.NewMessage(incoming=True))
async def my_event_handler(event):
    try:
        sender = await event.get_sender()
        if (event.chat_id > 0):
            await initDialogs() #если не вызывать, что черех раз крашится
            r = sqlmanager.sql_get_chat_by_id(cn, event.chat_id)
            nchat = defaultChatParam
            nchat.chatid = event.chat_id
            if r != None:
                nchat = chat.Chat(event.chat_id, r[1], r[2])
            if (event.message.voice) and (event.message.voice.attributes[0].duration < nchat.minlenght or nchat.minlenght == -1):
                logger.logOutput(sender)
                await event.respond('__Пользователь ограничил функцию голосовых сообщений.__')
                await selfbot.delete_messages(event.chat_id, [event.id])
            elif event.message.voice and nchat.isrecognize:
                filename = f"media\\{nchat.chatid}voice{event.message.id}.ogg"
                await selfbot.download_media(message=event.message, file=filename)
                await recognizeMessage(selfbot, event.message.id, event.chat_id, filename)
    except Exception as rf:
        logger.logException(rf)

#отлов исходящих сообщений
@selfbot.on(events.NewMessage(outgoing=True, pattern=r"\A/vm"))
async def outgoing_handler(event):
    try:
        if(event.chat_id > 0):
            await initDialogs()
            cmd = event.message.message.lower().split()
            r = sqlmanager.sql_get_chat_by_id(cn, event.chat_id)
            nchat = defaultChatParam
            nchat.chatid = event.chat_id
            #проверка на команду
            if r != None:
                nchat = chat.Chat(event.chat_id, r[1], r[2])
            if cmd[1] == "setminlenght":
                nchat.minlenght = int(cmd[2])
                sqlmanager.sql_update_or_add_chat(cn, nchat)
                if len(cmd) > 3:
                    if cmd[3] == 'info':
                        if nchat.minlenght == 0:
                            await selfbot.send_message(event.chat_id, "__Вы можете отправлять любые голосовые сообщения__")
                        elif nchat.minlenght == -1:
                            await selfbot.send_message(event.chat_id, "__Вы не можете отправлять голосовые сообщения__")
                        else:
                            await selfbot.send_message(event.chat_id, f"__Вы можете отправлять голосовые сообщения не короче {nchat.minlenght} секунд__")
                logger.logExecuteCommand(
                    f"Minimum voice size for chat with id={nchat.chatid} is set to {nchat.minlenght} seconds")
            elif cmd[1] == "setrecognize":
                nchat.isrecognize = int(cmd[2])
                sqlmanager.sql_update_or_add_chat(cn, nchat)
                if len(cmd) > 3:
                    if cmd[3] == 'info':
                        if nchat.isrecognize:
                            await selfbot.send_message(event.chat_id, "__Включена функция расшифровки голосовых сообщений__")
                        else:
                            await selfbot.send_message(event.chat_id, "__Функция расшифровки голосовых сообщений отключена__")
                logger.logExecuteCommand(
                    f"Recognazion for chat with id={nchat.chatid} is set to {nchat.isrecognize}")
            elif cmd[1] == "print":
                str = ""
                if nchat.minlenght > 0:
                    str += f"__Вы можете отправлять голосовые сообщения не короче {nchat.minlenght} секунд "
                elif nchat.minlenght == 0:
                    str += f"__Вы можете отправлять любые голосовые сообщения "

                if nchat.isrecognize:
                    str += "при условии авторасшифровки__"
                else:
                    str += "__"

                if nchat.minlenght == -1:
                    str = "__Вы не можете отправлять голосовые сообщения__"

                await selfbot.send_message(event.chat_id, str)
                logger.logExecuteCommand(f"Print for users: {str}")

            await selfbot.delete_messages(event.chat_id, [event.id])
    except Exception as err:
        logger.logException(err)


if __name__ == "__main__":
    global cn

    cn = sqlmanager.sql_connect()
    sqlmanager.sql_create_db_if_not_created(cn)
    selfbot.run_until_disconnected() #бесконечный цикл. Функция блокирующая

    cn.cursor().close()
    cn.close()
