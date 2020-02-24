import asyncio
from .cogs.util import simpleEmbed

class MessageActions:
    """
    A class which takes actions bassed on the
    content of non-command messages.
    """

    def __init__(self, bot, repo):
        self.bot = bot
        self.repo = repo

        #Action functions
        self.actions = [
            self.botMention,
            self.backFromAFK,
            self.afkMention
        ]

    async def invoke(self, message):
        """
        Called when a message arrives.
        Each function in list `action` is called with the message
        object as the only parameter
        The action functions can be coroutines.
        """

        for action in self.actions:
            #For now all the actions are coroutines however
            if asyncio.iscoroutinefunction(action):
                await action(message)
            else:
                action(message)

    async def botMention(self, message):
        """
        Informs the prefix if bot is mentioned
        """
        if self.bot.user.mentioned_in(message) and not message.mention_everyone:
            #We have got a mention!
            prefix = self.repo.get_prefix(message.guild.id)
            await message.add_reaction('👀')
            await message.channel.send(
                f"My prefix here is: **{prefix}**\n" +
                f"Try **{prefix}help** to get list of commands!"
            )

    async def backFromAFK(self, message):
        """
        Welcomes the user if he had previously set an AFK
        status using `bye` command - clearing the AFK status.
        """

        if (await self.repo.get_afk_status(message.guild.id, message.author.id)) != None:
            await self.repo.clear_afk_status(message.guild.id, message.author.id)
            msg = await message.channel.send(
                embed = simpleEmbed(
                    f"Welcome back {message.author.display_name}!",
                    "I've removed your AFK status"
                )
            )

            await msg.delete(delay=5)

    async def afkMention(self, message):
        """
        Informs the the sender that the mentioned user is AFK if any
        """

        for user in message.mentions:
            afk_status = await self.repo.get_afk_status(message.guild.id, user.id)
            if afk_status == None:
                continue

            await message.channel.send(
                embed = simpleEmbed(
                    "Oops!",
                    f"**{user.display_name} is not here**\n" +
                    f"**Reason:** {afk_status}"
                )
            )