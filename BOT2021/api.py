import urllib.request
import json
import numpy as np
str1 = "http://api.tianapi.com/txapi/star/index?key=8228182d120df1024763546c91223d95&astro=aries"
resp = urllib.request.urlopen(str1)
content = resp.read()
t = content.decode()
load_data = json.loads(t)
data = load_data.get("newslist")
result1 = []
for i in data:
    result1.append(i.get("type"))
    result1.append(i.get("content"))
data2 = np.array(result1)
print(data)
print(data2)






# {"code":200,
#  "msg":"success",
#  "newslist":
#     [
#         {"type":"综合指数","content":"60%"},
#         {"type":"爱情指数","content":"60%"},
#         {"type":"工作指数","content":"70%"},
#         {"type":"财运指数","content":"50%"},
#         {"type":"健康指数","content":"85%"},
#         {"type":"幸运颜色","content":"青色"},
#         {"type":"幸运数字","content":"2"},
#         {"type":"贵人星座","content":"水瓶座"},
#         {"type":"今日概述","content":"今天的你很有可能进行冲动支出，消费之前再三思考，切忌盲目跟风，适合自己的才是最好的。爱情方面进入平缓期，最近你们没有什么大的矛盾，可以尝试进行约会，巩固感情。"}
#     ]
#  }
