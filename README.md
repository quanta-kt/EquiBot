# EquiBot
EquiBot is a general purpose and activity management Discord bot written using discord.py.

## This repo is Archived
This repo will no longer be maintaied/developed. I created this bot to learn and get started with discord.py and I'm more or less done with that sole objective. :)

## Features

- Command to change the bot prefix,
- Kick and ban commands for moderators.
- Birthday greetings! Also draws a nice looking calendar in the specified channel.

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
