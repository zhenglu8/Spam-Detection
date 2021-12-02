from discord.ext import commands
import asyncio
from Filter import *
from Stemming import *
import pyrebase

firebaseConfig = {
    'apiKey': "AIzaSyA_bFpa4nY1erQO9g4tN8V416wZgQWkN2E",
    'authDomain': "antispam-bb7ee.firebaseapp.com",
    'projectId': "antispam-bb7ee",
    'storageBucket': "antispam-bb7ee.appspot.com",
    'messagingSenderId': "833403425944",
    'appId': "1:833403425944:web:d453677ebb3551f381aced",
    'measurementId': "G-GYNG4PT4GX",
    'databaseURL': "https://antispam-bb7ee-default-rtdb.firebaseio.com/"
}

firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()

# discord client
client = commands.Bot(command_prefix="?")


@client.event
async def on_ready():
    print("ready")
    print('Logged in as {0.user}'.format(client))
    while True:
        # print("cleared")
        await asyncio.sleep(10)
        with open("spam_detect.txt", "r+") as file:
            file.truncate(0)


@client.event
async def on_message(message):

    # define punctuation
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''

    # message to lowercase and remove punctuation
    cleaned_message = message.content.lower()
    no_punctuation = ""
    for char in cleaned_message:
        if char not in punctuations:
            no_punctuation = no_punctuation + char

    # stemming message and add to array list
    stemming = []
    stemmed_message = word_tokenize(no_punctuation)
    for a in stemmed_message:
        stemming.append(ps.stem(a))

    print(stemming)

    # counter for spam message
    spam_counter = 0

    if classify(message.content) == 0:
        print(
            "Not spam, start checking Banned Word List")

        # check in ban word list
        check = any(item in stemming for item in new_list)
        if check:
            await message.channel.send('WARNING!! We detected banned words!')
            print("Found in Banned Word List")
        else:
            print("Not Found in Banned Word List")
    else:
        # retrieve data key and count number of ID
        data = db.child("Spam Sender").order_by_child(
            "User ID").equal_to(message.author.id).get()

        for user in data.each():
            if user.val()['User ID'] == message.author.id:
                key = user.key()

        for user in data.each():
            spam_counter = spam_counter + 1
            print(user.key())
            print(user.val())

        if spam_counter >= 1:
            await message.guild.ban(message.author, reason="spam message")
            await asyncio.sleep(1)
            await message.guild.unban(message.author)
            db.child("Spam Sender").child(key).child("User ID").remove()
            print("spam sender - second spam, kick out")
        else:
            db.child("Spam Sender").push(
                {"User ID": message.author.id})
            print("spam sender - first spam")
            await message.channel.send('WARNING!! We detected spam words!')


# Use your own token
client.run("OTEzMzAxNDQ0Mjg1ODQ5NjYw.YZ8gQA.yCskiJMpoEEBPA_C0AsukbfeCZk")
