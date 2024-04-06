import asyncio
import os
import discord

from dotenv import load_dotenv
from discord.ext import commands
from helpers import generate_zao_response

# Replace with your bot token
load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
assert isinstance(TOKEN, str), "A discord bot token is required"

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.command()
async def zao(ctx, language: str):
    # Validate user in voice channel
    if not ctx.author.voice:
        return

    zao_response = generate_zao_response(language)

    # Send text response
    await ctx.send(zao_response.text)
    if zao_response.audio_path is None:
        return
    tts_audio = zao_response.audio_path

    # Join voice
    try:
        voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if not voice_client:
            voice_channel = ctx.author.voice.channel
            voice_client = await voice_channel.connect()

        # Play audio using FFmpegAudioSource
        source = discord.FFmpegPCMAudio(source=tts_audio)
        voice_client.play(source, after=lambda e: print("Audio finished playing"))

    except:
        await voice_client.disconnect()


@bot.event
async def on_voice_state_update(member, before, after):
    if bot.user is not None and not member.id == bot.user.id:
        return
    elif before.channel is None:
        voice = after.channel.guild.voice_client
        time = 0
        while True:
            await asyncio.sleep(1)
            time = time + 1
            if voice.is_playing() and not voice.is_paused():
                time = 0
            if time == 10:
                await voice.disconnect()
            if not voice.is_connected():
                break


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


bot.run(TOKEN)
