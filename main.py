from dotenv import load_dotenv
load_dotenv(override=True)

from Broker.IG import session
from Data.Price import Price
import os


def main():

  price = Price()
  price.connect_to_db(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST', 'localhost'),
        port=os.getenv('DB_PORT', '5432')
    )
  
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

if __name__ == "__main__":
    main()