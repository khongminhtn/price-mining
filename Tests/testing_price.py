import unittest
from Data.Price import price

class TestPrice(unittest.TestCase):
  def test_collect(self):
    price.collect("1,1|10865.7|10866.3")
    print(price._data)


unittest.main()