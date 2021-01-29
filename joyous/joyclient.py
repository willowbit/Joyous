import schedule, time, discord, ctx, json, os
import random as rnd
from discord.ext import commands, tasks
from discord import ext
from .grabdata import addtofile, fetch_file, msg_blacklist, removefromfile
from .embeds import help_embed, command_embed
comand_prefix = '>'

async def add(words, trigger, message):
    print('TRIGGERED---')
    words.remove(trigger)
    x = ' '.join(words)
    addtofile(x, f'joydata{message.author.guild.id}.json')
    await message.channel.send(f'{message.author.mention} "{x}" has been added to my library!')

async def remove(words, trigger, message):
    words.remove(trigger)
    x = ' '.join(words)
    print('---------------------')
    print(x)
    removefromfile(x, f'joydata{message.author.guild.id}.json')
    await message.channel.send(f'{message.author.mention} "{x}" has been removed from my library.')

async def random(words, trigger, message):
    joys = fetch_file(f'joydata{message.author.guild.id}.json')
    await message.channel.send(f"I'm grateful for...**{rnd.choice(joys)}**")

async def all(words, trigger, message):
    joys = fetch_file(f'joydata{message.author.guild.id}.json')
    nl = '\n'
    sep = ', '
    await message.channel.send(f'{message.author.mention} here are all the joys in my library......{nl}**{sep.join(joys)}**')

async def help(words, trigger, message):
    await message.channel.send(embed = help_embed)
    awaiting_response = True

async def amigay(words, trigger, message):
    x = ' '.join(words[1:])
    if len(words) == 1:
        gayornotgay = ['not', 'in fact']
        await message.channel.send('calculating gayness......')
        time.sleep(2.6)
        await message.channel.send(f'{message.author.mention} I can confirm you are **{rnd.choice(gayornotgay)}** gay')
    else:
        gayornotgay = ['is not', 'is in fact']
        await message.channel.send('calculating gayness......')
        time.sleep(2.6)
        await message.channel.send(f'{message.author.mention} I can confirm that {x} **{rnd.choice(gayornotgay)}** gay')

async def say(words, trigger, message):
    await message.channel.purge(limit=1)
    await message.channel.send(' '.join(words[1:]))

async def commands(words, trigger, message):
    await message.channel.send(embed = command_embed)

async def delete(words, trigger, message):
    if len(words) == 1:
        x = 2
    else:
        x = (int(words[1]) + 1)
    await message.channel.purge(limit=x)



class botcommand:
    def __init__(self, trigger, response):
        self.trigger = trigger
        self.response = response
    async def handle(self, message, words):
        if words[0] == self.trigger:
            if type(self.response) == str:
                await message.channel.send(self.response)
            else:
                await self.response(words, self.trigger, message)
                return True
        else:
            return False


command_list = [
    botcommand('add', add),
    botcommand('remove', remove),
    botcommand('random', random),
    botcommand('wall', all),
    botcommand('help', help),
    botcommand('amigay', amigay),
    botcommand('panic', 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA!!!!!!'),
    botcommand('say', say),
    botcommand('commands', commands),
    botcommand('d', delete),
    botcommand('hello', 'Nice to see you!')
]

@tasks.loop(seconds=25)
async def change_status():
    playlist = fetch_file('playlist.json')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=(rnd.choice(playlist))))

class Client(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('--------------')
        change_status.start()
    async def on_message(self, message: discord.Message):

        content = message.content
        print(f'{message.author}: {content}')

        if message.author.id == self.user.id:
            return

        for w in msg_blacklist:
            if w in content:
                msg_response1 = 'That is not appropriate to say to anyone. Please watch your language.'
                await message.channel.send(msg_response1)

        if content.startswith(comand_prefix):
            words = content[1:].split()
            for command in command_list:
                if (await command.handle(message, words)) is True:
                    return
client = Client()

def run_client():
    with open('botcode.txt') as f:
        code = f.read()
    client.run(code)