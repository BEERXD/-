import discord
from discord.ext import commands
import yt_dlp

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='>', intents=intents)

@bot.event
async def on_ready():
    print(f'✅ บอทออนไลน์แล้ว: {bot.user}')

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        await ctx.author.voice.channel.connect()
        await ctx.send("เข้าห้องเสียงแล้ว 🎶")
    else:
        await ctx.send("คุณต้องอยู่ในห้องเสียงก่อนน้า")

@bot.command()
async def play(ctx, url):
    if not ctx.voice_client:
        await ctx.invoke(bot.get_command('join'))

    ydl_opts = {'format': 'bestaudio/best', 'quiet': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        audio_url = info['url']
        source = await discord.FFmpegOpusAudio.from_probe(audio_url)
        ctx.voice_client.stop()
        ctx.voice_client.play(source)
        await ctx.send(f"🎧 Playing: {info['title']}")

@bot.command()
async def stop(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("⏹️ หยุดเพลงแล้วจ้า")

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 ออกจากห้องแล้ว")

# ใส่ Token ของคุณตรงนี้
bot.run("วาง TOKEN ของคุณตรงนี้")