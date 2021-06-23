import pymongo
import time
gyb = pymongo.MongoClient("mongodb://localhost:27017/")

db = gyb["FilmDB"]
col1 = db["Filmdb"]
col2 = db["Comment"]

# name = "碟中谍"
# myquery = {"NAME": {"$regex": "^" + name}}
comid = 1359352573
comid2 = comid+1
time =  time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
doc = {"COMMENT_ID":str(comid2), "MOVIE_ID":"5113101", "CONTENT":"细节饱满，但不恐怖，很孤独", "COMMENT_TIME":time, "RATING":"2"}
x = col2.insert_one(doc)
# for x in flag:
print(x)
# print(flag)
# id = flag.get("MOVIE_ID")
# print(id)
# print(time)
# print(flag)
# if (flag == None):
#     print("没找到1")
# else:
#     id = flag.get("MOVIE_ID")
#     if id == None:
#         print("没找到2")
#     else:
#             myquery2 = {"MOVIE_ID": id}
#             print(myquery2)
#             flag2 = col2.find_one(myquery2)
#             doc = col2.find(myquery2)
#             if (flag2 == None):
#                 print("没找到3")
#             else:
#                 i = 0
#                 for y in doc:
#                     content = y.get("CONTENT")
#                     if content == None:
#                         content == "一般般"
#                     else:
#                         i += 1
#                         j = str(i)
#                         print("评论"+j+":"+content)
#                         i = int(j)



# Lost Prophet