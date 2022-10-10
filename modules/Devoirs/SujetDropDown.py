import nextcord


class SujetDrop(nextcord.ui.Select):
    def __init__(self, subjects: list):
        options = []
        ids = {}
        for ele in subjects:
            subject_id = ele["subject_id"]
            subject_name = ele["subject_name"]
            options.append(nextcord.SelectOption(
                label=subject_name, value=str(subject_id), description=subject_name))
            ids[subject_id] = subject_name
        super().__init__(
            placeholder="Choisir la matière",
            min_values=1,
            max_values=1,
            options=options,
        )
        self.subject_ids = ids
