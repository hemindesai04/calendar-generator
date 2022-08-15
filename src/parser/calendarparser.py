import datetime
import os
import string

from src.util import edays
from src.parser.calendarmonthdata import CalendarMonthData
from src.parser import celldatabuilder as cdb
from src.parser.celldatabuilder import CellData
from src.util import emonths as emonths
import re

MAX_LINE_WIDTH = 22
MAX_SHORT_LINE_WIDTH = 12


def parse_month_date(month: emonths, line, cell: CellData) -> bool:
    """
    Method to parse a date of a month from the given string data and populate the given cell (CellData data structure)
    with its value.
    :param month: Month
    :param line: String data that contains date and data specific to that date of the given month
    :param cell: cell data structure to be populated with date
    :return: true, if the date is parsed appropriately, otherwise false
    """
    values = line.split(',')
    if values[0] is not None:
        vals = values[0].split(' ')
        if vals[0] == month.name:
            cell.date = vals[1].strip('\n\t')
            debug_print("Date: " + month.name + " " + cell.date)
            return True
        else:
            return False


def parse_tithi(line, cell: CellData):
    """
    Method to parse Tithis from the given string data of a particular date and populate the cell with it.
    :param line: String data of a particular date
    :param cell: cell data structure to be populated with the Tithis
    :return: None
    """
    values = line.strip().split(',')
    cell.tithi = values[1].strip().replace('till ', '')
    cell.tithi = strip_long_words(cell.tithi)
    debug_print("- Tithi: " + cell.tithi)
    if len(cell.tithi) < MAX_LINE_WIDTH:
        cell.t0 = True
    if len(values) > 3:
        # swap the tithis to display if there are more than two on a day
        cell.second_tithi = cell.tithi
        if len(cell.second_tithi) < MAX_SHORT_LINE_WIDTH:
            cell.st = True
        cell.tithi = values[2].strip().replace('till ', '')
        cell.tithi = strip_long_words(cell.tithi)
        debug_print("- Second Tithi: " + cell.tithi)
        if len(cell.tithi) < MAX_LINE_WIDTH:
            cell.t0 = True


def parse_nakshatra(line, cell: CellData):
    """
    Method to parse Nakshatras from the given string data of a particular date and populate the given cell with it.
    :param line: String data of a particular date of the month
    :param cell: cell data structure to be populated with the Nakshatras
    :return: None
    """
    values = line.split(',')
    for value in values:
        value = value.strip()
        if "yoga" not in value and len(value) > 0:
            nakshatra = value.strip().replace('till ', '')
            nakshatra = strip_long_words(nakshatra)
            if len(cell.nakshatra) > 0:
                cell.nakshatra = cell.nakshatra + ',' + '\n' + ' '
            cell.nakshatra = cell.nakshatra + nakshatra
            debug_print("- Nakshatra: " + cell.nakshatra)
    # if len(cell.nakshatra) < MAX_LINE_WIDTH:
        cell.nk = True


def parse_rahu_and_yama(line, cell: CellData):
    """
    Parse Rahu Kalam and Yamagandham of a particular date from the given string data and populate the cell with it.
    :param line: String data of a particular date of the month
    :param cell: cell data structure to be populated with Rahu Kalam and Yamagandham
    :return: None
    """
    values = line.split(',')
    cell.rahuk = values[0].strip().replace('ahuK', '')
    debug_print("- Rahu Kalam: " + cell.rahuk)
    if len(cell.rahuk) < MAX_LINE_WIDTH:
        cell.r0 = True
    if len(values) > 2:
        cell.yamag = values[2].strip().replace('amaG', '')
        debug_print("- Yamagandham : " + cell.yamag)
        if len(cell.yamag) < MAX_LINE_WIDTH:
            cell.y0 = True


def parse_varjya_and_durmuhurta(line, cell: CellData):
    """
    Parse Varjya and Durmuhurta of a particular date from the given string data and populate the cell with it.
    :param line: String data of a particular date of the month
    :param cell: cell data structure to be populated with Varjya and Durmuhurta data
    :return: None
    """
    values = re.findall(r"Varjya: ([^a-z]*),[\s|A-Z]*", line.strip())
    if len(values) > 0:
        cell.varjya = "V: " + str(values[0])
        debug_print("- Varjya: " + cell.varjya)
        if len(cell.varjya) < MAX_LINE_WIDTH:
            cell.v0 = True
    values = re.findall(r"Durmuhurta: (.*),\s?[a-zA-Z]?", line.strip())
    if len(values) > 0:
        cell.durmuhurta = "D: " + str(values[0])
        debug_print("- Durmuhurta: " + cell.durmuhurta)
        if len(cell.durmuhurta) < MAX_LINE_WIDTH:
            cell.d0 = True


