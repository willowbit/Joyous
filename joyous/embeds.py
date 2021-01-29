import discord

command_embed = discord.Embed(title='Commands', description="""
**>commands** - shows this screen
**>help** - displays the help screen

**>add [x]** - allows you to add [x] to the joy wall
**>remove [x]** - allows you to remove [x] from the joy wall
**>wall** - displays the joy wall
**>random** - displays a random joy from the joy wall

**>amigay [x]** - discerns if you, or x if provided, are gay
**>say [x]** - makes joyous say [x], your message will be deleted

**>d [x]** - deletes [x] number of the previous messages, your message will be deleted
**>kill** - kills Joyous. Use only in case of emergency.
""", color=0xff6bc9)

help_embed = discord.Embed(title='Joyous Help', description="Hi! I'm Joyous, your discord positivity bot!", color=0xff6bc9)
help_embed.add_field(name='What do I do?', value="I keep your server a nice, clean place where you and your friends can hang out. Check out the project at https://github.com/CuteBlueRadio/Joyous")
help_embed.add_field(name="How do I use Joyous?", value="Talk to me by using '>' + whatever you would like me to do. You can ask find a list of my tools with '>commands'")
help_embed.set_footer(text='under progress by willy! (willow#5131), contact me with bugs or ideas :)')