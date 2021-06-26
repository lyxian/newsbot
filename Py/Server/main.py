from flask import Flask, request
import telebot
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Telegram.main import createBot


if __name__ == "__main__":

    app = Flask(__name__)
    bot = createBot()

    PUBLIC_URL = "https://9d8e9893f256.ngrok.io/"
    weburl = PUBLIC_URL + bot.token

    print(weburl)

    @app.route("/stop")
    def stop():
        shutdown_hook = request.environ.get("werkzeug.server.shutdown")
        try:
            shutdown_hook()
            print("--End--")
        except:
            pass

    @app.route("/" + bot.token, methods=["POST"])
    def getMessage():
        try:
            bot.process_new_updates(
                [telebot.types.Update.de_json(request.stream.read().decode("utf-8"))]
            )
            return "!", 200
        except Exception as e:
            print(e)
            return "?", 500

    @app.route("/", methods=["GET", "POST"])
    def webhook():
        if request.method == "GET":
            bot.remove_webhook()
            print("Setting webhook...")
            try:
                bot.set_webhook(url=weburl)
                return "Webhook set!"
            except:
                return "Webhook not set...Try again..."
        elif request.method == "POST":
            print("Wating...")
            return "!", 200

    def start():
        bot.remove_webhook()
        print("Setting webhook...", end=" ")
        try:
            bot.set_webhook(url=weburl)
            print("Webhook set!")
            return "Webhook set!"
        except:
            return "Webhook not set...Try again..."

    start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
