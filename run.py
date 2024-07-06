import discord

client = discord.Client(intents=discord.Intents.all())
tree = discord.app_commands.CommandTree(client)

@client.event
async def on_ready():
    await tree.sync()
    print(f'Logged in as {client.user}')

@tree.command(name='button', description='Shows buttons')
async def button(interaction: discord.Interaction):
    view = discord.ui.View()

    # Button 1
    button1 = discord.ui.Button(
        label='Button 1',
        style=discord.ButtonStyle.blurple
    )
    async def button1_callback(interaction: discord.Interaction):
        await interaction.response.send_message('Button 1 was pressed!', ephemeral=True)
    button1.callback = button1_callback

    # Button 2
    button2 = discord.ui.Button(
        label='Button 2',
        style=discord.ButtonStyle.red
    )
    async def button2_callback(interaction: discord.Interaction):
        await interaction.response.send_message('Button 2 was pressed!', ephemeral=True)
    button2.callback = button2_callback

    # Button 3
    button3 = discord.ui.Button(
        label='Button 3',
        style=discord.ButtonStyle.green
    )
    async def button3_callback(interaction: discord.Interaction):
        await interaction.response.send_message('Button 3 was pressed!', ephemeral=True)
    button3.callback = button3_callback

    # Add buttons to the view
    view.add_item(button1)
    view.add_item(button2)
    view.add_item(button3)

    await interaction.response.send_message(content='Here are your buttons:', view=view)

client.run('MTIzMDk2MjI2OTc0ODQ2NTY2Ng.G99PQ1.04Ch0VvwZbQqS0ZnbPKMjjAra8t2dHv38M9BQ0')
