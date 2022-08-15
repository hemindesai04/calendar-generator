import src.util.emonths as emonths


class CalendarMonthData:
    """
    Class to store data specific to a month.
    """

    def __init__(self, month: emonths, quote):
        self.month = month
        self.quote = quote      # "Saburi (patience) ferries you across to the distant goal."
        self.table_rows = []    # list of table row dictionary objects
        self.data_dict = {
            'month': month.name,
            'quote': self.quote,
            'tbl_contents': self.table_rows
        }

    def append_table_row(self, table_row):
        # reason it needs to be saved with 'cols' as the key is because the template can understand and populate the
        # doc based on the dictionary value.
        self.table_rows.append({'cols': table_row})

