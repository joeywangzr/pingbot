import json
from datetime import datetime
from threading import Thread

from apscheduler.schedulers.background import BackgroundScheduler
from discord.ext import commands

token = ""

bot = commands.Bot(command_prefix=["."])

channel = bot.get_channel(993022827848544406)

with open("times.txt", "r") as t:
    users = json.load(t)


def get_all_users(key):
    values = list(users.values())
    keys = list(users.keys())
    user = []
    for i in range(values):
        if keys[i] == key:
            user.append(values[i])
    return user


def convert_utc(time):
    return datetime.utcfromtimestamp(time)


def pings():
    bs = BackgroundScheduler()
    user = get_all_users(datetime.utcnow())

    def ping_users():
        pinged_users = [f"<@{i}>" for i in user]
        if pinged_users:
            await channel.send(', '.join(pinged_users))

    job = bs.add_job(ping_users, 'interval', hour=1)
    bs.start()
    while True:
        try:
            user = users[datetime.utcnow()]
        except:
            pass


@bot.command(aliases=["u"])
async def update(ctx, time):
    author = int(ctx.author.id)
    utc_time = convert_utc(time)
    keys = list(users.keys())
    values = list(users.values())
    for i in range(keys):
        if values[i] == author:
            keys[i] = utc_time
    else:
        users[utc_time] = author
    with open("times.txt", "w") as t:
        t.write(json.dumps(users))
    await ctx.send(f"Your ping time was changed to {time}")


def run():
    bot.run(token)


if __name__ == "__main__":
    Thread(target=pings).start()
    Thread(target=run).start()
