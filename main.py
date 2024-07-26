from dotenv import load_dotenv
load_dotenv(override=True)

from Broker.IG import session
from Data.Price import price

def main():
  while True:
    try:
      session.authenticate()
      session.get_stream()
      for rawdata in session.stream:
        price.collect(rawdata)
        price.inform(rawdata)
      price.cutoff()
      price.save()

    except Exception as e:
      price.cutoff()
      price.save()

main()