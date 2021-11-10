from discord.ext import commands
import asyncio

client = commands.Bot(command_prefix="?")

@client.event
async def on_ready():
    print("ready")
    while True:
        print("cleared")
        await asyncio.sleep(10)
        with open("spam_detect.txt", "r+") as file:
            file.truncate(0)

@client.event
async def on_message(message):
    counter = 0
    with open("spam_detect.txt", "r+") as file:
        for lines in file:
            if lines.strip("\n") == str(message.author.id):
                counter+=1
        
        file.writelines(f"{str(message.content)}\n")
        if counter > 2:
            await message.guild.ban(message.author, reason="spam")
            await asyncio.sleep(1)
            await message.guild.unban(message.author)
            print("uh oh")

#Use your own token
client.run("OTA2Mjk1MTQ4MjQ0MjM4NDQ2.YYWjIQ.J6LmIqLVoYvK_kwFKWG8Z3z-Pgc")

