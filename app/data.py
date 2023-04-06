from os import getenv

from certifi import where
from dotenv import load_dotenv
from MonsterLab import Monster
from pandas import DataFrame
from pymongo import MongoClient


class Database:
    """
    A class to connect to a collection in the MongoDB database.

    ...

    Attributes
    ----------
    collection : str, optional
        The name of the collection to connect (default is 'monsters')

    Methods
    -------
    seed(amount):
        Creates specified amount of monster records to insert into collection.

    reset():
        Erase all records in the collection.

    count():
        Return the number of records in the collection.

    dataframe():
        Return a DataFrame containing all records in the collection.

    html_table():
        Return an HTML table containing all records in the collection.
    """

    load_dotenv()
    database = MongoClient(getenv("DB_URL"), tlsCAFile=where())["Database"]

    def __init__(self, collection='monsters'):
        """
        Connects to a collection in the database.

        Parameters
        ----------
            collection : str, optional
                The name of the collection to connect (default is 'monsters')
        """

        self.collection = self.database[collection]

    def seed(self, amount: int):
        """
        Creates specified amount of monster records to insert into collection.

        Parameters
        ----------
            amount : int
                amount of records to create
        """

        if amount == 1:
            record = Monster().to_dict()
            return self.collection.insert_one(record).acknowledged
        if amount > 1:
            records = [Monster().to_dict() for i in range(amount)]
            return self.collection.insert_many(records).acknowledged

    def reset(self):
        """
        Erase all records in the collection.
        """

        return self.collection.delete_many({}).acknowledged

    def count(self) -> int:
        """
        Return the number of records in the collection.
        """

        return self.collection.count_documents({})

    def dataframe(self) -> DataFrame:
        """
        Return a DataFrame containing all records in the collection.
        """

        records = self.collection.find({})
        return DataFrame(data=records)

    def html_table(self) -> str:
        """
        Return an HTML table containing all records in the collection.
        """

        df = self.dataframe()
        return df.to_html()
