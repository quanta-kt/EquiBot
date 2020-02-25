
# EquiBot
EquiBot is a general purpose and activity management Discord bot written using discord.py.
This project is currently under massive development and not ready for any production level use.

## Planned features
I have planned to add these features to the bot, you're welcome to edit this file to add more. :)

- [x] Command to change the bot prefix,
- [x] Command to add moderator roles, which have access to some special commands.
- [x] Birthday greetings! Also draws a nice looking calendar in the specified channel.
- [ ] Command to schedule and host 'Question Of The Day' event.

## Contributing
This project is open for any suggestions, PRs and feature requests. :smile:

Please make sure you write any necessary tests in `tests` sub-module.

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
python -m equiBot
```

In order to use the debug bot token instead, use:
```
python -m equiBot --debug
```

### Test
EquiBot uses `pytest` for unit testing. To run these unit tests, you need to install `pytest` and `pytest-asyncio`
```
pip install pytest
pip install pytest-asyncio
```

Now simply run `pytest` from the project's root directory.
```
pytest
```

Optionally, you can run tests by running the `tests` sub-module instead:
```
python -m equibot.tests
```
This allows debuggers to work for pytest cases.

## Contact
Discord: Quanta#4037
