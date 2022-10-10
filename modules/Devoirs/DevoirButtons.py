import nextcord


class ValiderBtn(nextcord.ui.Button):
    def __init__(self, style=nextcord.ButtonStyle.green, label="Valider"):
        super().__init__(style=style, label=label)

    async def callback(self, interaction: nextcord.Interaction):
        await self.view.submit()


class CancelBtn(nextcord.ui.Button):
    def __init__(self, style=nextcord.ButtonStyle.red, label="Annuler"):
        super().__init__(style=style, label=label)

    async def callback(self, interaction: nextcord.Interaction):
        await self.view.ctx.message.delete()
        await self.view.ans.delete()
        self.view.canceled = True
        self.view.stop()
