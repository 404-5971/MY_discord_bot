import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command(name='button')
async def button(ctx, split=False):
    view = discord.ui.View()

    # Button 1
    button1 = discord.ui.Button(
        label='Stand',
        style=discord.ButtonStyle.red
    )
    async def button1_callback(interaction: discord.Interaction):
        await interaction.response.send_message('Button 1 was pressed!', ephemeral=True)
    button1.callback = button1_callback

    # Button 2
    button2 = discord.ui.Button(
        label='Split',
        style=discord.ButtonStyle.secondary
    )
    async def button2_callback(interaction: discord.Interaction):
        await interaction.response.send_message('Button 2 was pressed!', ephemeral=True)
    button2.callback = button2_callback

    # Button 3
    button3 = discord.ui.Button(
        label='Double',
        style=discord.ButtonStyle.blurple
    )
    async def button3_callback(interaction: discord.Interaction):
        await interaction.response.send_message('Button 3 was pressed!', ephemeral=True)
    button3.callback = button3_callback

    # Button 4
    button4 = discord.ui.Button(
        label='Hit',
        style=discord.ButtonStyle.green
    )
    async def button4_callback(interaction: discord.Interaction):
        await interaction.response.send_message('Button 4 was pressed!', ephemeral=True)
    button4.callback = button4_callback

    # Add buttons to the view
    view.add_item(button1)
    if split:
        view.add_item(button2)
    view.add_item(button3)
    view.add_item(button4)

    await ctx.send(content='Here are your buttons:', view=view)

bot.run('MTIzMDk2MjI2OTc0ODQ2NTY2Ng.G99PQ1.04Ch0VvwZbQqS0ZnbPKMjjAra8t2dHv38M9BQ0')
