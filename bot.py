# bot.py
import os
import discord
import random

from dotenv import load_dotenv
from discord.ext import commands
from openai import AzureOpenAI

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )

@bot.command(name='ai', help='Responds with chat completion from AzureOpenAI')
#@commands.has_role('Admin')
async def azure_openai(ctx):
   
    msg = ctx.message.content.replace("!ai","").strip() 
    
    client = AzureOpenAI(
    azure_endpoint = os.getenv("AZURE_TURBO_API_ENDPOINT"), 
    api_key=os.getenv("AZURE_TURBO_API_KEY"),  
    api_version="2023-05-15"
    )
        
    response = client.chat.completions.create(
        model="gpt-35-turbo", # model = "deployment_name".
        messages=[
            {"role": "system", "content": "Eres un servicial asistente. Proporcionas respuesta a las preguntas que formulan los usuarios"},
            {"role": "user", "content": msg}
        ]
    )    

    await ctx.send(response.choices[0].message.content)     

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

bot.run(TOKEN)
