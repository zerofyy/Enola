import datetime
import random
import time
import pytz
from thefuzz import fuzz
from difflib import SequenceMatcher
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
    def _get_progress_bar_segments(bar_type: str) -> tuple[..., ...]:
        """ Helper function for getting different progress bar styles. """

        match bar_type:
            case 'unicode':
                bar_pre, bar_suf = '', ''
                bar_l_seg = ('▱▱', '▰▱', '▰▰')
                bar_m_seg = ('▱▱', '▰▱', '▰▰')
                bar_r_seg = ('▱▱', '▰▱', '▰▰')
            case 'boxes':
                bar_pre, bar_suf = '|', '|'
                bar_l_seg = ('--', '█-', '██')
                bar_m_seg = ('--', '█-', '██')
                bar_r_seg = ('--', '█-', '██')
            case 'emojis':
                bar_pre, bar_suf = '', ''
                bar_l_seg = (Emoji.bar.l_empty, Emoji.bar.l_half, Emoji.bar.l_full)
                bar_m_seg = (Emoji.bar.m_empty, Emoji.bar.m_half, Emoji.bar.m_full)
                bar_r_seg = (Emoji.bar.r_empty, Emoji.bar.r_half, Emoji.bar.r_full)
            case _:
                bar_pre, bar_suf = '[', ']'
                bar_l_seg = ('--', '=-', '==')
                bar_m_seg = ('--', '=-', '==')
                bar_r_seg = ('--', '=-', '==')

        return bar_pre, bar_suf, bar_l_seg, bar_m_seg, bar_r_seg


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

        bar_pre, bar_suf, bar_l_seg, bar_m_seg, bar_r_seg = Misc._get_progress_bar_segments(bar_type)
        percent = round(100 * progress / total, 2)
        segments = int(percent / 10)
        remaining = percent % 10
        info_left, info_right, info_spaces = '', '', len(str(total))

        if display_left == 'number' or display_left == 'both':
            info_left += f'{bar_pre}{progress:<{info_spaces}}/{total}{bar_suf} '
        if display_left == 'percent' or display_left == 'both':
            info_left += f'{bar_pre}{percent:<{6}}%{bar_suf} '
        if display_right == 'number' or display_right == 'both':
            info_right += f' {bar_pre}{progress:<{info_spaces}}/{total}{bar_suf}'
        if display_right == 'percent' or display_right == 'both':
            info_right += f' {bar_pre}{percent:<{6}}%{bar_suf}'

        if percent < 10:
            bar = bar_l_seg[0] if percent < 5 else bar_l_seg[1]
            bar += bar_m_seg[0] * 8 + bar_r_seg[0]

        elif percent == 100:
            bar = bar_l_seg[2] + 8 * bar_m_seg[2] + bar_r_seg[2]

        else:
            bar = bar_l_seg[2] + bar_m_seg[2] * (segments - 1)
            if segments == 9:
                bar += bar_r_seg[0] if remaining < 5 else bar_r_seg[1]
            else:
                bar += bar_m_seg[0] if remaining < 5 else bar_m_seg[1]
                bar += bar_m_seg[0] * (8 - segments) + bar_r_seg[0]

        return f'{info_left}{bar_pre}{bar}{bar_suf}{info_right}'


    @staticmethod
    def sort_dict(input_dict: dict[..., str | int | float], reverse: bool = False) -> dict[..., str | int | float]:
        """
        Sort a dictionary based on its values.

        Arguments:
             input_dict: The unsorted dictionary.
             reverse: Whether to reverse the sort. True for descending, False for ascending.

        Returns:
            The same dictionary, but sorted.
        """

        return dict(sorted(input_dict.items(), key = lambda item: item[1], reverse = reverse))


    @staticmethod
    def make_scoreboard(scores: dict[..., int | float], title: str, emoji: str = None, reverse: bool = True,
                        names: dict[..., str] = None, suffixes: tuple[str, str] = None) -> str:
        """
        Create a scoreboard.

        Arguments:
             scores: Dictionary of scores for each participant.
             title: The scoreboard title.
             emoji: The scoreboard title emoji.
             reverse: Whether to reverse the scoreboard. True for descending, False for ascending.
             names: The participant names to display on the scoreboard.
                    Uses the scores keys if None, otherwise this dictionary must have the same keys as scores.
             suffixes: The suffixes to show after each score.
                       The first string is for singular, and the second for plural.

        Returns:
            A scoreboard with Discord message formatting.
        """

        if emoji is None:
            emoji = ''
        if names is None:
            names = {key : key for key in scores.keys()}
        if suffixes is None:
            suffixes = ('', '')

        board = f'## {emoji} {title}'
        if len(scores) == 0:
            board += f'\n> There aren’t any entries yet.'
            return board

        name_spacing, score_spacing = 0, 0
        for name, score in names.items():
            name_spacing = max(name_spacing, len(name))
            score_spacing = max(score_spacing, len(str(score)))

        scores = Misc.sort_dict(scores, reverse)
        counter = 0
        for key, val in scores.items():
            counter += 1
            match counter:
                case 1: medal = '🥇'
                case 2: medal = '🥈'
                case 3: medal = '🥉'
                case _: medal = Emoji.blank

            name, score = names[key], f'{val:,}'
            suffix = suffixes[0] if val == 1 else suffixes[1]
            board += f'\n> {medal} `{name:<{name_spacing}} | {score:>{score_spacing}} {suffix}`'

            if counter == 10:
                if len(scores) > 10:
                    remaining = len(scores) - 10
                    board += f'\n> \n> ... and {remaining:,} more ...'
                break

        return board


    @staticmethod
    def get_current_time(seconds_only: bool = False, timezone: str = 'default',
                         time_format: str = '%d-%m-%Y %H:%M:%S', as_dt: bool = False) -> str | float | datetime:
        """
        Get the current time.

        Arguments:
             seconds_only: Whether to return the number of seconds since the Epoch.
             timezone: A specific timezone.
             time_format: A datetime format, example: %d/%m/%Y, %H:%M:%S . Does not apply if as_dt==True.
             as_dt: Whether to return a datetime object.

        Returns:
            The current time as an object, formatted string, or in seconds only.
        """

        if seconds_only:
            return time.time()

        if timezone == 'default':
            timezone = Bot.timezone

        timezone = pytz.timezone(timezone)
        datetime_now = datetime.datetime.now(timezone).replace(microsecond = 0)

        if as_dt:
            return datetime_now

        return datetime_now.strftime(time_format)


    @staticmethod
    def get_specific_time(hour: int, minute: int, second: int, microsecond: int,
                          timezone: str = 'default', time_format: str = None) -> str | datetime.time:
        """
        Get a specific time.

        Arguments:
             hour: The specific hour (0 - 23).
             minute: Number of minutes.
             second: Number of seconds.
             microsecond: Number of microseconds.
             timezone: The specific timezone.
             time_format: A datetime format, example: %d/%m/%Y, %H:%M:%S .

        Returns:
            The specified time as an object or a formatted string.
        """

        if timezone == 'default':
            timezone = Bot.timezone

        timezone = pytz.timezone(timezone)
        datetime_specific = datetime.time(hour, minute, second, microsecond, timezone)

        if time_format:
            return datetime_specific.strftime(time_format)
        
        return datetime_specific


    @staticmethod
    def format_datetime(dt: datetime.datetime, style: str = None) -> str:
        """
        Format a datetime object into a Discord-friendly representation.

        Styles:
            - t | 22:57
            - T | 22:57:58
            - d | 17/05/2016
            - D | 17 May 2016
            - f | 17 May 2016 22:57
            - F | Tuesday, 17 May 2016 22:57
            - R | 5 years ago

        Arguments:
             dt: The datetime object.
             style: The format style.

        Returns:
            A formatted datetime string for Discord.
        """

        return discord.utils.format_dt(dt, style)


    @staticmethod
    def convert_alphanum(string: str, ignore: str = None) -> str:
        """
        Remove all non-alphanumerical characters in a string.

        Arguments:
            string: The string to convert.
            ignore: A string of characters non-alphanumerical characters to keep.

        Returns:
            The converted string.
        """

        allowed_chars = 'abcdefghijklmnopqrstuvwxyz0123456789 '
        if ignore:
            allowed_chars += ignore.lower()

        return ''.join([char for char in string if char.lower() in allowed_chars])

    @staticmethod
    def convert_invisible(visible: str, invisible: str) -> str:
        """
        Create a Discord message with an invisible part.

        Arguments:
            visible: The visible part of the message.
            invisible: The invisible part of the message.

        Returns:
            A string formatted for Discord.
        """

        return f'{visible} ||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​|| _ _ _ _ _ _ {invisible}'


    @staticmethod
    def get_similarity_ratio(string1: str, string2: str, mode: str = 'sequence') -> float:
        """
        Get the similarity ratio between two strings.

        Modes:
            - sequence   | Most accurate calculations.
            - fuzzy      | Slightly more relaxed calculations.
            - partial    | Check if either string contains the other.
            - positional | Check if the second string contains the first.
            - token_sort | Checks if both strings have the same words.
            - token_set  | Check if both strings have the same words, ignoring duplicates.

        Arguments:
            string1: The first string.
            string2: The second string.
            mode: The mode to use when calculating the similarity ratio.

        Returns:
            A number between 0 and 1 representing how similar the two strings are.
        """

        match mode:
            case 'fuzzy':
                ratio = fuzz.ratio(string1, string2) / 100

            case 'partial':
                ratio = fuzz.partial_ratio(string1, string2) / 100

            case 'positional':
                ratio = fuzz.partial_ratio(string1, string2) / 100
                if string1 not in string2:
                    ratio /= 1.75

            case 'token_sort':
                ratio = fuzz.token_sort_ratio(string1, string2) / 100

            case 'token_set':
                ratio = fuzz.token_set_ratio(string1, string2) / 100

            case _:
                ratio = SequenceMatcher(None, string1, string2).ratio()

        return ratio


    @staticmethod
    def autocomplete(query: str, completions: tuple[str, ...],
                     defaults: tuple[str, ...] = None) -> tuple[str, ...] | None:
        """
        Get autocomplete suggestions based on a list of possible completions.

        Arguments:
             query: The string to complete.
             completions: Possible completions.
             defaults: Default suggestions to return if no other suggestions are found.

        Returns:
            A list of suggestions or the default list if no other suggestions are found.
        """

        query = query.lower()
        suggestions = tuple(
            string for string in completions
            if string.lower().startswith(query)
            or Misc.get_similarity_ratio(string, query, mode = 'token_set') > 0.5
        )

        if suggestions:
            return suggestions

        return defaults


    @staticmethod
    def find_member(query: str, server: discord.Guild) -> discord.Member | None:
        """
        Find a member of a specific Discord server based on a given query.

        Arguments:
            query: The member's name, nickname, ID, or mention.
            server: The Discord server to search.

        Returns:
            The Discord member object or None if not found.
        """

        if query.startswith('<@'):
            query = query[2:-1]

        if query.isdigit():
            user = server.get_member(int(query))
            if user:
                return user

        query = query.lower()
        best_match, best_ratio = None, 0
        for member in server.members:
            ratio = max(
                Misc.get_similarity_ratio(query, member.display_name, mode = 'positional'),
                Misc.get_similarity_ratio(query, member.name, mode = 'sequence'),
            )

            if ratio >= 0.6 and ratio > best_ratio:
                best_match = member
                best_ratio = ratio

                if ratio == 1:
                    break

        return best_match


    @staticmethod
    def get_random_member(server: discord.Guild, exclude_member: discord.Member = None,
                          exclude_bots: bool = False) -> discord.Member | None:
        """
        Get a random member from the specified Discord server.

        Arguments:
            server: The Discord server to search.
            exclude_member: The member to exclude, usually the command author.
            exclude_bots: Whether to exclude bots from the possible choices.

        Returns:
              A randomly chosen member object or None if there are no valid choices.
        """

        members = list(server.members)
        if exclude_member:
            members.remove(exclude_member)

        if exclude_bots:
            members = [member for member in members if not member.bot]

        if len(members) == 0:
            return None

        return random.choice(members)


__all__ = ['Misc']
