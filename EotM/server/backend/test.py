from dbInterface import DBInterface
from bson.objectid import ObjectId
from trends import TrendSpider

# DBInterface.initialize('test')
#
# print(DBInterface.URI)
# print(DBInterface.DATABASE)
# DBInterface.delete_all('testing')
# #print(Database.find('testing'))
# print(DBInterface.getlist_docs('testing'))
#
# #print(Database.update_one('testing', {'x':2}, {'x': 14}))

trendy = TrendSpider()


