import discord
from discord import app_commands
from discord.ext import commands
import openai
import asyncio
import json

def get_config():
    with open('./config.json', 'r') as f:
        config = json.load(f)

    return config

config = get_config()

openai.api_key = config['openai_key']
bot_token = config['bot_token']

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="$", intents=intents)

@bot.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType.listening, name="to your demands")
    await bot.change_presence(status=discord.Status.idle, activity=activity)
    print("Ready!")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

@bot.tree.command(name="text")
@app_commands.describe(
    prompt='Start a conversation, ask a question, or fix some code'
)
async def text(
    interaction: discord.Interaction,
    prompt: str
):

    await interaction.response.defer()
    await asyncio.sleep(5)
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0,
    )
    await interaction.followup.send(response['choices'][0]["text"])
    


@bot.tree.command(name="image")
@app_commands.describe(
    prompt='Input image details and attributes'
)
async def image(
    interaction: discord.Interaction,
    prompt: str
):
    await interaction.response.defer()
    await asyncio.sleep(5)
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    await interaction.followup.send(response['data'][0]['url'])


bot.run('MTA2NDYxNDc0NzUxOTA2MjAxNg.GpmGV3.OiVTEgE4udb5IVFlx24q6qP9Y5YuPYhbAxQRvM')