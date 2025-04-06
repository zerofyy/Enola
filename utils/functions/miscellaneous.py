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
    def create_progress_bar(bar_type: str, progress: int | float, total: int | float,
                           display_left: str = None, display_right: str = None) -> str:
        """
        Create a progress bar.

        Bar Types:
            - text | Plain text symbols.
            - unicode | Special characters.
            - boxes | Combination of unicode characters and plain text.
            - emojis | Custom Discord emojis.

        Display Options:
            - percent | Show progress as percentage.
            - number | Show progress as a number.
            - both | Show progress both as a number and percentage.
            - None | Don't show any additional information.

        Arguments:
             bar_type: The type of progress bar.
             progress: The current progress value.
             total: The maximum progress value.
             display_left: What to display left of the bar.
             display_right: What to display right of the bar.

        Returns:
            The progress bar as a string.
        """

        match bar_type:
            case 'unicode':
                bar_segments = ('▱▱', '▰▱', '▰▰',
                                '▱▱', '▰▱', '▰▰',
                                '▱▱', '▰▱', '▰▰')
            case 'boxes':
                bar_segments = ('--', '█-', '██',
                                '--', '█-', '██',
                                '--', '█-', '██')
            case 'emojis':
                bar_segments = (Emoji.bar.l_empty, Emoji.bar.l_half, Emoji.bar.l_full,
                                Emoji.bar.m_empty, Emoji.bar.m_half, Emoji.bar.m_full,
                                Emoji.bar.r_empty, Emoji.bar.r_half, Emoji.bar.r_full)
            case _:
                bar_segments = ('--', '=-', '==',
                                '--', '=-', '==',
                                '--', '=-', '==')

        percent = '{0:.2f}'.format(100 * (progress / float(total)))
        filled = 20 * progress // total

        if bar_type == 'emojis':
            pass
        else:
            bar = bar_segments[0] + bar_segments[]

        #######
        # percent = ("{0:.1f}").format(100 * (iteration / float(total)))
        # filled_length = int(length * iteration // total)
        # bar = fill * filled_length + '-' * (length - filled_length)
        #######


__all__ = ['Misc']
