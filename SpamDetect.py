from discord.ext import commands
import asyncio
from filter_new import *

# discord client
client = commands.Bot(command_prefix="?")


@client.event
async def on_ready():
    print("ready")
    print('Logged in as {0.user}'.format(client))
    while True:
        print("cleared")
        await asyncio.sleep(10)
        with open("spam_detect.txt", "r+") as file:
            file.truncate(0)


@client.event
async def on_message(message):
    # counter = 0
    # with open("spam_detect.txt", "r+") as file:
    #     for lines in file:
    #         if lines.strip("\n") == str(message.author.id):
    #             counter += 1
    #
    #     file.writelines(f"{str(message.author.id)}\n")
    #     if counter > 3:
    #         await message.guild.ban(message.author, reason="spam")
    #         await asyncio.sleep(1)
    #         await message.guild.unban(message.author)
    #         print("spam user kick out")

    # ban word list
    wordlist1 = "sell"
    wordlist2 = "bad"
    wordlist3 = "drug"

    counter = 0

    with open("spam_detect.txt", "r+") as file:
        for lines in file:
            if lines.strip("\n") == str(message.author.id):
                counter += 1
        file.writelines(f"{str(message.author.id)}\n")

        if classify(message.content) == 0:
            print("This message is not spam")
            print("Start check message contain ban word")

            # 1. selling stuff in server
            if message.content.find(wordlist1) != -1:
                #
                await message.guild.ban(message.author, reason="selling stuff")
                await asyncio.sleep(1)
                await message.guild.unban(message.author)
                print("selling stuff sender kick out")
            # 2. bad word in server
            elif message.content.find(wordlist2) != -1:
                #
                await message.guild.ban(message.author, reason="bad word")
                await asyncio.sleep(1)
                await message.guild.unban(message.author)
                print("bad word sender kick out")
            # 3. related to drug in server
            elif message.content.find(wordlist3) != -1:
                #
                await message.guild.ban(message.author, reason="related to drug")
                await asyncio.sleep(1)
                await message.guild.unban(message.author)
                print("sender that related to drug kick out")
            else:
                print("message does not contain ban word")
        else:
            #
            await message.guild.ban(message.author, reason="spam message")
            await asyncio.sleep(1)
            await message.guild.unban(message.author)
            # await message.channel.send('sends spam message')
            print("spam message sender kick out")

# Use your own token
client.run("OTA2Mjk1MTQ4MjQ0MjM4NDQ2.YYWjIQ.J6LmIqLVoYvK_kwFKWG8Z3z-Pgc")
