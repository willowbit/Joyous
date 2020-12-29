import schedule
import time
import discord
import random as rnd
from discord import client
from data import add_joy
from data import fetch_joys
from data import questions

qst = rnd.choice(questions)

comand_prefix = '>'

reflection_embed = discord.Embed(title='Reflection', description='Take this time to reflect. Mention one thing you were grateful for today, as well as answer the question below.', color=0xff6bc9)
reflection_embed.add_field(name="Today's Question:", value=qst, inline=True)
reflection_embed.add_field(name='example:', value='I was grateful for ____ today', inline=False)
reflection_embed.set_footer(text='add ">" to the start of your response to add it to the wall')

help_embed = discord.Embed(title='Joyous Help', description="Hi! I'm Joyous, your discord positivity bot!")
help_embed.add_field(name='What can I do?', value="I keep your server positive with a daily reflection. I also have a wall where people can keep their responses.")
help_embed.add_field(name="How do I use Joyous?", value="You can talk to me by using '>' and your command. You can find a list of commands with >commands.")
help_embed.set_footer(text='under progress by willy! you can find the project here')

async def hello(words, trigger, message):
    await message.channel.send('bleck')

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
    
async def daily_joy(words, trigger, message):
    joys = fetch_joys()
    await message.channel.send(f"""Goooooood Morning!! Here's todays joy:
I'm grateful for...**{rnd.choice(joys)}**""")

async def reflection(words, trigger, message):
    await message.channel.send(embed = reflection_embed)
    awaiting_response = True


class botcommand:
    def __init__(self, trigger, response):
        self.trigger = trigger
        self.response = response
    async def handle(self, message, words):
        if words[0] == self.trigger:
            await self.response(words, self.trigger, message)
            return

command_list = [
    botcommand('hello', hello),
    botcommand('add', add),
    botcommand('random', random),
    botcommand('all', all),
    botcommand('test', reflection)
]

class Client(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('--------------')

    async def on_message(self, message: discord.Message):
        content = message.content
        print(content)
        
        if message.author.id == self.user.id:
            return

        if content.startswith(comand_prefix):
            words = content[1:].split()
            for command in command_list:
                await command.handle(message, words)

client = Client()
client.run('NzkzMTMyOTA1NTY3NzQ4MTE2.X-n0lA.kHKsW9bF-ranyQ_bdOPxwCt30MA')