import nextcord

from modules.Devoirs.SujetDropDown import SujetDrop
from modules.Devoirs.WeekDropDown import WeeksDrop
from modules.Devoirs.DayDropDown import DayDrop
from modules.Devoirs.DevoirButtons import CancelBtn, ValiderBtn


class AddDevoirView(nextcord.ui.View):
    def __init__(self, subjects: list):
        super().__init__(timeout=180)
        self.canceled = False
        self.subject = SujetDrop(subjects)
        self.week = WeeksDrop()
        self.day = DayDrop()
        self.add_item(self.subject)
        self.add_item(self.day)
        self.add_item(self.week)
        self.add_item(ValiderBtn())
        self.add_item(CancelBtn())

    async def submit(self):
        if len(self.subject.values) == 0:
            await self.ctx.send("Il faut choisir une matière !")
        elif not self.canceled:
            self.stop()
