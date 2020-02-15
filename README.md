
# EquiBot
EquiBot is a general purpose and activity management Discord bot written using discord.py.
This project is currently under massive development and not ready for any production level use.

## Planned features
I have planned to add these features to the bot, you're welcome to edit this file to add more. :)

- [x] Command to change the bot prefix,
- [x] Command to add moderator roles, which have access to some special commands.
- [ ] Command to schedule and host 'Question Of The Day' event.

## Contributing
This project is open for any suggestions, PRs and feature requests. :smile:

Please make sure you write tests for any feature you add in `tests.py` whenever necessary.

## Usage and setup

### Setup bot tokens
Before you can test/deploy the bot, you need to create a file named 'secrets.json' with the following content:

```
{
    "debug_token": "Insert your token of the bot being used for testing",
    "production_token": "Insert your token of the bot being used for production"
}
```
Token which will be used can be changed by changing the `DEBUG` variable in the `constants.py` file. If set to true, debug token will be used, otherwise the production one will be used.

### Run
Simply run the `main.py` file to start the bot. ;)

### Test
Tests are written in `tests.py`.

## Contact
Discord: Quanta#4037
