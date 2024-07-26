import psycopg2
from datetime import datetime
from util import tprint

class Price:
    def __init__(self):
        # Initialize empty lists and variables
        self._data = []  # Stores collected price data
        self.informed = []  # Keeps track of informed tables
        self.informed_hour = 0  # Tracks the current hour for informing
        self.conn = None  # Database connection object
        self.cur = None  # Database cursor object

    def connect_to_db(self, dbname, user, password, host="localhost", port="5432"):
        """Establish a connection to the PostgreSQL database"""
        try:
            # Attempt to connect to the database
            self.conn = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port
            )
            self.cur = self.conn.cursor()
            self.create_table()  # Ensure the required table exists
        except (Exception, psycopg2.Error) as error:
            tprint(f"Error while connecting to PostgreSQL: {error}")

    def create_table(self):
        """Create the price_data table if it doesn't exist"""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS price_data (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP,
            table_id INTEGER,
            bid FLOAT,
            offer FLOAT,
            spread FLOAT
        )
        """
        self.cur.execute(create_table_query)
        self.conn.commit()

    def collect(self, rawdata):
        """Collect and parse raw data"""
        if "|" in rawdata:
            parsedData = self.__parse(rawdata)
            self._data.append(parsedData)

    def __parse(self, rawdata):
        """Parse raw data into a tuple"""
        now = datetime.now()
        table, bid, ofr = rawdata.split("|")
        table = int(table[0])
        bid = float(bid)
        ofr = float(ofr)
        spread = round(ofr - bid, 2)
        return (str(now), table, bid, ofr, spread)

    def inform(self, rawdata):
        """Print raw data to console once per hour"""
        if "|" in rawdata:
            table, bid, ofr = rawdata.split("|")

            # Reset informed criteria at the start of each hour
            now = datetime.now()
            if now.hour != self.informed_hour:
                self.informed_hour = now.hour
                self.informed = []

            # Print raw data to console if not already informed this hour
            if table not in self.informed:
                self.informed.append(table)
                tprint(rawdata)

    def save(self):
        """Save collected data to the database"""
        if not self.conn or not self.cur:
            tprint("Database connection not established. Call connect_to_db() first.")
            return

        insert_query = """
        INSERT INTO price_data (timestamp, table_id, bid, offer, spread)
        VALUES (%s, %s, %s, %s, %s)
        """
        try:
            # Insert all collected data into the database
            self.cur.executemany(insert_query, self._data)
            self.conn.commit()
            tprint(f"Saved {len(self._data)} rows to database.")
            self._data = []  # Clear the data after saving
        except (Exception, psycopg2.Error) as error:
            tprint(f"Error while saving data to PostgreSQL: {error}")

    def cutoff(self):
        """Add an empty row to indicate a cutoff period"""
        if not self.conn or not self.cur:
            tprint("Database connection not established. Call connect_to_db() first.")
            return

        cutoff_query = """
        INSERT INTO price_data (timestamp, table_id, bid, offer, spread)
        VALUES (%s, %s, %s, %s, %s)
        """
        try:
            now = datetime.now()
            # Insert a row with NULL values except for timestamp
            self.cur.execute(cutoff_query, (now, None, None, None, None))
            self.conn.commit()
            tprint("Added empty row to indicate a cut off period from the stream.")
        except (Exception, psycopg2.Error) as error:
            tprint(f"Error while adding cutoff to PostgreSQL: {error}")

    def close_connection(self):
        """Close the database connection"""
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
        tprint("Database connection closed.")