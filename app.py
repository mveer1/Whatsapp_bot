from flask import Flask, request, jsonify
from wabot import WABot
import json

app = Flask(__name__)

@app.route('/', methods=['POST'])
def home():
    if request.method == 'POST':
        bot = WABot(request.json)
        return bot.processing()

if(__name__) == '__main__':
    app.run()

# Let's initialize the app variable, which is going to be a FLASK class.

# app = Flask(__name__)

# @app.route('/', methods=['POST'])
# def home():
#     if request.method == 'POST':
#         bot = WABot(request.json)
#         return bot.processing()
# We'll write the path app.route('/', methods = ['POST']) for it. This decorator means that our home function will be called every time our FLASK server is accessed through a post request by the main path.

# We are testing the fact that the server was accessed through the POST method. Now we create an instance of our bot and submit JSON data to it.

# requests.json – lets you get JSON files from the request body sent to our server.

# def home():
# if request.method == 'POST':
#     bot = WABot(request.json)
#     return bot.processing()