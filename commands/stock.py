import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import requests
import json
import os
import traceback

from const import USER_STOCKS, CACHE_DIR, DEFUALT_PROFILE_PIC, STOCK_LOGO_DIR, CACHE_DIR_PFP, EXCEPTION_MESSAGE
from write_exception import write_exception

@commands.command()
async def stock(ctx):
    user_id = str(ctx.author.id)

    try:
        with open(USER_STOCKS, 'r') as f:
            stocks = json.load(f)

        if user_id in stocks:
            user_stocks = stocks[user_id]

            # Initialize variables for image creation
            image_width = 500
            image_height = 500
            margin = 20
            y_offset = margin
            font_size = 20
            font = ImageFont.truetype("arial.ttf", font_size)
            image = Image.new("RGBA", (image_width, image_height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(image)

            # Load user's profile picture
            profile_picture_path = os.path.join(CACHE_DIR_PFP, f"{user_id}.png")
            if not os.path.exists(profile_picture_path):
                user = ctx.bot.get_user(int(user_id))
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

            profile_image = Image.open(profile_picture_path).resize((100, 100))
            image.paste(profile_image, (margin, margin))

            stock_logos = {}
            for stock in user_stocks.keys():
                logo_path = os.path.join(STOCK_LOGO_DIR, f"{stock}.png")
                if os.path.exists(logo_path):
                    stock_logos[stock] = Image.open(logo_path).resize((35, 35))  # Resize logo if necessary

            # Draw stock information
            for stock, quantity in user_stocks.items():
                if stock in stock_logos:
                    logo = stock_logos[stock]
                    image.paste(logo, (margin + 120, y_offset))
                    draw.text((margin + 200, y_offset), f"{stock}: {quantity}", font=font, fill=(255, 255, 255))
                    y_offset += logo.height + margin
                else:
                    draw.text((margin + 120, y_offset), f"{stock}: {quantity}", font=font, fill=(255, 255, 255))
                    y_offset += font_size + margin

            # Save and send the image
            image_path = os.path.join(CACHE_DIR, f"{user_id}_stocks.png")
            image.save(image_path)
            await ctx.send(file=discord.File(image_path))

        else:
            await ctx.send("You don't own any stocks.")

    except Exception as e:
        await ctx.send(EXCEPTION_MESSAGE)
        write_exception(traceback.format_exc())