def configure_start_date(table_row, cell_counter, month: emonths):
    """
    Utility method to determine the table row and cell number of the start date of a month.
    :param table_row: table row in the matrix of a month
    :param cell_counter: cell number in the matrix of a month
    :param month: month for which the table row and cell number needs to be obtained
    :return: table row and cell number for the start date of the given month
    """

    # get day name
    day_name = datetime.date(2022, int(month.value[3]), 1)
    debug_print(day_name.strftime("%A"))
    day_counter = 0
    for day in edays.Days:
        if day.name == day_name.strftime("%A"):
            break
        day_counter = day_counter + 1

    while day_counter > 0:
        cell_counter = cell_counter + 1
        table_row.append({})
        day_counter = day_counter - 1
    return cell_counter, table_row


def strip_long_words(line) -> str:
    word_split = re.findall(r"([A-Za-z]+)\s([a-zA-Z]+)*\s(.*),*", line)
    if len(word_split) > 0 and len(word_split[0][1]) > 0:
        return word_split[0][0][0].upper() + '.' + word_split[0][1] + ' ' + word_split[0][2].strip(',')
    return line


def debug_print(data: string):
    if os.getenv("DEBUG_CALENDAR", default=None) is not None:
        print(data)


class CalendarParser:

    def __init__(self, file_path):
        self.file_path = file_path

    def parse(self, month: emonths, quote) -> CalendarMonthData:
        return self.parse_and_build_cell(month, quote)

    def parse_and_build_cell(self, month: emonths, quote) -> CalendarMonthData:
        """
        Method to parse data and build the cells that are added to the table row.
        Data Format:
        #1: <Month> <Date>, <Year>:
        #2: <Day>, <Tithi1>, <Tithi2>,
        #3: <Nakshatra>, <Nakshatra2>, <NA>, <NA>,
        #4: <NA>, <NA>,
        #5: <RahuK>, <NA>, <YamaG>,
        #6: <Varjya>, <Durmuhurta>,
        #7: <NA>, <NA>,
        #8: <NA>, <NA>, <NA>,
        :param month: month for which the data needs to be parsed and returned
        :param quote: quote of the month
        :return: parsed data structure for a given month
        """
        month_data = CalendarMonthData(month, quote)
        with open(self.file_path) as file:
            cell = cdb.CellData()
            block_line_counter = 0  # there are 8 lines for a date block in the data format
            cell_counter = 0
            table_row = []
            cell_counter, table_row = configure_start_date(table_row, cell_counter, month)
            valid = True

            # parse the date block
            for line in file:
                if line.strip() and line != "\n":
                    # non-empty lines
                    block_line_counter = block_line_counter + 1
                    if block_line_counter == 1:
                        valid = parse_month_date(month, line, cell)
                        if not valid:
                            pass
                    elif block_line_counter == 2:
                        if valid:
                            parse_tithi(line, cell)
                    elif block_line_counter == 3:
                        if valid:
                            parse_nakshatra(line, cell)
                    elif block_line_counter == 5:
                        if valid:
                            parse_rahu_and_yama(line, cell)
                    elif block_line_counter == 6:
                        if valid:
                            parse_varjya_and_durmuhurta(line, cell)
                    elif block_line_counter == 8:
                        block_line_counter = 0
                        cell_counter = cell_counter + 1
                        if valid:
                            debug_print(cell)
                            table_row.append(vars(cell))
                        else:
                            table_row.append({})
                        # initialize a new cell
                        cell = cdb.CellData()
                        # append the table row once we have cells for all seven days
                        if cell_counter % 7 == 0:
                            month_data.table_rows.append({'cols': table_row})
                            table_row = []
                    else:
                        pass

            if cell_counter < 35:
                while cell_counter < 35:
                    # append empty list for the empty cells to the last table row to render them
                    table_row.append({})
                    cell_counter = cell_counter + 1
                if len(table_row) > 0:
                    # append the last non-empty and incomplete table row
                    month_data.table_rows.append({'cols': table_row})
            elif cell_counter > 35:
                # wrap around and start filling first row as the dates have crossed the table size
                i = 0
                while cell_counter != 35:
                    month_data.table_rows[0]['cols'][i] = table_row[i]
                    cell_counter = cell_counter - 1
                    i = i + 1

        return month_data
