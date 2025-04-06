from difflib import SequenceMatcher
from fuzzywuzzy import fuzz
from uuid import getnode as get_mac_address

import discord

from utils.core import Bot, DB
from utils.assets import Emoji


Bot = Bot()
DB = DB()
client = Bot.client


class Misc:
    """ Class for various miscellaneous functions that don't fit elsewhere. """

    @staticmethod
    def get_location(auto: bool = False) -> dict[str, str]:
        """
        Get information about the current hosting location of the bot.

        Arguments:
            auto: Whether to check for the hosting location in the database.

        Returns:
            A dictionary containing hosting location information.
        """

        mac_address = ':'.join(('%012X' % get_mac_address())[i:i + 2] for i in range(0, 12, 2))
        host = Bot.location if Bot.location else 'unknown'

        if auto:
            doc = DB.find('devices', {'mac_address' : mac_address})
            if doc:
                return doc

        DB.update('devices', {'mac_address' : mac_address}, {
            'set' : {'host' : host}
        }, upsert = True)

        return {'mac_address' : mac_address, 'host' : host}


    @staticmethod
    def get_prefix(auto: bool = False) -> str | None:
        """
        Get the bot's commands prefix.

        Arguments:
            auto: Whether to automatically pick the prefix based on the bot's hosting location.

        Returns:
            The bot's commands prefix or None if not set/found.
        """

        if auto:
            match Misc.get_location()['host']:
                case 'home':
                    return '>'
                case 'server':
                    return '0'
                case _:
                    return '.'

        return Bot.prefix


    @staticmethod
    def create_loading_bar(bar_type: str, total: int | float, progress: int | float,
                           display_left: str = None, display_right: str = None) -> str:
        """
        Create a loading bar.

        Bar Types:
            - text | Plain text symbols.
            - unicode | Special characters.
            - emojis | Custom Discord emojis.

        Display Options:
            - percent | Show bar progress as percentage.
            - number | Show bar progress as a number.
            - both | Show bar progress both as a number and percentage.
            - None | Don't show any additional information.

        Arguments:
             bar_type: The type of loading bar.
             total: The maximum bar value.
             progress: The current bar value.
             display_left: What to display left of the bar.
             display_right: What to display right of the bar.

        Returns:
            The loading bar as a string.
        """

        match bar_type:
            case 'unicode':
                bar_segments = {'str_empty' : '▱', 'str_half' : '▱', 'str_full' : '▰',
                                'mid_empty' : '▱', 'mid_half' : '▱', 'mid_full' : '▰',
                                'end_empty' : '▱', 'end_half' : '▱', 'end_full' : '▰'}

            case 'emojis':
                bar_segments = {'str_empty' : Emoji.bar_str_empty, 'str_half' : Emoji.bar_str_half, 'str_full' : Emoji.bar_str_full,
                                'mid_empty' : Emoji.bar_mid_empty, 'mid_half' : Emoji.bar_mid_half, 'mid_full' : Emoji.bar_mid_full,
                                'end_empty' : Emoji.bar_end_empty, 'end_half' : Emoji.bar_end_half, 'end_full' : Emoji.bar_end_full}

            case _:
                bar_segments = {'str_empty' : '-', 'str_half' : '-', 'str_full' : '=',
                                'mid_empty' : '-', 'mid_half' : '-', 'mid_full' : '=',
                                'end_empty' : '-', 'end_half' : '-', 'end_full' : '='}

        """
        - text    | [ 4/10] [====------] [40%]
        - unicode | 4/10 ▰▰▰▰▱▱▱▱▱▱ 40%
        - emojis  | ...
        """


__all__ = ['Misc']
