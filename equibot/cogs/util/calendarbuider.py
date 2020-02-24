import calendar
from discord import Embed

class CalendarEmbedBuilder:
    """
    Class for constructing calendar page embeds.
    """

    def __init__(self, month):
        self.month = month
        
        self.name = calendar.month_name[month]
        self.monthrange = calendar.monthrange(0, month)[1]
        self.birthdays = dict(
            map(
                lambda n: (n, list()),
                range(1, self.monthrange + 1)
            )
        )

    def add(self, person, day):
        """
        Add a person's birthday to this month.
        """
        self.birthdays[day].append(person)

    def build(self):
        """
        Builds and returns the message embed.
        """

        body = ''

        for day in range(1, self.monthrange + 1):
            body += f"[ {day} ] {' '.join(self.birthdays[day])}\n"

        return Embed(
            title=('\\~' * 8) + self.name + ('\\~' * 8),
            description=body
        )
