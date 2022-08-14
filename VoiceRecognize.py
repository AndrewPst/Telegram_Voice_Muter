from asyncio.log import logger
import logging
import subprocess
import speech_recognition as sr
import logger
import os
from config import *
import asyncio
import concurrent.futures


async def recognizeMessage(selfbot, reply_id, chat_id, path): #распознать голос
    output = ""
    try:
        # конвертировать из .wav формата в mp4 с помощью утилиты ffmpeg
        wavfile = os.path.splitext(path)[0]+".wav"
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        CREATE_NO_WINDOW = 0x08000000
        process = subprocess.run(
            [ffmpeg_path,
                '-y', '-i', path, wavfile],
            shell=True, startupinfo=si, creationflags=CREATE_NO_WINDOW)

        if process.returncode != 0:
            raise Exception("Something went wrong")

        r = sr.Recognizer()
        with sr.AudioFile(wavfile) as source:
            audio = r.record(source)
        try:
            output = r.recognize_google(audio, language="ru-RU") #распознаем с помощью нужного сервиса на нужном языке
        except Exception as err:
            logger.logException(err)

        logger.logExecuteCommand(f"Recognition complated: {output}")
    except Exception as err:
        logger.logException(err)

    #удаляем временные файлы
    try:
        os.remove(path)
        os.remove(wavfile)
    except Exception as err:
        logger.logException(err)

    #отсылаем расшифрованное сообщение
    try:
        await selfbot.send_message(chat_id, f"__Расшифрованное сообщение__:\n {output}", reply_to=reply_id)
    except Exception as e:
        logger.logException(e)
