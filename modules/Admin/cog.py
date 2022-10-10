from typing import Optional
from nextcord.ext import commands
from nextcord import Embed, Member
import nextcord
import datetime
import humanfriendly


class Admin(commands.Cog, name="Admin"):
    """Collection of admin commands"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    async def kick(self, ctx: commands.Context, member: Member):
        """Kick the mentioned users

        Exemple :
        $kick Baptiste"""
        if member == self.bot.user:
            await ctx.send("You can't kick me out !")
        elif member == ctx.author:
            await ctx.send("You really tried to kick yoursef out..?")
        else:
            await ctx.send(f"{member.name} was kicked out by {ctx.author.nick or ctx.author.name}")
            ctx.guild.kick(member)
        await ctx.message.delete()

    @commands.command()
    async def mute(self, ctx: commands.Context, member: Member, f_time: str, reason: Optional[str] = None):
        """Mute a member for a certain amount of time

        `$mute <Baptiste> <60m> ["for this reason"]` 
        valid time string are _s, _m, _h, _d, _w, _m, _y
        where _ is an int"""

        time = humanfriendly.parse_timespan(f_time)
        # member.timeout(timeout=nextcord.utils.utcnow() +
        #                datetime.timedelta(seconds=time), reason=reason)
        await member.edit(timeout=nextcord.utils.utcnow()+datetime.timedelta(seconds=time))
        msg = f"{member} has been muted for {f_time}"
        if reason:
            msg += f"\nReason : {reason}"
        await ctx.send(msg)

    @commands.command()
    async def unmute(self, ctx: commands.Context, member: Member):
        """Unmute a member

        Example :
        ``$unmute member"""
        await member.edit(timeout=None)
        await ctx.send(f"{member} has been unmuted")


def setup(bot: commands.Bot):
    bot.add_cog(Admin(bot))
