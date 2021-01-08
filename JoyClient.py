import time
import discord
import random as rnd
from discord import client
from data import add_joy
from data import fetch_joys
from data import questions
from data import remove_joy
import json

author_blacklist = []

qst = rnd.choice(questions)
qstq = qst.question
qstex = qst.example

command_embed = discord.Embed(title='Commands', description="""
**>commands** - shows this screen
**>help** - displays the help screen

**>add [x]** - allows you to add [x] to the gratitude wall
**>remove [x]** - allows you to remove [x] to the gratitude wall

**>amigay [x]** - discerns if you, or x if provided, are gay
**>say [x]** - makes joyous say [x], your message will be deleted

**>d [x]** - deletes [x] number of the previous messages, your message will be deleted
**>kill** - kills Joyous. Use only in case of emergency.
""", color=0xff6bc9)

help_embed = discord.Embed(title='Joyous Help', description="Hi! I'm Joyous, your discord positivity bot!", color=0xff6bc9)
help_embed.add_field(name='What do I do?', value="I keep your server positive with a daily reflection. I also have a wall where people can save their responses.")
help_embed.add_field(name="How do I use Joyous?", value="You can talk to me by using '>' and whatever you want me to do. You can find a list of commands with >commands.")
help_embed.set_footer(text='under progress by willy! (WaffleBread#5131) you can find the project here: https://github.com/CuteBlueRadio/Joyous')

wall_embed = discord.Embed(title='The Wall', description="Here's where all of your opted daily reflection responses are stored! Everyone can see this.", color=0xff6bc9)

comand_prefix = '>'


async def add(words, trigger, message):
    words.remove(trigger)
    x = ' '.join(words)
    add_joy(x)
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
    joys = fetch_joys()
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
        await message.channel.send(f'I can confirm you are **{rnd.choice(gayornotgay)}** gay')
    else:
        gayornotgay = ['is not', 'is in fact']
        await message.channel.send('calculating gayness......')
        time.sleep(2.6)
        await message.channel.send(f'I can confirm that {x} **{rnd.choice(gayornotgay)}** gay')

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
    botcommand('random', random),
    botcommand('all', all),
    botcommand('help', help),
    botcommand('amigay', amigay),
    botcommand('panic', 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA!!!!!!'),
    botcommand('say', say),
    botcommand('commands', commands),
    botcommand('remove', remove),
    botcommand('kill', kill),
    botcommand('d', delete)
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

class Client(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('--------------')
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Guster on Ice - Live from Portland, Maine"))
    async def on_message(self, message: discord.Message):
        content = message.content
        print(message.author, content)
        
        if message.author.id == self.user.id:
            return

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
        if message.author.id == 235088799074484224:
            await message.channel.send('!help')

client = Client()

with open('botcode.txt') as f:
    code = f.read()
client.run(code)
