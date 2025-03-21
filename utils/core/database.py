from pymongo.mongo_client import MongoClient
from pymongo.collection import InsertOneResult, InsertManyResult, DeleteResult, UpdateResult, Database


class DB:
    """ Singleton class representing the database. """

    _instance = None
    client: MongoClient = None
    database: Database = None


    def __new__(cls) -> 'DB':
        """ Create a new instance of the DB class if it doesn't already exist. """

        if cls._instance is None:
            cls._instance = super(DB, cls).__new__(cls)

        return cls._instance


    def setup(self, db_url: str) -> None:
        """
        Set up the database.

        Arguments:
             db_url: A MongoDB connection url.
        """

        self.client = MongoClient(db_url)
        self.database = self.client['database']


    def find(self, collection: str, query: dict[str, ...], find_many: bool = False) \
            -> tuple[dict[str, ...], ...] | dict[str, ...] | None:
        """
        Find documents in a database collection.

        Arguments:
             collection: Name of the database collection.
             query: The search query.
             find_many: Whether to find all documents that satisfy the query or stop at the first one.

        Returns:
            The document(s) or None if not found.
        """

        if find_many:
            return tuple(self.database[collection].find(query))

        return self.database[collection].find_one(query)


    def insert(self, collection: str, data: dict[str, ...] | list[dict[str, ...]]) \
            -> InsertOneResult | InsertManyResult:
        """
        Insert documents to a database collection.

        Arguments:
            collection: Name of the database collection.
            data: The document(s) to insert.

        Returns:
            The result of inserting documents.
        """

        if isinstance(data, list):
            return self.database[collection].insert_many(data)

        return self.database[collection].insert_one(data)


    def delete(self, collection: str, query: dict[str, ...], delete_many: bool = False) -> DeleteResult:
        """
        Delete documents from a database collection.

        Arguments:
             collection: Name of the database collection.
             query: The search query.
             delete_many: Whether to delete all documents that satisfy the query or just the first one.

        Returns:
            The result of deleting documents.
        """

        if delete_many:
            return self.database[collection].delete_many(query)

        return self.database[collection].delete_one(query)


    def update(self, collection: str, query: dict[str, ...], updates: dict[str, dict[str, ...]],
               update_many: bool = False, upsert: bool = False) -> UpdateResult:
        """
        Update documents in a database collection.

        Update modifications: https://www.mongodb.com/docs/upcoming/reference/mql/update/#std-label-update-operators

        Arguments:
            collection: Name of the database collection.
            query: The search query.
            updates: Update modifications to apply onto the documents.
            update_many: Whether to update all documents that satisfy the query or just the first one.
            upsert: Whether to insert a new document if the search fails.

        Returns:
            The result of updating documents.
        """

        if update_many:
            return self.database[collection].update_many(query, updates, upsert = upsert)

        return self.database[collection].update_one(query, updates, upsert = upsert)


__all__ = ['DB']
