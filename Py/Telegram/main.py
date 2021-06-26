from cryptography.fernet import Fernet
import requests
import telebot
import json
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Database.models import db, User, UserSchema

def getToken():
    key = bytes(os.getenv("KEY"), "utf-8")
    encrypted = bytes(os.getenv("TELEGRAM_KEY"), "utf-8")
    return json.loads(Fernet(key).decrypt(encrypted))["api_key"]

def createBot():
    TOKEN = getToken()

    bot = telebot.TeleBot(token=TOKEN)

    @bot.message_handler(commands=["start"])
    def _start(message):
        try:
            from utils.REST.helpers import _get_user_prop
        except Exception as err:
            print(err)
            return
        
        try:
            user_schema = UserSchema()
            user = user_schema.load(_get_user_prop(message.json))
            db.session.add(user)
            db.session.commit()

            text = "You are now subscribed to News Bot! ☺♥☻♥"
            bot.send_message(message.chat.id, text, parse_mode=None)
        except Exception as err:
            print(err)
            text = f"Subscription error, please try again\n{err}"
            bot.send_message(message.chat.id, text, parse_mode=None)

    @bot.message_handler(commands=["stop"])
    def _stop(message):
        try:
            username = message.from_user.username
            user = User.query.filter(User.username == username).first()
            db.session.delete(user)
            db.session.commit()

            text = "You have just un-subscribed from News Bot! ☺♥☻♥"
            bot.send_message(message.chat.id, text, parse_mode=None)
        except Exception as err:
            print(err)
            text = f"Subscription error, please try again\n{err}"
            bot.send_message(message.chat.id, text, parse_mode=None)

    return bot

if __name__ == "__main__":
    bot = createBot()