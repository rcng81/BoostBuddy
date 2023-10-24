import discord
import os
import asyncio
from discord.ext import commands, tasks
from time import sleep
from datetime import datetime, timedelta
import pytz
from responses import get_daily_quote
from webserver import keep_alive  # Import the keep_alive function from your webserver.py

intents = discord.Intents.default()
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

channel_id = 1038236010611474433  # Ensure this is the ID of your channel


@bot.event
async def on_ready():
  print(f'Logged in as {bot.user.name} ({bot.user.name})')
  post_daily_quote.start()  # Starts the loop


def calc_time_until_next_run():
  timezone = pytz.timezone("America/New_York")
  now_est = datetime.now(timezone)
  next_run = now_est.replace(hour=8, minute=30, second=0, microsecond=0)
  if now_est >= next_run:
    next_run += timedelta(days=1)
  delay = (next_run - now_est).total_seconds()
  return delay


@tasks.loop(hours=24)  # Loop will run every 24 hours
async def post_daily_quote():
  message = get_daily_quote()
  channel = bot.get_channel(channel_id)
  if channel:
    await channel.send(message)
  else:
    print(f"No channel with ID {channel_id} found.")


@post_daily_quote.before_loop
async def before_post_daily_quote():
  await bot.wait_until_ready()  # Ensure the bot has loaded
  delay = calc_time_until_next_run()  # Calculate the delay
  print(f"Next message scheduled in {delay} seconds")
  await asyncio.sleep(delay)  # Sleep until the next scheduled time


# This keeps your bot running 24/7 by pinging a web server created in webserver.py
keep_alive()  # Call this before running the bot

bot.run(os.getenv(
    'DISCORD_BOT_TOKEN'))  # Use the token from the environment variable
try:
  keep_alive()
  bot.run('DISCORD_BOT_TOKEN')
except discord.errors.HTTPException:
  os.system("echo RATELIMITED, TRYING AGAIN")
  sleep(25)
  os.system("kill 1")