# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import os

from docxtpl import DocxTemplate
from src.parser.calendarparser import CalendarParser
import src.util.emonths as emonths

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    for month in emonths.Months:
        data_parser = CalendarParser(month.value[2])
        month_data = data_parser.parse(month, month.value[4])
        doc = DocxTemplate("./template/template.docx")
        doc.render(month_data.data_dict)
        OUT_DIR = "./output"
        if not os.path.exists(OUT_DIR):
            os.mkdir(OUT_DIR)
        doc.save("./output/2022_generated_calendar_" + month.name + ".docx")
