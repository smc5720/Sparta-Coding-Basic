from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta

score = db.movies.find_one({'title':'매트릭스'})['score']
same_score = list(db.movies.find({'score':score},{'_id':False, 'rank':False, 'score':False}))

for i in same_score:
    print(i['title'])

db.movies.update_one({'title':'매트릭스'},{'$set':{'score':0}})