#https://github.com/sferreyr/PythonPLCController

import datetime
import asyncio #DISABLE THIS IN LINUX - This version is only relevant for Python 3.3, which does not include asyncio in its stdlib.

import telebot

TOKEN = '541243341123:23423423423423' #Token telegram
CHAT_ID = 511111111  # Obtenido en telegram pertenece a la cuenta.

tb = telebot.TeleBot(TOKEN)
isNotificaciones = False  # Notificaciones Activadas?


class Telegram:

    '''@tb.message_handler(commands=['activar'])
    def send_activate(message):
        isNotificaciones = True

        print("Notificaciones Activadas")
        tb.reply_to(message, f"Notificaciones TELEGRAM Activadas   - [ {datetime.date.today()} ]")

    @tb.message_handler(commands=['desactivar'])
    def send_desactivate(message):
        isNotificaciones = False
        print("Notificaciones TELEGRAM Desactivadas")
        tb.reply_to(message, f"Notificaciones Desactivadas   - [ {datetime.date.today()} ]")

    tb.infinity_polling()
 '''

def enviar_mensaje(text) -> None:
     """Send message."""
     try:
         tb.send_message(CHAT_ID, text=text)

     except OSError:
         print('No se puede enviar mensaje a telegram')


def enviar_mensaje_chequeo(text) -> None:
    """Send message."""
    try:
        tb.send_message(CHAT_ID, text=text, disable_notification=True)

    except OSError:
        print('No se puede enviar mensaje a telegram')

