import random
from nextcord.ext import commands


class Random(commands.Cog, name="Random"):
    """Random commands"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def roll(self, ctx: commands.Context, dice: str):
        """Roll dices in the form \_d\_
        Example: 
        ```
        $roll 3d20```
        """
        try:
            amount, max_value = dice.split("d")
            results = ""
            total = 0
            for i in range(1, int(amount)+1):
                val = random.randint(1, int(max_value))
                total += val
                results += f"Dice {i} : {val}\n"
            await ctx.send(f"=== Results ===\n{results}\nTotal = {total}")
        except ValueError:
            await ctx.send("Dices must be in the format 2d6 (2 dices of 6 faces here")

    @commands.command()
    async def coin(self, ctx: commands.Context):
        """Flip a coin"""
        if random.randint(0, 1):
            msg = "Heads !"
        else:
            msg = "Tails !"
        await ctx.send(msg)

    @commands.command()
    async def choose(self, ctx: commands.Context, *args):
        """Choose one option from the given options

        Example:
        ```
        $choose "First Option" "Second Option "Third Option"
        ```
        """
        await ctx.send(f"Je choisis {random.choice(args)}")


def setup(bot: commands.Bot):
    """Add the cog to the bot"""
    bot.add_cog(Random(bot))
