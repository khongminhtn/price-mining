from datetime import datetime
from util import tprint



class Price:
  def __init__(self):
    self._data = []
    self.informed = []
    self.informed_hour = 0



  def collect(self, rawdata):
    if "|" in rawdata:
      parsedData = self.__parse(rawdata)
      self._data.append(parsedData)



  def __parse(self, rawdata):
    now = datetime.now()
    table, bid, ofr = rawdata.split("|")
    table = int(table[0])
    bid = float(bid)
    ofr = float(ofr)
    spread = round(ofr - bid, 2)
    return (str(now), table, bid, ofr, spread)



  def inform(self, rawdata):
    if "|" in rawdata:
      table, bid, ofr = rawdata.split("|")

      # reset informed criteria
      now = datetime.now()
      if now.hour is not self.informed_hour:
        self.informed_hour = now.hour
        self.informed = []

      # print raw data to console every hour
      if table not in self.informed:
        self.informed.append(table)
        tprint(rawdata)



  def save():
    tprint("Saved data to database.")



  def cutoff():
    tprint("Added empty row to indicate a cut off period from the stream.")


price = Price()