
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

Please make sure you write tests in `tests.py` whenever necessary.

## Usage and setup

### Clone
Get the copy of this repo with Git:
```
git clone https://github.com/abhijeet-nkt/EqviBot
```

### Install
Run the `setup.py` file to install the bot right away!
```
python setup.py install
```

### Setup bot tokens
Before you can test/deploy the bot, you need to create a file named 'secrets.json' with the following content:

```
{
    "debug_token": "Insert your token of the bot being used for testing",
    "production_token": "Insert your token of the bot being used for production"
}
```
`debug_token` will only be used if you pass the command line argument `--debug`.

### Run
Make sure you're in the directory where the `secrets.json` is stored.
Now run the bot using:
```
python -m EquiBot
```

In order to use the debug bot token instead, use:
```
python -m EquiBot --debug
```

## Contact
Discord: Quanta#4037
