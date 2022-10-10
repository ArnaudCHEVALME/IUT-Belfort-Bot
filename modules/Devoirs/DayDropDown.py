import nextcord


class DayDrop(nextcord.ui.Select):
    def __init__(self):
        days = (
            nextcord.SelectOption(label="Lundi"),
            nextcord.SelectOption(label="Mardi"),
            nextcord.SelectOption(label="Mercredi"),
            nextcord.SelectOption(label="Jeudi"),
            nextcord.SelectOption(label="Vendredi"),
            nextcord.SelectOption(label="Samedi"),
            nextcord.SelectOption(label="Dimanche"),
        )
        super().__init__(
            placeholder="Choisir le jour de la semaine",
            min_values=1,
            max_values=1,
            options=days,
        )
