import asyncio
import os
import discord

from dotenv import load_dotenv
from discord.ext import commands
from gtts import gTTS, lang
from helpers import get_language_code
from translate import Translator

# Replace with your bot token
load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
assert isinstance(TOKEN, str), "A discord bot token is required"

# Supported languages based on gTTS
supported_languages = lang.tts_langs()
supported_languages["nan"] = ""

intents = discord.Intents.default()
intents.message_content = True
text_to_translate = "Good morning China, now I have ice cream."
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.command()
async def zao(ctx, language: str):
    # Validate user in voice channel
    if not ctx.author.voice:
        return

    # Validate language
    language_code = get_language_code(language)
    if language_code not in supported_languages:
        await ctx.send(f"{language} is not supported")
        return

    if language_code == "nan":
        # Easter egg
        await ctx.send("🇨🇳 🇨🇳  🇨🇳 🇨🇳")
    else:
        # Translate text using googletrans
        translator = Translator(to_lang=language_code)
        translated_text = translator.translate(text=text_to_translate)
        await ctx.send(translated_text)

    # Generate TTS audio
    tts_audio = f"audio/tts-{language_code}.mp3"
    if not os.path.isfile(tts_audio):
        tts = gTTS(text=translated_text, lang=language_code)
        tts.save(tts_audio)

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
