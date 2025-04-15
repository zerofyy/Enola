import os
import glob
import asyncio
import logging

import discord

from utils.core import Bot
from utils.assets import Emoji, Channels, Coloring
from utils.functions import Misc


client = Bot().client
Text = Coloring.Text


class LogLevel:
    """ Class for log level definitions. """

    def __init__(self, code: str, emoji: str, color: str, embed_color: int) -> None:
        """
        Create a new LogLevel object.

        Arguments:
            code: The prefix of each log message.
            emoji: The emoji that appears in log entries sent to Discord.
            color: The text color of each log entry.
            embed_color: The embed color of log entries sent to Discord.
        """

        self.code, self.emoji, self.color, self.embed_color = code, emoji, color, embed_color


    def get_info(self) -> tuple[str, str, str, int]:
        """ Get the log level information. """

        return self.code, self.emoji, self.color, self.embed_color


class Logger:
    """ Singleton class for logging. """

    _instance = None
    file: str = None
    INFO = LogLevel('[i]', Emoji.info, Coloring.Text.li_blue, Coloring.blue)
    OK = LogLevel('[o]', Emoji.check, Coloring.Text.li_green, Coloring.green)
    NOTICE = LogLevel('[*]', Emoji.megaphone, Coloring.Text.yellow, Coloring.yellow)
    WARNING = LogLevel('[!]', Emoji.warning, Coloring.Text.li_yellow, Coloring.gold)
    ERROR = LogLevel('[-]', Emoji.error, Coloring.Text.li_red, Coloring.red)
    CRITICAL = LogLevel('[X]', Emoji.error_crit, Coloring.Text.red, Coloring.black)
    DEFAULT = LogLevel('[?]', Emoji.note, Coloring.Rest.fg, Coloring.white)


    def __new__(cls) -> 'Logger':
        """ Create a new instance of the Logger class if it doesn't already exist. """

        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)

        return cls._instance


    def set_file(self, path: str) -> None:
        """
        Change the current logs file.

        Arguments:
             path: Path to the new logs file.
        """

        self.file = path


    def get_file(self) -> str | None:
        """ Get the path to the current logs file. """

        return self.file


    def new_file(self) -> None:
        """ Create a new logs file and set it as the current one. """

        time = Misc.get_current_time(time_format = '%d-%m-%Y %H-%M-%S')
        self.file = f'logs/{time}.log'
        self.ok('Logger', 'New logs file created.')


    @classmethod
    def get_level_info(cls, level: str) -> tuple[str, str, str, int]:
        """
        Get information for a specific log level.

        Arguments:
            level: The log level name.

        Returns:
            A tuple containing the code, emoji, color, and embed color for the given log level.
        """

        level = level.lower()
        for name, obj in dict(cls.__dict__).items():
            if name.lower() == level and isinstance(obj, LogLevel):
                return obj.get_info()

        return cls.DEFAULT.get_info()


    def _log(self, level: str, title: str, message: str, report: bool = None) -> None:
        """
        Helper function for making log entries.

        Arguments:
            level: The log level.
            title: Title of the log message, usually the module from which it is logged.
            message: The log message.
            report: Whether to send the log entry to Discord. Leave None to use config settings.
        """

        time = Misc.get_current_time()
        code, _, color, _ = self.get_level_info(level)

        file_format = f'{code} [{time}][{title.center(25)}]'
        cons_format = f'{color}{code} {Text.cyan}[{time}]{Text.li_magenta}[{title.center(25)}]'

        lines = message.split('\n')
        file_entry = f'{file_format} {lines[0]}'
        cons_entry = f'{cons_format} {lines[0]}'

        spacing = ' ' * len(file_format)
        for line in lines[1:]:
            file_entry += f'\n{spacing} {line}'
            cons_entry += f'\n{spacing} {color}{line}'

        print(cons_entry)
        with open(self.file, 'a', encoding = 'UTF-8') as file:
            file.write(file_entry)

        if report is None:
            report = True  # TODO: Implement config logic.

        if report:
            asyncio.run(self.report(level, message, title))


    def info(self, title: str, message: str, report: bool = None) -> None:
        """ Log an informational message. """

        self._log('info', title, message, report)


    def ok(self, title: str, message: str, report: bool = None) -> None:
        """ Log an informational message of a successfully finished process. """

        self._log('ok', title, message, report)


    def notice(self, title: str, message: str, report: bool = None) -> None:
        """ Log a message that should be acknowledged. """

        self._log('notice', title, message, report)


    def warning(self, title: str, message: str, report: bool = None) -> None:
        """ Log a warning message. """

        self._log('warn', title, message, report)


    def error(self, title: str, message: str, report: bool = None) -> None:
        """ Log an error message. """

        self._log('error', title, message, report)


    def critical(self, title: str, message: str, report: bool = None) -> None:
        """ Log a critical error message. """

        self._log('crit', title, message, report)


    def log(self, title: str, message: str, report: bool = None) -> None:
        """ Log a level-less message. """

        self._log('?', title, message, report)


    def get_log(self, option: str = 'current') -> str | list[str]:
        """
        Get paths to log files.

        Options:
            - last | The previous logs file.
            - current | The current logs file.
            - all | All log files.

        Arguments:
             option: Which log files to search for.

        Returns:
            The paths to the selected log files.
        """

        files = glob.glob('logs/*')

        match option:
            case 'last':
                return max(files, key = os.path.getctime)
            case 'all':
                return files
            case _:
                return self.file


    async def archive(self, path: str) -> None:
        """
        Move a logs file to Discord.

        Arguments:
             path: The path to the specific logs file.
        """

        channel = client.get_channel(Channels.logs)
        file_name = path.split('\\')[-1].split('/')[-1][:-4]
        await channel.send(f'### {Emoji.folder} Archived: {file_name}', file = discord.File(path))

        if path != self.file:
            os.remove(path)


    async def report(self, level: str, text: str, title: str = None) -> None:
        """
        Send a log entry to Discord.

        Arguments:
            level: The log level.
            text: The log message.
            title: The title of the log entry.
        """

        level = level.lower()
        if level in ('warn', 'error', 'crit'):
            channel = client.get_channel(Channels.errors)
        else:
            channel = client.get_channel(Channels.logs)

        _, emoji, _, color = self.get_level_info(level)

        if title:
            title = f'### {emoji} {title}'

        embed = discord.Embed(color = color, description = text, timestamp = Misc.get_current_time(as_dt = True))
        await channel.send(title, embed = embed)


class LogsHandler(logging.Handler):
    """ Class for redirecting Discord logs to the custom logger. """

    log_levels = {
        logging.DEBUG : Logger.log,
        logging.INFO : Logger.info,
        logging.WARNING : Logger.warning,
        logging.ERROR : Logger.error,
        logging.CRITICAL : Logger.critical
    }


    def __init__(self) -> None:
        """ Create a new LogsHandler object. """

        super().__init__()
        self.logger = Logger()


    def emit(self, record: logging.LogRecord) -> None:
        """ Redirect log records to the custom logger. """

        message = self.format(record)
        log_func = self.log_levels.get(record.levelno, self.logger.log)
        log_func(title = record.name, message = message, report = False)


def setup_logger() -> None:
    """ Set up the handler to redirect Discord logs to the custom logger. """

    logs_handler = LogsHandler()
    formatter = logging.Formatter('%(message)s')
    logs_handler.setFormatter(formatter)

    discord_logger = logging.getLogger('discord')

    for handler in discord_logger.handlers:
        discord_logger.removeHandler(handler)

    discord_logger.addHandler(logs_handler)
    discord_logger.setLevel(logging.DEBUG)


__all__ = ['Logger', 'setup_logger']
