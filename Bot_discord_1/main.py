import datetime
import random
import asyncio
import discord
from discord import app_commands
from discord.ext import commands, tasks
from config import TOKEN

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
async def on_command(ctx):
    logs_channel = discord.utils.get(ctx.guild.channels, name="logs")

    if logs_channel:
        command_used = ctx.message.content
        member = ctx.message.author
        embed = discord.Embed(
            title="Command Use",
            description="A command was used",
            color=discord.Color.blue(),
            timestamp=datetime.datetime.now()
        )
        embed.set_thumbnail(url=member.avatar)
        embed.add_field(name=f"{member} use the command", value=command_used)
        embed.set_footer(text=ctx.guild.name)
        await logs_channel.send(embed=embed)



@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.lower() == "test":
        await message.channel.send(f"{message.content}")
        print("message envoyer")
    await bot.process_commands(message)



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
async def choice(ctx, *, args):
    var = list(filter(lambda x: x.strip(), args.split(" ")))
    message = await ctx.send("Thinking")
    await message.edit(content=message.content+".")
    await asyncio.sleep(0.5)
    await message.edit(content=message.content +"..")
    await asyncio.sleep(0.5)
    await message.edit(content=message.content +"...")
    await asyncio.sleep(0.5)
    result = random.choice(var)
    await message.edit(content=f"I choose {result} !")

@choice.error
async def choice_error(ctx: commands.Context, error: commands.CommandError):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title="Error",
            description="Missing Argument",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return

    else:
        embed = discord.Embed(
            title="Error",
            description="Something wrong !",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)


@bot.command(aliases=['info', 'uinfo', 'ui'])
async def userinfo(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.message.author
    roles = [role for role in member.roles]
    embed = discord.Embed(
        title="Information utilisation",
        description=f"information sur {member.name}",
        color=discord.Color.blue(),
        timestamp=datetime.datetime.now()
    )
    embed.set_thumbnail(url=member.avatar)
    embed.add_field(name="Nom", value=member.display_name, inline=False)
    embed.add_field(name="Information created", value=member.created_at.strftime('%B %d, %Y'), inline=True)
    embed.add_field(name="Information arrival", value=member.joined_at.strftime('%B %d, %Y'), inline=True)
    embed.add_field(name="Information roles", value="\n".join([role.mention for role in roles]), inline=False)
    embed.add_field(name="Information top role", value=member.top_role, inline=False)
    embed.add_field(name="Information supplementary", value=member.bot, inline=False)
    await ctx.send(embed=embed)


@bot.command(aliases=['si', 'SI', 'info_serv', 'gi'])
async def guild_info(ctx):
    guild = ctx.guild
    count_voice_channels = len(guild.voice_channels)
    count_text_channels = len(guild.text_channels)

    embed = discord.Embed(
        title=f"Information sur server",
        description=f"Information du server {guild.name}",
        color=discord.Color.blue(),
        timestamp=datetime.datetime.now()
    )
    embed.set_thumbnail(url=guild.icon)
    embed.add_field(name="Owner of the guild", value=f"{guild.owner.mention}")
    embed.add_field(name="Description of the guild", value=guild.description)
    embed.add_field(name="Created at", value=guild.created_at.strftime('%B %d, %Y'))
    embed.add_field(name="Number of salons ", value=count_text_channels + count_voice_channels)
    embed.add_field(name="Number of salons text ", value=count_text_channels, inline=True)
    embed.add_field(name="Number of salons voice", value=count_voice_channels, inline=True)
    embed.add_field(name="Number of members", value=guild.member_count, inline=False)

    await ctx.send(embed=embed)


@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: discord.Member, reason: str = None):
    if reason is None:
        reason = "Reason not defined"

    await ctx.guild.ban(user, reason=reason)

    mbed = discord.Embed(
            title="Ban",
            description="User ban",
            color=discord.Color.red(),
            timestamp=datetime.datetime.now()

    )
    mbed.set_author(name=f"**{ctx.message.author.user.name}**")
    mbed.set_thumbnail(url=user.avatar)
    mbed.add_field(name="Informations", value=f"{user.mention} was ban by {ctx.message.author.user.mention}")
    mbed.add_field(name="Reason", value=reason, inline=True)
    mbed.set_footer(text=ctx.guild.name)
    await ctx.send(embed=mbed)


