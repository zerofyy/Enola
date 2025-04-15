# Project Plan
```
❌ | main.py
❌ | requirements.txt
✅ | .gitignore
❌ | todo.md
❌ | README.md
⬛ |
❌ | extensions/
❌ |-| utility/
❌ |-| voice/
❌ |-| fun/
❌ |-| moderation/
❌ |-| management/
❌ |-| bot/
❌ |-| testing/
❌ |-| events/
❌ |-| other/
⬛ |
❌ | templates/
❌ |-| discord_command.py
❌ |-| discord_event.py
❌ |-| scheduled_event.py
⬛ |
❌ | utils/
❌ | __init__.py
⬛ |
✅ |-| assets/
✅ |-|-| __init__.py
✅ |-|-| secrets.py
✅ |-|-| emojis.py
✅ |-|-| storage.py
✅ |-|-| coloring.py
⬛ |-|
✅ |-| core/
✅ |-|-| __init__.py
✅ |-|-| bot.py
✅ |-|-| database.py
✅ |-|-| installer.py
⬛ |-|
❌ |-| extension_manager/
❌ |-|-| __init__.py
❌ |-|-| extension.py
❌ |-|-| extension_manager.py
❌ |-|-| cooldown_manager.py
❌ |-|-| permission_manager.py
❌ |-|-| restriction_checks.py
❌ |-|-| extensions.toml
⬛ |-|
❌ |-| exception_manager/
❌ |-|-| __init__.py
❌ |-|-| exception_manager.py
⬛ |-|
❌ |-| functions/
❌ |-|-| miscellaneous.py
⬛ |-|
❌ |-| helpers/
❌ |-|-| __init__.py
❌ |-|-| ...
⬛ |-|
❌ |-| logging/
❌ |-|-| __init__.py
❌ |-|-| logger.py
⬛ |
❌ | logs/ 
```

# DataBase Structure
```
📦 devices
⬛ | mac_address: str
⬛ | host: str
```

# TODO (by priority)
```
✅ | utils/core/*
✅ | utils/assets/*
✅ | utils/functions/*
✅ | utils/logging/logger.py
✅ |-| Update logging in installer.py
❌ | Make a new emoji (Emoji.error_crit) for critical error logs.
❌ | Implement a config.
⬛ |-| Replace secrets.py with a config file.
⬛ |-| Commandline arguments can be set to default values in the config, including:
⬛ |-| * whether to report logs to Discord.
⬛ |-| * --not_home, --timezone, and other such arguments.
⬛ |-| * tokens and keys.
⬛ |-| * Bot.setup() arguments.
❌ | utils/extension_manager/*
❌ | utils/exception_manager/*
❌ | main.py
```

# Notes & Ideas
- Removed utils/assets/storage.Channels.anon_questions. It should be converted into a local feature for all servers.
- Keep MAC addresses of different devices in the database to automatically check whether the bot is started from a home device or a server.

# Latest Changes
Finished the logging module and updated miscellaneous functions.

- Finished the `utils.logging` module:
  - Added a custom Logger class for logging.
  - Added a LogsHandler class for redirecting logs from discord.py to the custom logger.
  - Added more colors to the `utils.assets.coloring` module for logging purposes.
  - Updated logs in `utils.core.installer`.
- Reorganized imports in miscellaneous functions.
- Added a `timezone` argument to Bot.setup() for setting a default timezone.
- Updated time-related miscellaneous functions:
  - Added options to return datetime objects.
  - Added options to use the default timezone.
- Fixed the init file for the `utils.functions` module.
- Updated TODO list.