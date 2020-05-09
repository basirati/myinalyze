import pymongo

class DBInterface(object):

    URI = 'mongodb://127.0.0.1:27017'
    DATABASE = None

    # Initialize the connection to the database
    @staticmethod
    def initialize(db):
        client = pymongo.MongoClient(DBInterface.URI)
        DBInterface.DATABASE = client[db]

    #get collections
    @staticmethod
    def get_colletions():
        return DBInterface.DATABASE.list_collection_names()

    # Creating a method for insertion in DB; you can use this method to create a collection as well
    @staticmethod
    def insert(collection, data):
        DBInterface.DATABASE[collection].insert(data)

    # Creating a method for querying a collection of the DB, if you do not specify query, it will return everything
    @staticmethod
    def getlist_docs(collection, query=None):
       allDocs = []
       for doc in DBInterface.DATABASE[collection].find(query):
           allDocs.append(doc)
       return allDocs

    #retruns a cursor object which needs to be iterated to show results
    @staticmethod
    def find(collection, query=None):
        return DBInterface.DATABASE[collection].find(query)

    # Creating a method for querying a collection of the DB
    @staticmethod
    def find_one(collection, query=None):
        return DBInterface.DATABASE[collection].find_one(query)

    #inserting one document
    @staticmethod
    def insert_one(collection, doc):
        DBInterface.DATABASE[collection].insert_one(doc)

    #inserting bulk(list of documents)--specify the collection and pass on a list of docs
    @staticmethod
    def insert_many(collection, list_doc):
        DBInterface.DATABASE[collection].insert_many(list_doc)


    #updating an existing document
    @staticmethod
    def update_one(collection, query, newValue):
        DBInterface.DATABASE[collection].update_one(query, {'$set': newValue})

    #update many records, updates field of all documents
    @staticmethod
    def remove_field(collection, query, remove):
        DBInterface.DATABASE[collection].update(query, {'$unset': remove})

    #delete documents
    @staticmethod
    def delete_one(collection, query):
        DBInterface.DATABASE[collection].delete_one(query)

    #delete all docs in a collection
    @staticmethod
    def delete_all(collection, query={}):
        DBInterface.DATABASE[collection].delete_many(query)




