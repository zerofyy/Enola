import discord
from discord.ext import commands


class Bot:
    """ Singleton class representing the Discord bot client. """

    _instance = None
    location: str = None
    prefix: str = None
    client: commands.Bot = None
    timezone: str = None


    def __new__(cls) -> 'Bot':
        """ Create a new instance of the Bot class if it doesn't already exist. """

        if cls._instance is None:
            cls._instance = super(Bot, cls).__new__(cls)

        return cls._instance


    def setup(self, client: type[commands.Bot], location: str = 'home',
              prefix: str = '>', timezone: str = None) -> None:
        """
        Set up the Discord bot client.

        Arguments:
             client: Bot class with custom setup_hook function.
             location: The hosting location of the bot.
             prefix: The commands prefix.
             timezone: The default timezone.
        """

        self.location = location
        self.prefix = prefix
        self.timezone = timezone
        self.client = client(
            command_prefix = prefix,
            intents = discord.Intents.all(),
            allowed_mentions = discord.AllowedMentions(everyone = False, roles = False, replied_user = False),
            case_insensitive = True
        )


__all__ = ['Bot']
