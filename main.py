import json
from datetime import datetime
import os
from discord.ext import commands, tasks

from token import token

bot = commands.Bot(command_prefix=["!"])

def format_time(time):
    try:
        return(str(datetime.strptime(time, '%H:%M:%S').time())[:-3])
    except:
        try:
            return(str(datetime.strptime(time, '%H:%M').time())[:-3])
        except:
            return(str(datetime.strptime(time, '%H').time())[:-3])

@bot.event
async def on_ready():
    print('Bot ready!')
    global all_users
    global channel
    channel = bot.get_channel(993022827848544406)

    if os.path.getsize("times.txt") == 0:
        print("File is empty")

        # useful piece of code for future? gets all members in guild
        # guild = bot.get_guild(911121541717196810)
        # for member in guild.members:
        #     username = str(member.id)
        #     global all_users
        #     all_users = {}
        #     all_users[username] = ""
        # print(all_users)

        with open("times.txt", "w") as t:
            all_users = {'': '1008425387199570041'}
            t.write(json.dumps(all_users))
            print(all_users)
    else:
        with open("times.txt", "r") as t:
            all_users = json.load(t)
            print(all_users)

    checkTime.start()


@bot.command(aliases=["time"])
async def update(ctx, time):
    author = str(ctx.author.id)
    try:
        # to do: add all users to text document
        global all_users
        values = all_users.values()
        keys = all_users.keys()
        formatted_time = format_time(str(time))
        if author in values:
            for i in keys:
                if all_users[i] == author:
                    del all_users[i]
                    break

        all_users.update({str(formatted_time):str(author)})
        await ctx.send('Time modified!')
        print(all_users)

        # clear text file
        open('times.txt', 'w').close()
        # update stored file
        with open("times.txt", "w") as t:
            t.write(json.dumps(all_users))

    except:
        await ctx.send('Incorrect formatting')

@tasks.loop(seconds = 60)
async def checkTime():
    global all_users
    keys = all_users.keys()
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    print(current_time)
    if str(current_time) in keys:
        await ping_user(all_users[current_time])

# if time reached, repeat for 1 hour until command run to stop
async def ping_user(id):
    global channel
    await channel.send("<@" + str(id) + ">" + ", you have to do Leetcode!")

if __name__ == "__main__":
    bot.run(token)