@ban.error
async def ban_error(ctx: commands.Context, error: commands.CommandError):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title="Error",
            description="You must give a name for the user to ban !",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title="Error",
            description="Something wrong !",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)


@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, user: discord.User, *, reason: str=None):
    if reason is None:
        reason = "Reason not given"
    await ctx.guild.unban(user=user, reason=reason)
    message = await ctx.send(f"{user} was deban")
    await asyncio.sleep(4)
    await message.delete()


@unban.error
async def unban_error(ctx: commands.Context, error: commands.CommandError):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title="Error",
            description="You must give a name for the user to unban !",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title="Error",
            description="Something wrong !",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)




@bot.command()
@commands.has_permissions(manage_channels=True)
async def create_category(ctx, name: str):
    try:
        await ctx.guild.create_category(name)
        await ctx.send(f"La catégorie '{name}' a été créée avec succès.")
    except discord.HTTPException:
        await ctx.send("Une erreur s'est produite lors de la création de la catégorie.")




@bot.command()
@commands.has_permissions(manage_channels=True)
async def delete_category(ctx, category_name: str):
    # Recherche de la catégorie par son nom
    category = discord.utils.get(ctx.guild.categories, name=category_name)

    # Si la catégorie n'a pas été trouvée
    if category is None:
        await ctx.send(f"La catégorie \"{category_name}\" n'a pas été trouvée.")
        return

    try:
        # Suppression de la catégorie
        await category.delete()
        await ctx.send(f"La catégorie \"{category_name}\" a été supprimée.")
    except Exception as e:
        # Gestion des erreurs éventuelles
        await ctx.send(f"Une erreur est survenue lors de la suppression de la catégorie : {e}")

@bot.command()
@commands.has_permissions(administrator=True)
async def logs(ctx: commands.Context):
    logs_channel = discord.utils.get(ctx.guild.channels, name="logs")
    if logs_channel:
        await ctx.send("Salon exist ")
        return

    logs_channel = await ctx.guild.create_text_channel("logs")
    admin_role = discord.utils.get(ctx.guild.roles, name="Admin")
    await logs_channel.set_permissions(admin_role, read_messages=True, send_messages=True)
    everyone_role = ctx.guild.default_role
    await logs_channel.set_permissions(everyone_role, read_messages=False, send_messages=False)
    message = await ctx.send(f"This channel {logs_channel.mention} was create for Admin.")
    await asyncio.sleep(4)
    await message.delete()



@bot.command(aliases=['newM', 'nM', 'nm'])
@commands.has_permissions(manage_channels=True)
async def new_member(ctx):
    channels = ctx.guild.channels
    if any(channel.name.lower() == "arriving" or channel.name.lower() == "deserter" for channel in channels):
        await ctx.send("Les salons existent .")
        return

    category = discord.utils.get(ctx.guild.categories, name="Welcome And Left Members")
    if not category:
        await ctx.guild.create_category(name="Welcome And Left Members")
        category = discord.utils.get(ctx.guild.categories, name="Welcome And Left Members")

    welcome = await ctx.guild.create_text_channel("arriving", category=category)
    left = await ctx.guild.create_text_channel("deserter", category=category)

    everyone_role = ctx.guild.default_role
    await welcome.set_permissions(everyone_role, read_messages=True, send_messages=False)
    await left.set_permissions(everyone_role, read_messages=True, send_messages=False)

    mbed = discord.Embed(
        title="Command success",
        description="Salon create.",
        color=discord.Color.green(),
        timestamp=ctx.message.created_at
    )
    message = await ctx.send(embed=mbed)
    await asyncio.sleep(4)
    await message.delete()


@bot.event
async def on_member_join(member):
    channels = member.guild.channels
    for channel in channels:
        if channel.name.lower() == "arriving":
            mbed = discord.Embed(
                title=f"Welcome {member.name}",
                description="A member join",

            )
            mbed.set_thumbnail(url=member.avatar)
            mbed.add_field(name="Account create ", value=member.created_at.strftime("%B %d, %Y"))
            await channel.send(embed=mbed)
            return


