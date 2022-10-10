from datetime import timedelta, datetime
import nextcord


class WeeksDrop(nextcord.ui.Select):
    def __init__(self):
        weeks = []
        start = datetime.now()
        while start.weekday() != 0:
            start -= timedelta(days=1)
        for i in range(13):
            end = start + timedelta(days=6)
            desc = f"{start.strftime('%d/%m/%y')} - {end.strftime('%d/%m/%y')}"
            weeks.append(nextcord.SelectOption(
                label=f"S+{i}", description=desc))
            start = end + timedelta(days=1)

        super().__init__(
            placeholder="Choisir la semaine",
            min_values=1,
            max_values=1,
            options=weeks,
        )
