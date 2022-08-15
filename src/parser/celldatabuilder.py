class CellData:
    """Class to collect cell data in the calendar table."""

    def __init__(self):
        self.date = None
        self.tithi = ''
        self.t0 = False
        self.second_tithi = ''
        self.st = False
        self.nakshatra = ''
        self.nk = False
        self.rahuk = ''
        self.r0 = False
        self.yamag = ''
        self.y0 = False
        self.varjya = ''
        self.v0 = False
        self.durmuhurta = ''
        self.d0 = False

    def __str__(self):
        return "Date: " + self.date + "\n" + \
              "- Tithi: " + self.tithi + "\n" + \
              "- Second Tithi: " + self.second_tithi + "\n" + \
              "- Nakshatra: " + self.nakshatra + "\n" + \
              "- Rahu Kalam: " + self.rahuk + "\n" + \
              "- Yamagandham: " + self.yamag + "\n" + \
              "- Varjya: " + self.varjya + "\n" + \
              "- Durmuhurta: " + self.durmuhurta + "\n"

    def date(self) -> int:
        return self.date

    def tithi(self) -> str:
        return self.tithi

    def second_tithi(self) -> str:
        return self.second_tithi

    def nakshatra(self) -> str:
        return self.nakshatra

    def rahu(self) -> str:
        return self.rahuk

    def yama(self) -> str:
        return self.yamag

    def varjya(self) -> str:
        return self.varjya

    def durmuhurta(self) -> str:
        return self.durmuhurta


class CellDataBuilder:

    def __init__(self):
        self._cell_data = CellData()

    def with_date(self, date):
        self._cell_data.date = date
        return self

    def with_tithi(self, tithi):
        self._cell_data.tithi = tithi
        return self

    def with_second_tithi(self, second_tithi):
        self._cell_data.second_tithi = second_tithi
        return self

    def with_nakshatra(self, nakshatra):
        self._cell_data.nakshatra = nakshatra
        return self

    def with_rahu(self, rahu):
        self._cell_data.rahu = rahu
        return self

    def with_yama(self, yama):
        self._cell_data.yama = yama
        return self

    def with_varjya(self, varjya):
        self._cell_data.varjya = varjya
        return self

    def with_durmuhutra(self, durmuhurta):
        self._cell_data.durmuhurta = durmuhurta
        return self

    def build(self) -> CellData:
        return self._cell_data
