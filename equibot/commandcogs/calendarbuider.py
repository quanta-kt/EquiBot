import calendar

class CalendarBuilder:
    """
    Class for constructing calendar messages.
    """

    def __init__(self, month):
        self.month = month
        
        self.name = calendar.month_name[month]
        self.monthrange = calendar.monthrange(0, month)[1]
        self.birthdays = dict(
            map(
                lambda n: (n, []),
                range(1, self.monthrange + 1)
            )
        )

    def add(self, person, day):
        """
        Add a person's birthday to this month.
        """
        self.birthdays[day].append(person)

    def __str__(self):
        """
        Builds and returns the message text.
        """

        header = f'**{self.name}**'.rjust(20) + '\n'
        header += '♡∞:｡.｡　　｡.｡:∞♡'.rjust(20) + '\n\n'

        body = ''

        for day in range(1, self.monthrange + 1):

            day_str = str(day).ljust(2)

            if len(self.birthdays[day]) == 0:
                body += f'{day_str} 『 '.ljust(30) + ' 』\n'
                continue
            
            chunk = ' '.join(self.birthdays[day])
            body += f'{day_str} 『 {chunk}'.ljust(30) + ' 』\n'

        footer = '♡∞:｡.｡　　｡.｡:∞♡'.rjust(20)

        return header + body + footer