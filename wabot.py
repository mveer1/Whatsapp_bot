import datetime, json, requests

class WABot():
    def __init__(self, json): 
        self.json = json                             #it will be received by WebHook
        self.dict_messages = json['messages']
        self.APIUrl = 'https://eu41.chat-api.com/instance12345/'
        self.token = 'abcdefg'

    #method determines the Chat API method be called.
    #data contains the data required for sending.
    def send_requests(self, method, data):
        url = f"{self.APIUrl}{method}?token={self.token}"
        headers = {'Content-type': 'application/json'}
        answer = requests.post(url, data=json.dumps(data), headers=headers)
        return answer.json()

    # chatId – ID of the chat where the message should be sent
    # Text – Text of the message
    def send_message(self, chatId, text):
        data = {"chatId" : chatId,
                "body" : text}
        answer = self.send_requests('sendMessage', data)
        return answer

    # chatId – ID of the chat where the message should be sent
    # noWelcome – Boolean type variable defining the text to be sent to a chat: welcome or command list. This is the False by default.
    def welcome(self,chatId, noWelcome = False):
        welcome_string = ''
        if (noWelcome == False):
            welcome_string = "WhatsApp Demo Bot Python\n"
        else:
            welcome_string = """Incorrect command
        Commands:
        1. chatId - show ID of the current chat
        2. time - show server time
        3. me - show your nickname
        4. file [format] - get a file. Available formats: doc/gif/jpg/png/pdf/mp3/mp4
        5. ptt - get a voice message
        6. geo - get a location
        7. group - create a group with the bot"""
        return self.send_message(chatId, welcome_string)

    # chatId Output
    def show_chat_id(self,chatId):
        return self.send_message(chatId, f"Chat ID : {chatId}")

    # Time Output
    def time(self, chatId):
        t = datetime.datetime.now()
        time = t.strftime('%d:%m:%Y')
        return self.send_message(chatId, time)

    # “me” Function
    # Outputs information about your companion's name by the “me” command
    def me(self, chatId, name):
        return self.send_message(chatId, name)


    # chatId – ID of the chat where the message should be sent
    # format – is the format of the file to be sent. All files to be sent are stored on the server-side.
    def file(self, chatId, format):
        availableFiles = {'doc' : 'document.doc',
                        'gif' : 'gifka.gif',
                        'jpg' : 'jpgfile.jpg',
                        'png' : 'pngfile.png',
                        'pdf' : 'presentation.pdf',
                        'mp4' : 'video.mp4',
                        'mp3' : 'mp3file.mp3'}
        if format in availableFiles.keys():
            data = {    'chatId' : chatId,
                        'body': f'https://domain.com/Python/{availableFiles[format]}',
                        'filename' : availableFiles[format],
                        'caption' : f'Get your file {availableFiles[format]}'}
        return self.send_requests('sendFile', data)


    #"ptt" Function
    # Sends a voice message to the chat room
    def ptt(self, chatId):
        data = {
        "audio" : 'https://domain.com/Python/ptt.ogg',
        "chatId" : chatId }
        return self.send_requests('sendAudio', data)


    # chatId – ID of the chat where the message should be sent
    # lat – predefined coordinates
    # lng – predefined coordinates
    # address – this is your address or any string you need.
    def geo(self, chatId):
        data = {
            "lat" : '51.51916',
            "lng" : '-0.139214',
            "address" :'Your address',
            "chatId" : chatId
        }
        answer = self.send_requests('sendLocation', data)
        return answer

    #“group” Function
    # Makes a group between you and the bot
    def group(self, author):
        phone = author.replace('@c.us', '')
        data = {
            "groupName" : 'Group with the bot Python',
            "phones" : phone,
            'messageText' : 'It is your group. Enjoy'
        }
        answer = self.send_requests('group', data)
        return answer
    # author – the JSON body sent by the WebHook with information on the message sender.
    # The body contains information about the user number, but with additional characters. Let's call the replace function and delete them, keeping only the phone number:
    # phone = author.replace('@c.us', '')
    # phones – all the necessary participants' phone numbers; you can also send an array of several phone numbers
    # messageText – The first message in the conference
    # We send a request with the 'group' method


    def processing(self):
        if self.dict_messages != []:
            for message in self.dict_messages:
                text = message['body'].split()
                if not message['fromMe']:
                    id  = message['chatId']
                    if text[0].lower() == 'hi':
                        return self.welcome(id)
                    elif text[0].lower() == 'time':
                        return self.time(id)
                    elif text[0].lower() == 'chatId':
                        return self.show_chat_id(id)
                    elif text[0].lower() == 'me':
                        return self.me(id, message['senderName'])
                    elif text[0].lower() == 'file':
                        return self.file(id, text[1])
                    elif text[0].lower() == 'ptt':
                        return self.ptt(id)
                    elif text[0].lower() == 'geo':
                        return self.geo(id)
                    elif text[0].lower() == 'group':
                        return self.group(message['author'])
                    else:
                        return self.welcome(id, True)
                else: return 'NoCommand'
    # We will call this function for each time we receive data in our WebHook
    #     We may receive several messages in a single request, and our bot must process them all. To do this, we are going through all the dictionaries which have a dict_messages list.

    # for message in self.dict_messages:
    # text = message['body'].split()

    #     We declare a variable text — which will be a list of words contained in our message — after entering the loop. To do this, we turn to the message dictionary using the ['body'] key to get the text of the incoming message and just call the split() function, which allows us to split the text into words.
    # We then check if the incoming message is not coming from ourselves by referring to the 'fromMe' key which contains True or False values and validates who the message was from.
    # Prepared a manual on how to write a bot whatsapp on a python
    # If this test is not performed, the bot may become an infinite recursion.
    # We now get the chat id from the same message dictionary using the ['chatId'] key. We address the first element of the word list, put it in the lower case so that the bot could react to messages written by UPPERCASE or MiXeD cAsE and then compare it with the commands we need.
    # Then we just call the functionality we described in the previous steps with the id parameter.
    # Congratulations, our bot is ready!) So now we can fully react to incoming messages.
    # You only need to substitute both your token from your account and the instance number.
    