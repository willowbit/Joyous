import schedule, time, discord, ctx, json, os, subprocess, mpv, youtube_dl, sys, requests, coverpy
import xkcd as xk
import random as rnd
from discord.ext import commands, tasks
from discord import ext
from .grabdata import addtofile, fetch_file, msg_blacklist, removefromfile
from .embeds import help_embed, command_embed
from datetime import datetime as dt

cpy = coverpy.CoverPy()

thisdir = os.path.dirname(os.path.realpath(__file__))

### Change this for the symbol before commands
comand_prefix = '>'
songlist = ['rickroll.mp3', 'mrbrightside.mp3', 'almostsweetmusic.mp3']

async def add(words, trigger, message):
    words.remove(trigger)
    x = ' '.join(words)
    addtofile(x, f'server{message.author.guild.id}.server', key=2)
    await message.channel.send(f'{message.author.mention} "{x}" has been added to my library!')

async def remove(words, trigger, message):
    words.remove(trigger)
    x = ' '.join(words)
    if words[0] == '-force':
        x = ' '.join(words[1:])
        removefromfile(x, f'server{message.author.guild.id}.server', message, force=True)
        await message.channel.send(f'{message.author.mention} "{joy}" has been removed from my library.')
        return
    if removefromfile(x, f'server{message.author.guild.id}.server', message) is False:
        await message.channel.send(f"{message.author.mention} Sorry! I couldn't find that joy. Check you're spelling, or if you're really stuck, try >remove -force <item>")
        return
    removefromfile(x, f'server{message.author.guild.id}.server', message)
    await message.channel.send(f'{message.author.mention} "{x}" has been removed from my library.')

async def random(words, trigger, message):
    joys = fetch_file(f'server{message.author.guild.id}.server')
    await message.channel.send(f"I'm grateful for...**{rnd.choice(joys)}**")

async def wall(words, trigger, message):
    joys = fetch_file(f'server{message.author.guild.id}.server')
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
    for word in msg_blacklist:
        if word in words:
            await message.channel.send('I cannot say that.')
            return
    await message.channel.send(' '.join(words[1:]))

async def commands(words, trigger, message):
    await message.channel.send(embed = command_embed)

# async def delete(words, trigger, message):
#     if len(words) == 1:
#         x = 2
#     else:
#         x = (int(words[1]) + 1)
#     await message.channel.purge(limit=x)

async def lottery(words, trigger, message):
    emoji_list = [':cat:', ':full_moon_with_face:', ':sun_with_face:', ':christmas_tree:', ':cherries:', ':croissant:', ':football:', ':rainbow_flag:']
    choice1 = rnd.choice(emoji_list)
    choice2 = rnd.choice(emoji_list)
    choice3 = rnd.choice(emoji_list)
    # if rnd.randint(1,3) == 2:
    #     choice2 = choice1
    #     choice3 = choice1
    await message.channel.send(f"""||{choice1} {choice2} {choice3}||""")
    for slot in emoji_list:
        if choice1 == choice2 == choice3 == slot:
            time.sleep(5)
            await message.channel.send(f"** {message.author.mention} YOU'VE WON!!!!** :sparkles: :sparkles: :exploding_head:")

async def compliment(words, trigger, message):
    x = ' '.join(words[1:])
    comps = fetch_file('compliments.yaml')
    if len(words) == 1:
        await message.channel.send(f"{message.author.mention} {rnd.choice(comps)}")
    else:
        await message.channel.send(f"{x} {rnd.choice(comps)}")

async def filter(words, trigger, message):
    if words[1]=='off':
        nofilter = fetch_file('nofilter.yaml')
        if message.guild.id in nofilter:
            await message.channel.send("Message filtering has already been turned off! To turn it on, try >filter on")
            return
        addtofile(message.guild.id, 'nofilter.yaml', key=2)
        print(nofilter)
        await message.channel.send('message filtering has been turned off.')
    if words[1]=='on':
        nofilter = fetch_file('nofilter.yaml')
        if message.guild.id not in nofilter:
            await message.channel.send("Message filtering has already been turned on! To turn it off, try >filter off")
            return
        removefromfile(message.guild.id, 'nofilter.yaml', message)
        await message.channel.send('message filtering has been turned on.')

async def poll(words, trigger, message):
    pollquestion = ' '.join(words[1:])
    stateq = await message.channel.send(f"""A new poll has been created! The question is....
**{pollquestion}**
React with a :thumbsup: for yes and a :thumbsdown: for no.""")
    await stateq.add_reaction('👍')
    time.sleep(0.1)
    await stateq.add_reaction('👎')
    # await stateq.edit(content='CHUNKYYY')
    time.sleep(2)

async def xkcd(words, trigger, message):
    if words[1] in ['-r', 'r', 'random']:
        comic = xk.getRandomComic()
    elif words[1] in ['-l', 'l', 'latest', 'new', '-n']:
        comic = xk.getLatestComic()
    else:
        comic = xk.getLatestComic()
    comic = comic.getImageLink()
    await message.channel.send(comic)

async def albumart(words, trigger, message):
    limit = 1
    songname = ' '.join(words[1:])
    result = cpy.get_cover(songname, limit)
    art = result.artwork(10000)
    
    description = f'{message.author.mention}, {result.artist} - {result.name}'
    print(description)
    
    embed = discord.Embed(description=description, color=0xff6bc9)
    embed.set_image(url=art)
    embed.set_footer(text='try >xkcd random!')

    await message.channel.send(embed=embed)

async def tea(words, trigger, message):
    if len(words) == 2:
        await message.channel.send(f"here, {words[1]}, have a nice cozy cup of hot tea :heart: :coffee:")
    else:
        await message.channel.send(f"here, {message.author.mention}, have a nice cozy cup of hot tea :heart: :coffee:")

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
    botcommand('wall', wall),
    botcommand('help', help),
    botcommand('tea', tea),
    botcommand('amigay', amigay),
    botcommand('say', say),
    botcommand('commands', commands),
    botcommand('hello', 'nice to see you!'),
    botcommand('lottery', lottery),
    botcommand('compliment', compliment),
    botcommand('filter', filter),
    botcommand('poll', poll),
    botcommand('xkcd', xkcd),
    botcommand('albumart', albumart),
]

### Changes the status every 50 seconds
@tasks.loop(seconds=50)
async def change_status():
    statuslist = fetch_file('statuslist.yaml')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=(rnd.choice(statuslist))))

class Client(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print(f'at {datetime.now.strftime("%H:%M:%S")}')
        print('--------------')
        change_status.start()
    async def on_message(self, message: discord.Message):

        content = message.content
        ### Make sure the bot doesn't reply to itself
        if message.author.id == self.user.id:
            return

        ### Filter
        for w in msg_blacklist:
            if w in content:
                nofilteredservers = fetch_file('nofilter.yaml')
                if message.guild.id not in nofilteredservers:
                    msg_response1 = 'That is not appropriate to say to anyone. Please watch your language.'
                    await message.channel.send(msg_response1)
                    return
                else:
                    print('filter message has been blocked.')
                    return
                await message.channel.send(msg_response1)
        
        ### If message is command
        if content.startswith(comand_prefix):
            words = content[1:].split()
            for command in command_list:
                if (await command.handle(message, words)) is True:
                    return

        ### win the lottery idk lol
        if rnd.randint(1,100000) == 42:
            time.sleep(5)
            await message.channel.send("there was a 1 in 100,000 chance that this message was sent. I like those odds.")

client = Client()

# Run the bot
def run_client():
    with open('botcode.txt') as f:
        code = f.read()
    client.run(code)