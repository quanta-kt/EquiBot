import asyncio

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
        Each action funtion retuns True if the action was taken.
        No further processing is done if that is true.
        The action functions can be coroutines.
        """

        for action in self.actions:
            #For now all the actions are coroutines however
            if asyncio.iscoroutinefunction(action):
                if await action(message): return True
            else:
                if action(message): return True

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
            return True

        #The `else` is just a redability concern
        else: return False

    async def backFromAFK(self, message):
        """
        Welcomes the user if he had previously set an AFK
        status using `bye` command - clearing the AFK status.
        """

        if (await self.repo.get_afk_status(message.guild.id, message.author.id)) != None:
            await self.repo.clear_afk_status(message.guild.id, message.author.id)
            msg = await message.channel.send(
                f"**Welcome back {message.author.display_name}!**\n" +
                "I've removed your AFK status"
            )

            await msg.delete(delay=5)
            return True

        else: return False

    async def afkMention(self, message):
        """
        Informs the the sender that the mentioned user is AFK if any
        """

        for user in message.mentions:
            afk_status = await self.repo.get_afk_status(message.guild.id, user.id)
            if afk_status == None:
                continue

            await message.channel.send(
                f"Nice, but {user.display_name} is AFK.\n" +
                f"**Reason:** {afk_status}"
            )

        return False #Always returns False so that kick/ban commands continue to work