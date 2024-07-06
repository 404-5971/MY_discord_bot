import discord
from discord.ext import commands
import asyncio
from money_bals import *

@commands.command()
async def  sudo(ctx, *agreements):
    async def confirm_action(ctx):
        def check(message):
            return (
                message.author == ctx.author
                and message.content.lower() == '$confirm'
                and message.author.guild_permissions.administrator
            )

        try:
            await ctx.send("Are you sure? Type `$confirm` to confirm.")
            confirmation = await ctx.bot.wait_for('message', check=check, timeout=30)
            return True
        except asyncio.TimeoutError:
            await ctx.send("Confirmation timed out.")
            return False
    if "hack" in agreements and "watch" in agreements and "gay" in agreements and "porn" in agreements:
        await ctx.send("Executing command with sudo privileges... \n[gay porn.com](https://www.youtube.com/@BionicOctopus)")
        # Implement your command logic here
    elif ctx.author.guild_permissions.administrator:
        if "lol" in agreements:
            if await confirm_action(ctx):
                await ctx.send("You have access to the **MOST POEWRFUL** *lol* out there! Use it wisely.")
        elif "ban" in agreements:
            # Check if there is a user mentioned
            if len(ctx.message.mentions) == 1:
                user_to_ban = ctx.message.mentions[0]
                # Check if the bot has permissions to ban members
                if ctx.guild.me.guild_permissions.ban_members:
                    try:
                        if await confirm_action(ctx):
                            # Ban the user
                            await ctx.guild.ban(user_to_ban, reason="Banned by sudo command")
                            await ctx.send(f"User {user_to_ban.mention} has been banned.")
                    except Exception as e:
                        await ctx.send(f"{user_to_ban.mention} was too poweruful to ban because {e}")
        elif "kick" in agreements:
            # Check if there is a user mentioned
            if len(ctx.message.mentions) == 1:
                user_to_kick = ctx.message.mentions[0]
                # Check if the bot has permissions to ban members
                if ctx.guild.me.guild_permissions.ban_members:
                    try:
                        if await confirm_action(ctx):
                            await ctx.guild.kick(user_to_kick, reason="Kicked by sudo command")
                            await ctx.send(f"User {user_to_kick.mention} has been kicked.")
                    except Exception as e:
                        await ctx.send(f"{user_to_kick.mention} was too poweruful to kick because {e}")
        elif "remove" in agreements:
            # Check if there is a user mentioned and a valid amount provided
            if len(ctx.message.mentions) == 1:
                user_to_remove = ctx.message.mentions[0]
                amount_index = agreements.index("remove") + 1
                if amount_index < len(agreements):
                    amount_str = agreements[amount_index]
                    try:
                        if await confirm_action(ctx):
                            amount = float(amount_str.replace(',', ''))
                            # Update the user's money balance here
                            user_id = str(user_to_remove.id)
                            money_data = load_money_data()
                            if user_id in money_data:
                                if money_data[user_id] >= amount:
                                    money_data[user_id] -= amount
                                    save_money_data(money_data)
                                    await ctx.send(f"Successfully removed {amount:.2f} from {user_to_remove.mention}'s account.")
                                else:
                                    await ctx.send(f"{user_to_remove.mention} doesn't have enough money.")
                            else:
                                await ctx.send(f"{user_to_remove.mention} doesn't have a money account.")
                        else:
                            await ctx.send(f"{user_to_remove.mention} doesn't have a money account.")
                    except ValueError:
                        await ctx.send("Invalid amount provided.")
                else:
                    await ctx.send("No amount provided.")
            else:
                await ctx.send("You need to mention a user to remove money from.")
        elif "add" in agreements:
            # Check if there is a user mentioned and a valid amount provided
            if len(ctx.message.mentions) == 1:
                user_to_add = ctx.message.mentions[0]
                amount_index = agreements.index("add") + 1
                if amount_index < len(agreements):
                    amount_str = agreements[amount_index]
                    try:
                        if await confirm_action(ctx):
                            amount = float(amount_str.replace(',', ''))
                            # Update the user's money balance here
                            user_id = str(user_to_add.id)
                            money_data = load_money_data()
                            if user_id in money_data:
                                money_data[user_id] += amount
                                save_money_data(money_data)
                                await ctx.send(f"Successfully added {amount:.2f} from {user_to_add.mention}'s account.")
                            else:
                                await ctx.send(f"{user_to_add.mention} doesn't have a balance")
                    except ValueError:
                        await ctx.send("Invalid amount provided.")
                else:
                    await ctx.send("No amount provided.")
            else:
                await ctx.send("You need to mention a user to add money.")
        elif "money" in agreements:
            # Check if there is a user mentioned
            if len(ctx.message.mentions) == 1:
                user_to_check = ctx.message.mentions[0]
                user_id = str(user_to_check.id)
                money_data = load_money_data()
                if user_id in money_data:
                    await ctx.send(f"{user_to_check.mention} has ${money_data[user_id]:,.2f} in their account.")
                else:
                    await ctx.send(f"{user_to_check.mention} doesn't have a money account.")
            else:
                await ctx.send("You need to mention a user to check their money balance.")
        elif "help" in agreements:
            embed = discord.Embed(title="Sudo Help", description="List of sudo commands.", color=discord.Color.blue())
            embed.add_field(name="`$sudo lol`", value="This command allows you to use the most powerful lol, **in existence!**", inline=False)
            embed.add_field(name="`$sudo ban @username`", value="This command allows you to ban a member, with only a command.", inline=False)
            embed.add_field(name="`$sudo kick @username`", value="This command allows you to kick a member, with only a command.", inline=False)
            embed.add_field(name="`$sudo remove amount @username`", value="This command allows you to remove an amount of money from a user's account.", inline=False)
            embed.add_field(name="`$sudo add amount @username`", value="This command allows you to add an amount of money from a user's account.", inline=False)
            embed.add_field(name="`$sudo money @username`", value="This command allows you to check the balance of a user.", inline=False)
            await ctx.send(embed=embed)