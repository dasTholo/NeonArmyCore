from utils.config_utils import load_config_file

config = load_config_file("../../bot_config.toml")

from bot import DiscordBot

print(config)
bot = DiscordBot(config)
bot.run(config.discord_settings.token)
