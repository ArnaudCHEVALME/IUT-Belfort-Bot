from nextcord.ext import commands
from datetime import datetime, timedelta

from modules.Devoirs.AddDevoirView import AddDevoirView


class Devoirs(commands.Cog, name="Devoirs"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    async def devoirs(self, ctx: commands.Context):
        """Affiche les devoirs pas encore passés"""
        devoirs = self.bot.bdd_interface.get_devoirs(ctx.guild.id)
        msg = ""
        for devoir in devoirs:
            msg += f"En {devoir['subject_name']}, pour le {devoir['devoir_due_time']} :\n{devoir['devoir_name']}\n"
        await ctx.send(msg)

    @commands.command()
    async def devoir(self, ctx: commands.Context, description: str):
        """Add a new work to the agenda

        `$devoir "Rendre le rapport"`"""
        await ctx.message.delete()
        view = AddDevoirView(self.bot.bdd_interface.get_subjects())
        view.ans = await ctx.send(f"Ajout d'un nouveau devoir : *{description}*", view=view)
        exit_state = await view.wait()
        if exit_state == False and view.canceled == False:
            week_range = [
                view.week.options[i].description
                for i in range(len(view.week.options))
                if view.week.options[i].label == view.week.values[0]
            ]
            date = get_date(view.day.values[0], week_range[0])
            devoir = {
                "subject_id": view.subject.values[0],
                "devoir_name": description.replace('"', ""),
                "devoir_due_date": date,
            }
            txt = f"Pour le {devoir['devoir_due_date']}, en {view.subject.subject_ids[int(view.subject.values[0])]} :\n{devoir['devoir_name']}"
            await view.ans.delete()
            await ctx.send(txt, delete_after=5)
            self.bot.bdd_interface.add_devoir(devoir, ctx.guild.id)
        elif exit_state:
            await ctx.send("Durée limite dépassée")


def get_date(day: str, week: str):
    """
    It takes a day of the week and a date in the format "dd/mm/yy" and returns the date of the next
    occurrence of that day of the week

    :param day: the day of the week
    :type day: str
    :param week: "Semaine du lundi 20/01/20 au dimanche 26/01/20"
    :type week: str
    :return: A string in the format "YYYY-MM-DD"
    """
    days = ("Lundi", "Mardi", "Mercredi", "Jeudi",
            "Vendredi", "Samedi", "Dimanche")
    day_id = days.index(day)
    bad_date = week.split("-")[0].strip().split("/")
    date_str = f"20{bad_date[2]}-{bad_date[1]}-{bad_date[0]}"
    date = datetime.strptime(date_str, "%Y-%m-%d")
    while date.weekday() != day_id:
        date += timedelta(days=1)
    return date.strftime("%Y-%m-%d")


def setup(bot: commands.Bot):
    bot.add_cog(Devoirs(bot))
