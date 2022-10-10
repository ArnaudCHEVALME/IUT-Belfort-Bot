from nextcord import RawReactionActionEvent
from nextcord.errors import Forbidden
from nextcord.ext import commands


class Poll(commands.Cog, name="Poll"):
    """Generate polls"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

        self.poll_reactions = {
            0: "0️⃣",
            1: "1️⃣",
            2: "2️⃣",
            3: "3️⃣",
            4: "4️⃣",
            5: "5️⃣",
            6: "6️⃣",
            7: "7️⃣",
            8: "8️⃣",
            9: "9️⃣",
            10: "🔟",
            "Y": "✅",
            "N": "❌"
        }

    @commands.command()
    async def poll(self, ctx: commands.Context, question: str = None, *options: str):
        """Creates a poll

        `$poll "Question here"` to create a Y/N poll

        `$poll "Question here" "First Option" "Second Option" "Third Option"`
        min = 2 | max = 11
        """

        try:
            await ctx.message.delete(delay=5)
        except Forbidden:
            pass

        if not question or len(options) == 1:
            await ctx.send("Invalid poll. Use `$help poll`to see how to use it", delete_after=5)
        else:
            poll_body = question+"\n\n"

            if not options:
                poll_body += f"{self.poll_reactions['Y']} : Oui\t"
                poll_body += f"{self.poll_reactions['N']} : Non"
                msg = await ctx.send(poll_body)
                await msg.add_reaction(self.poll_reactions["Y"])
                await msg.add_reaction(self.poll_reactions["N"])

            else:
                if len(options) > 11:
                    options = options[0:11]

                poll_body += "\n".join(
                    f"{self.poll_reactions[i]} : {options[i]}" for i in range(len(options)))

                msg = await ctx.send(poll_body)

                for i in range(len(options)):
                    await msg.add_reaction(self.poll_reactions[i])
            self.bot.bdd_interface.add_poll(msg.id, msg.guild.id)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        user = payload.member

        if user == self.bot.user:
            return

        guild_discord_id = payload.guild_id
        msg_id = payload.message_id

        channel = await self.bot.fetch_channel(payload.channel_id)
        msg = await channel.fetch_message(payload.message_id)

        emoji = payload.emoji.name
        if emoji not in self.poll_reactions.values():
            await msg.remove_reaction(emoji, user)
            return

        polls = self.bot.bdd_interface.get_polls()
        is_a_poll = False
        for poll in polls:
            if poll["message_id"] == str(msg_id) and poll["guild_discord_id"] == str(guild_discord_id):
                is_a_poll = True
                break
        if is_a_poll:
            for react in msg.reactions:
                if react.emoji != emoji:
                    await msg.remove_reaction(react.emoji, user)


def setup(bot: commands.Bot):
    bot.add_cog(Poll(bot))
