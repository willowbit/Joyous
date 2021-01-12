import schedule
import time
import discord
import ctx
import json
import random as rnd
from embeds import command_embed, help_embed
from discord.ext import commands, tasks
from discord import ext, client
from data import questions, remove_joy, addtofile, fetch_file, msg_blacklist

author_blacklist = []

qst = rnd.choice(questions)
qstq = qst.question
qstex = qst.example

comand_prefix = '>'

async def add(words, trigger, message):
    words.remove(trigger)
    x = ' '.join(words)
    addtofile(x, 'joydata.json')
    await message.channel.send(f'{message.author.mention} "{x}" has been added to my library!')

async def remove(words, trigger, message):
    words.remove(trigger)
    x = ' '.join(words)
    print('---------------------')
    print(x)
    remove_joy(x)
    await message.channel.send(f'{message.author.mention} "{x}" has been removed from my library.')

async def random(words, trigger, message):
    joys = fetch_joys()
    await message.channel.send(f"I'm grateful for...**{rnd.choice(joys)}**")

async def all(words, trigger, message):
    joys = fetch_file('joydata.json')
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

async def kill(words, trigger, message):
    exit()

async def delete(words, trigger, message):
    if len(words) == 1:
        x = 2
    else:
        x = (int(words[1]) + 1)
    await message.channel.purge(limit=x)

async def amicommunist(words, trigger, message):
    x = ' '.join(words[1:])
    if len(words) == 1:
        communist = ['not', 'in fact', 'in fact', 'in fact']
        await message.channel.send('calculating communism......')
        time.sleep(2.6)
        await message.channel.send(f'{message.author.mention} I can confirm you are **{rnd.choice(communist)}** a communist')
    else:
        gayornotgay = ['is not', 'is in fact', 'is in fact', 'is in fact']
        await message.channel.send('calculating communism......')
        time.sleep(2.6)
        await message.channel.send(f'{message.author.mention} I can confirm that {x} **{rnd.choice(communist)}** a communist')

async def addsong(words, trigger, message):
    formatsong = ' '.join(words[1:])
    addtofile(formatsong, 'playlist.json')
    await message.channel.send(f'{message.author.mention} "{formatsong}" has been added to my playlist!')

async def joydescript(words, trigger, message):
    await message.channel.send(embed = joy_embed)

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
    botcommand('amicommunist', amicommunist),   
    botcommand('panic', 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA!!!!!!'),
    botcommand('say', say),
    botcommand('commands', commands),
    botcommand('kill', kill),
    botcommand('d', delete),
    botcommand('addsong', addsong),
]

class reaction:
    def __init__(self, trigger, response):
        self.trigger = trigger
        self.response = response
    async def handle(self, message, words):
        if words == self.trigger:
            await message.channel.send(self.response)

reaction_list = [
    reaction('hello', 'Nice to see you!'),
    reaction('bleh', 'yeah same bro'),
    reaction('cookies', 'yum!!'),
    reaction('amigay', 'try >amigay')
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

        for r in reaction_list:
            words = content
            if words == r.trigger:
                await r.handle(message, words)
                return

        if content.startswith(comand_prefix):
            words = content[1:].split()
            for command in command_list:
                if (await command.handle(message, words)) is True:
                    return



client = Client()

with open('botcode.txt') as f:
    code = f.read()
client.run(code)