@bot.event
async def on_member_remove(member):
    channels = member.guild.channels
    for channel in channels:
        if channel.name.lower() == "deserter":
            mbed = discord.Embed(
                title=f"{member.name} leave the guild",
                description="A member is gone",

            )
            await channel.send(embed=mbed)
            return


@bot.command(aliases=['c_c', 'cc'])
@commands.has_permissions(manage_channels=True)
async def create_channel(ctx: commands.Context, channel: str, *, category: discord.CategoryChannel = None):
    guild = ctx.guild
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        guild.me: discord.PermissionOverwrite(read_messages=True)
    }
    if category is not None:
        overwrites[guild.default_role] = discord.PermissionOverwrite(read_messages=False, connect=False)
    new_channel = await guild.create_text_channel(channel, category=category, overwrites=overwrites)
    embed = discord.Embed(
        title="Success",
        description="New Channel",
        color=discord.Color.blue(),
        timestamp=datetime.datetime.now()
    )
    embed.add_field(name="Check", value=f"The channel {new_channel.mention} was created", inline=True)
    message = await ctx.send(embed=embed)
    await asyncio.sleep(4)
    await message.delete()


@create_channel.error
async def create_channel_error(ctx: commands.Context, error: commands.CommandError):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title="Error",
            description="You must give a name for the channel to be created !",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title="Error",
            description="Something wrong !",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)


@bot.command(aliases=['rm', 'd_c'])
@commands.has_permissions(manage_channels=True)
async def delete_channel(ctx: commands.Context, channel: str):
    guild = ctx.guild
    channels = guild.channels
    found = False
    for ch in channels:
        if ch.name == channel:
            await ch.delete()
            found = True

    if not found:
        embed = discord.Embed(
            title="Error",
            description=f"This channel **{channel}** don't exist."
        )
        await ctx.send(embed=embed)
        return

    mbed = discord.Embed(
        title="Success",
        color=discord.Color.green(),
        timestamp=ctx.message.created_at
    )
    mbed.add_field(name="The channel was find ", value=f"The channel **{channel}** was deleted.")
    await ctx.send(embed=mbed)


@delete_channel.error
async def delete_channel_error(ctx: commands.Context, error: commands.CommandError):
    if isinstance(error, commands.MissingRequiredArgument):
        mbed = discord.Embed(
            title="Error",
            description="You must give a name for the channel to be removed !",
            color=discord.Color.red()
        )
        await ctx.send(embed=mbed)
    else:
        mbed = discord.Embed(
            title="Error",
            description="Something wrong.",
            color=discord.Color.red()
        )
        await ctx.send(embed=mbed)


@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, nb: int):
    message_deleted = await ctx.channel.purge(limit=nb + 1)
    mbed = discord.Embed(
        title="Success",
        color=discord.Color.blue(),
        timestamp=ctx.message.created_at
    )
    author = ctx.message.author
    mbed.set_thumbnail(url=author.avatar)
    mbed.add_field(name="Message delete", value=f"{len(message_deleted) - 1} message was deleted")
    message = await ctx.send(embed=mbed)
    await asyncio.sleep(4)
    await message.delete()


@clear.error
async def clear_error(ctx: commands.Context, error: commands.CommandError):
    if isinstance(error, commands.MissingRequiredArgument):
        mbed = discord.Embed(
            title="Error",
            description="Argument forgot.",
            color=discord.Color.red(),
            timestamp=ctx.message.created_at
        )
        mbed.add_field(name="Argument forgot", value="Please enter a argument")
        await ctx.send(embed=mbed)
    else:
        mbed = discord.Embed(
            title="Error",
            description="Command Failed.",
            color=discord.Color.red(),
            timestamp=ctx.message.created_at
        )
        mbed.add_field(name="Error", value="Something Wrong !")
        await ctx.send(embed=mbed)


@bot.command()
async def helps(ctx):
    embed = discord.Embed(
        title="Helps",
        description="All commands",
        color=discord.Color.blue(),
        timestamp=datetime.datetime.now()
    )
    embed.set_thumbnail(url=bot.user.avatar)
    commands = bot.commands
    embed.set_footer(text=ctx.guild.name)
    for command in commands:
        command_bot = command.name
        embed.add_field(name="Commands", value=f"!{command_bot}",inline=False)

    await ctx.send(embed=embed)



bot.run(TOKEN)
