import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import os
import requests

from money_bals import *
from const import CACHE_DIR_PFP, DEFUALT_PROFILE_PIC, LEADERBOARD_PIC

@commands.command()
async def leaderboard(ctx):
    # Load money balances from JSON
    with open(MONEY_JSON_FILEPATH, 'r') as f:
        money_balances = json.load(f)
    
    # Sort the money balances dictionary by values (money) in descending order
    sorted_money_balances = dict(sorted(money_balances.items(), key=lambda item: item[1], reverse=True))
    
    # Create an empty image with desired dimensions
    image_width = 600
    image_height = 770
    background_color = (54,57,62)  # Darkish grey background
    image = Image.new("RGB", (image_width, image_height), background_color)
    
    # Load font with larger size
    font_size = 30
    font = ImageFont.truetype("arial.ttf", font_size)
    
    # Initialize drawing context
    draw = ImageDraw.Draw(image)
    
    # Load profile pictures and draw them with ranks and money balances
    count = 0
    y_offset = 10
    for user_id, money_balance in sorted_money_balances.items():
        # Skip the user with ID 1175890644191957013
        if user_id == '1175890644191957013':
            continue
        
        user = ctx.bot.get_user(int(user_id))
        if user is not None:
            count += 1
            
            # Check if profile picture is in cache
            profile_picture_path = os.path.join(CACHE_DIR_PFP, f"{user.id}.png")
            if os.path.exists(profile_picture_path):
                profile_picture = Image.open(profile_picture_path)
            else:
                # Download profile picture
                if user.avatar is None:
                    # Handle default profile picture
                    profile_picture = Image.open(DEFUALT_PROFILE_PIC)  # Provide path to your default profile picture
                else:
                    profile_picture_response = requests.get(user.avatar.url, stream=True)
                    profile_picture_response.raise_for_status()
                    profile_picture = Image.open(profile_picture_response.raw)
                
                # Save profile picture to cache
                profile_picture.save(profile_picture_path)
            
            # Resize profile picture to fit
            profile_picture = profile_picture.resize((70, 70))
            # Draw profile picture
            image.paste(profile_picture, (10, y_offset))
            # Determine color based on rank
            if count == 1:
                rank_color = (255, 215, 0)  # Gold color
            elif count == 2:
                rank_color = (192, 192, 192)  # Silver color
            elif count == 3:
                rank_color = (205, 127, 50)  # Bronze color
            else:
                rank_color = (255, 255, 255)  # White color
            # Draw user's rank, username, and money balance with appropriate color and larger dots
            draw.text((100, y_offset + 10), f"•  #{count} • {user.name}", fill=rank_color, font=font)
            draw.text((390, y_offset + 10), "${:,.2f}".format(money_balance), fill=(255, 255, 255), font=font)  # White color for money balance with commas
            # Increment y_offset for next user
            y_offset += 75
        if count == 10:
            break
    
    # Save the image
    image.save(LEADERBOARD_PIC)
    
    # Create an embed
    embed = discord.Embed(title="Money Leaderboard", color=0x282b30)
    embed.set_image(url="attachment://leaderboard.png")
    
    # Send the embed with the image file
    await ctx.send(embed=embed, file=discord.File(LEADERBOARD_PIC))