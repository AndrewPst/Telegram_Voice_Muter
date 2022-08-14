import time
import sqlite3
import logger
import chat

import threading
from threading import Lock

#мьютекс для потокобезопасности
sqlmutex = Lock()

#подключение к базе данных
def sql_connect():
    with sqlmutex:
        try:
            con = sqlite3.connect("allchats.db", check_same_thread=False)
            logger.logBDSuccesfull("sql connected")
            return con
        except Exception as err:
            logger.logException(err)

#проверка наличия и создание базы данных
def sql_create_db_if_not_created(con):
    with sqlmutex:
        try:
            cur = con.cursor()
            cur.execute(
                """CREATE TABLE IF NOT EXISTS chats (chatid INT PRIMARY KEY, minlenght INT, isrecognize INT);""")
            con.commit()
        except Exception as err:
            logger.logException(err)

#обновляем данные либо записываем новые
def sql_update_or_add_chat(con, chat):
    with sqlmutex:
        try:
            cur = con.cursor()
            cur.execute("""INSERT INTO chats (chatid, minlenght, isrecognize)
                            VALUES(?, ?, ?) 
                            ON CONFLICT(chatid) 
                            DO UPDATE SET minlenght=?, isrecognize=?;""",
                            (chat.chatid, chat.minlenght, chat.isrecognize, chat.minlenght,  chat.isrecognize))
            logger.logBDSuccesfull(f"chat with ID={chat.chatid} updated or created")
            con.commit()
        except Exception as err:
            logger.logException(err)

#метод отладки - выводит всю бд
def sql_print_all(con):
    with sqlmutex:
        try:
            cur = con.cursor()
            cur.execute("""SELECT * FROM chats""")
            result = cur.fetchall()
            print(result)
        except Exception as err:
            logger.logException(err)

#возвращает чат по его id
def sql_get_chat_by_id(con, id):
    with sqlmutex:
        try:
            cur = con.cursor()
            cur.execute("""SELECT chatid, minlenght, isrecognize FROM chats WHERE chatid = ?;""",(id,))
            result = cur.fetchone()
            return result
        except Exception as err:
            logger.logException(err)

