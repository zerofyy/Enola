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
❌ |-| assets/
❌ |-|-| __init__.py
❌ |-|-| secrets.py
❌ |-|-| installer.py
❌ |-|-| emojis.py
❌ |-|-| storage.py    (Servers & Channels)
❌ |-|-| coloring.py
⬛ |-|
✅ |-| core/
✅ |-|-| __init__.py
✅ |-|-| bot.py
✅ |-|-| database.py
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

# TODO (by priority)
```
✅ | utils/core/*
❌ | utils/assets/*
❌ | utils/functions/*
❌ | utils/logging/logger.py
❌ | utils/extension_manager/*
❌ | utils/exception_manager/*
❌ | main.py
```


# Notes & Ideas
- Instead of `get_location()`, add `--not_home` as a command line argument in main.py (`get_prefix()` can stay).
- ...