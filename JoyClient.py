import time
import discord
import random as rnd
from discord import client
from data import add_joy
from data import fetch_joys
from data import questions
import json

author_blacklist = []

qst = rnd.choice(questions)
qstq = qst.question
qstex = qst.example

help_embed = discord.Embed(title='Joyous Help', description="Hi! I'm Joyous, your discord positivity bot!", color=0xff6bc9)
help_embed.add_field(name='What do I do?', value="I keep your server positive with a daily reflection. I also have a wall where people can save their responses.")
help_embed.add_field(name="How do I use Joyous?", value="You can talk to me by using '>' and whatever you want me to do. You can find a list of commands with >commands.")
help_embed.set_footer(text='under progress by willy! you can find the project here https://github.com/CuteBlueRadio/Joyous')

wall_embed = discord.Embed(title='The Wall', description="Here's where all of your opted daily reflection responses are stored! Everyone can see this.", color=0xff6bc9)

comand_prefix = '>'


async def hello(words, trigger, message):
    await message.channel.send('Hello!!')

async def add(words, trigger, message):
    words.remove(trigger)
    x = ' '.join(words)
    add_joy(x)
    await message.channel.send(f'{message.author.mention} "{x}" has been added to my library!')

async def random(words, trigger, message):
    joys = fetch_joys()
    await message.channel.send(f"I'm grateful for...**{rnd.choice(joys)}**")

async def all(words, trigger, message):
    joys = fetch_joys()
    await message.channel.send(f'here are all the joys in my library......{joys}')

async def help(words, trigger, message):
    await message.channel.send(embed = help_embed)
    awaiting_response = True

async def gaytest(words, trigger, message):
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
    botcommand('hello', hello),
    botcommand('add', add),
    botcommand('random', random),
    botcommand('all', all),
    botcommand('help', help),
    botcommand('amigay', gaytest),
    botcommand('panic', 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA!!!!!!'),
    botcommand('say', say)
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
]

class Client(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('--------------')

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

client = Client()

with open('botcode.txt') as f:
    code = f.read()
client.run(code)
