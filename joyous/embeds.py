import discord

command_embed = discord.Embed(title='Commands', description="""
**>commands** - shows this page lol
**>help** - displays the help page

**>add [x]** - allows you to add [x] to the joy wall
**>remove [x]** - allows you to remove [x] from the joy wall
**>wall** - displays the joy wall
**>random** - displays a random joy from the joy wall

**>tea** - just a little something for your tummy
**>amigay [x]** - discerns if you, or x if provided, are gay
**>say [x]** - makes me say [x], your message will be deleted (do not abuse :rolling_eyes:)
**>lottery** - feeling lucky? try this command
**>compliment** - request a compliment! I love making people happy :)
**>xkcd [random, latest]** - displays a random (>xkcd random) or the latest (>xkcd latest) xkcd comic! check out all of Randall Munroe's work at https://xkcd.com/
**>albumart [keywords]** - find any album art! credit to https://github.com/matteing for the API

""", color=0xff6bc9)

help_embed = discord.Embed(title='Joyous Help', description="Hi! I'm Joyous, your discord positivity bot!", color=0xff6bc9)
help_embed.add_field(name='What do I do?', value="I keep your server a nice, positive place where you and your friends can hang out. Check out the project at https://github.com/willowbit/Joyous")
help_embed.add_field(name="How do I use Joyous?", value="Talk to me with '>' + whatever you would like me to do. You can ask find a list of my tools with '>commands'")
help_embed.set_footer(text='under progress by willy! (willow#5131), contact me with bugs or ideas :)')