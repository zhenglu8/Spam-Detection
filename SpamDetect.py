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


def func():
    func.variable = 0


# Define counter variable
func()


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
    '''
    counter = 0

    with open("spam_detect.txt", "r+") as file:
        for lines in file:
            if lines.strip("\n") == str(message.author.id):
                counter += 1
        file.writelines(f"{str(message.author.id)}\n")
    '''
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

    if classify(message.content) == 0:
        print(
            "Not spam, start ban word")

        counter = 0
        '''
        people = db.child("Messages").child(message.author.id).order_by_child(
            "counter").equal_to(1).get()
        for person in people.each():
            print(person.val()['discordUsername'])
            if person.val()['discordUsername'] == str(message.author):
                counter = 1
                # db.child("Messages").child(
                # person.key()).update({'counter': 'updated'})
                #print("time to update")
            else:
                counter = 0
        
        db.child("Messages").child(message.author.id).push({'discordUsername': str(
            message.author), 'discordID': message.author.id, 'message': message.content, 'status': 'ham', 'counter': 0})
        '''
        # check in ban word list
        check = any(item in stemming for item in new_list)
        if check:
            await message.channel.send('Warning')
            print("Found in Banned Word List")
        else:
            print("Not Found in Banned Word List")
    else:
        # Spam message, func.variable+1
        #func.variable = func.variable + 1
        '''
        people = db.child("Messages").child(message.author.id).order_by_child(
            "counter").equal_to(0).get()
        for person in people.each():
            print(person.val()['discordUsername'])
            if person.val()['discordUsername'] == str(message.author) and person.val()['counter'] == 0 and person.val()['status'] == 'ham':
                if person.val()['counter'] != 1:
                    # Add Spam to Firebase


        people1 = db.child("Messages").child(message.author.id).order_by_child(
            "counter").equal_to(0).get()

        for person1 in people1.each():

            if person1.val()['discordID'] == message.author.id:
                print("SPAM#1")
                db.child("Messages").child(message.author.id).push({'discordUsername': str(
                    message.author), 'discordID': message.author.id, 'message': message.content, 'status': 'spam', 'counter': 1})
                await message.channel.send('Counter + 1')
                return

        # If Spam second time
        people = db.child("Messages").child(message.author.id).order_by_child(
            "counter").equal_to(1).get()
        for person in people.each():
            print(person.val()['discordUsername'])
            if person.val()['discordUsername'] == str(message.author) and person.val()['counter'] == 1 and person.val()['status'] == 'spam':
                # Add Spam to Firebase
                db.child("Messages").child(message.author.id).push({'discordUsername': str(
                    message.author), 'discordID': message.author.id, 'message': message.content, 'status': 'spam', 'counter': 2})
                #func.variable = 0
                '''
        await message.guild.ban(message.author, reason="spam message")
        await asyncio.sleep(1)
        await message.guild.unban(message.author)
        # await message.channel.send('sends spam message')
        print("spam message sender kick out")

# Use your own token
client.run("OTA2Mjk1MTQ4MjQ0MjM4NDQ2.YYWjIQ.aHLitHDjuTkmWo4NOqHhAUlQtRU")
