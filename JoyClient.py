import schedule
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

reflection_embed = discord.Embed(title='Daily Reflection', description='Take this time to reflect on your day. What did you accomplish? Answer todays question below.', color=0xff6bc9)
reflection_embed.add_field(name="Today's Question:", value=qstq, inline=True)
reflection_embed.add_field(name='example:', value=qstex, inline=False)
reflection_embed.set_footer(text='add ">" to the start of your response to add it to the wall')

help_embed = discord.Embed(title='Joyous Help', description="Hi! I'm Joyous, your discord positivity bot!", color=0xff6bc9)
help_embed.add_field(name='What do I do?', value="I keep your server positive with a daily reflection. I also have a wall where people can save their responses.")
help_embed.add_field(name="How do I use Joyous?", value="You can talk to me by using '>' and whatever you want me to do. You can find a list of commands with >commands.")
help_embed.set_footer(text='under progress by willy! you can find the project here https://github.com/CuteBlueRadio/Joyous')

wall_embed = discord.Embed(title='The Wall', description="Here's where all of your opted daily reflection responses are stored! Everyone can see this.", color=0xff6bc9)
# wall_embed.add_field(name=)

comand_prefix = '>'

current_question = qstq

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
    
async def daily_joy(words, trigger, message):
    joys = fetch_joys()
    await message.channel.send(f"""Goooooood Morning!! Here's todays joy:
I'm grateful for...**{rnd.choice(joys)}**""")

async def reflection(words, trigger, message):
    await message.channel.send(embed = reflection_embed)

async def help(words, trigger, message):
    await message.channel.send(embed = help_embed)
    awaiting_response = True

async def success(x, message):
    success_embed = discord.Embed()
    success_embed.add_field(name="Success", value=f'Response "{x}" successfully saved!')
    success_embed.set_footer(text='try ">thewall" to see them all!')
    await message.channel.send(embed = success_embed)

async def thewall(words, trigger, message):
    with open('responses.json', 'r') as f:
        x = json.load(f)
        print(current_question)
        await message.channel.send(x[0][current_question])
        # await message.channel.send(embed=wall_embed)

async def panic(words, trigger, message):
    await message.channel.send('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA!!!!!!')

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


class botcommand:
    def __init__(self, trigger, response):
        self.trigger = trigger
        self.response = response
    async def handle(self, message, words):
        if words[0] == self.trigger:
            await self.response(words, self.trigger, message)
            return True
        else:
            return False

command_list = [
    botcommand('hello', hello),
    botcommand('add', add),
    botcommand('random', random),
    botcommand('all', all),
    botcommand('test', reflection),
    botcommand('help', help),
    botcommand('thewall', thewall),
    botcommand('amigay', gaytest),
    botcommand('panic', panic)
]

class Client(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('--------------')
        print('THIS THING:',current_question)

    async def on_message(self, message: discord.Message):
        content = message.content
        print(message.author, content)
        
        if message.author.id == self.user.id:
            return

        if content.startswith(comand_prefix):
            words = content[1:].split()
            for command in command_list:
                if (await command.handle(message, words)) is True:
                    return

            if message.author not in author_blacklist:
                if current_question is not None:
                    with open('responses.json', 'r') as f:
                        x = json.load(f)
                    for s in x:
                        print('woop woop')
                        if s[current_question] == True:
                            print('reeeeeeeeeeeeeeeeeeeeeeeeeeeee')
                            x[current_question].append({
                                str(current_question): [content[1:]]
                            })
                    else:
                        print('nooooooooooooooooooooooooooooo')
                        x.append({
                            str(current_question): [content[1:]]
                        })
                    with open('responses.json', 'w') as f:
                        json.dump(x, f)
                    author_blacklist.append(message.author)
                    await success(content[1:], message)

client = Client()
client.run('token')