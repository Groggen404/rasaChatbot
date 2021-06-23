# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.forms import FormValidationAction
import urllib.request
import pymongo
import random
import time
import json
import numpy as np

support_search = ["水瓶座", "双鱼座", "白羊座",
                  "金牛座", "双子座", "巨蟹座",
                  "狮子座", "处女座", "天秤座",
                  "天蝎座", "射手座", "摩羯座"]

def extract_horoscope(xingzuo):
    """
    check if xingzuo supported, this func just for lack of train data.
    :param xingzuo: item in track, eg: "巨蟹座"、"白羊座"
    :return:
    """
    if xingzuo is None:
        return None
    for name in support_search:
        if name in xingzuo:
            return name
    return None

class GetSportName(Action):
    def name(self):
        return 'action_return_sport_name'

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template="utter_ask_sport")

        return []

class GetGameName(Action):
    def name(self):
        return 'action_return_game_name'

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(template="utter_ask_game")

        return []

class HoroscopeMsgAction(Action):

    def name(self) -> Text:

        return "action_horoscope_msg"

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        errorflag = 1
        str1 = "http://api.tianapi.com/txapi/star/index?key=8228182d120df1024763546c91223d95&astro="

        str2 = tracker.get_slot("xingzuo")
        str2 = extract_horoscope(str2)

        if str2 == "白羊座":
            str2 = "aries"
        elif str2 == "金牛座":
            str2 = "taurus"
        elif str2 == "双子座":
            str2 = "gemini"
        elif str2 == "巨蟹座":
            str2 = "cancer"
        elif str2 == "狮子座":
            str2 = "leo"
        elif str2 == "处女座":
            str2 = "virgo"
        elif str2 == "天秤座":
            str2 = "libra"
        elif str2 == "天蝎座":
            str2 = "scorpio"
        elif str2 == "射手座":
            str2 = "sagittarius"
        elif str2 == "摩羯座":
            str2 = "capricorn"
        elif str2 == "水瓶座":
            str2 = "aquarius"
        elif str2 == "双鱼座":
            str2 = "pisces"
        else:
            dispatcher.utter_message("输入正确的星座哦")
            errorflag = 0

        if(errorflag>0):

            url = str1 + str2
            resp = urllib.request.urlopen(url)
            content = resp.read()
            t = content.decode()
            load_data = json.loads(t)
            data = load_data.get("newslist")
            result1 = []
            for i in data:
                result1.append(i.get("type"))
                result1.append(i.get("content"))
            # data2 = json.dumps(data)
            # t1 = data2.encode()
            data2 = json.dumps(result1)
            data3 = data2.encode('utf-8').decode('unicode_escape')
            dispatcher.utter_message(data3)

        return []

class FunctionFrom(FormValidationAction):

    def  name(self)  -> Text:
        return "validate_horoscope_form"

    def validate_xingzuo(
        self,
        value: Text,
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "Dict[Text,Any]",
    ) -> Dict[Text,Any]:

        if value.lower() in  self.horoscope_db():

            return {"xingzuo": value}
        else:
            dispatcher.utter_message("请输入正确的星座")
            return{"xingzuo": None}

class GetSportName(Action):
    def name(self):
        return 'action_return_sport_name'

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template="utter_ask_sport")

        return []

class ReturnActorMsg(Action):
    def name(self):
        return 'action_return_actor_msg'

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        gyb = pymongo.MongoClient("mongodb://localhost:27017/")

        db = gyb["FilmDB"]

        col = db["Filmdb"]

        actor = tracker.get_slot("actor")
        # director = tracker.get_slot("director")
        # language = tracker.get_slot("language")
        # type = tracker.get_slot("movie_type")
        # movie = tracker.get_slot("movie")

        Actquery = {"ACTORS": {"$regex": "^" + actor}}
        # Dirquery = {"DIRECTORS": {"$regex": "^" + director}}
        # Lanquery = {"LANGUAGES": {"$regex": "^" + language}}
        # Typequery = {"GENRES": {"$regex": "^" + type}}
        # Movquery = {"Name": {"$regex": "^" + movie}}
        flag  =  col.find_one(Actquery)
        if(flag == None):
            dispatcher.utter_message(text="对不起，没查到这位演员的相关作品")
        else:
            mydoc = col.find(Actquery)
            i = 0
            # dispatcher.utter_message(movie)
            dispatcher.utter_message(actor)
            # dispatcher.utter_message(language)
            # dispatcher.utter_message(type)
            # dispatcher.utter_message(director)

            for x in mydoc:
                # dispatcher.utter_message(x)
                name = x.get("NAME")
                alias = x.get("ALIAS")
                actors = x.get("ACTORS")
                directors = x.get("DIRECTORS")
                genres = x.get("GENRES")
                scores = x.get("DOUBAN_SCORE")
                votes = x.get("DOUBAN_VOTES")
                languages = x.get("LANGUAGES")
                regions = x.get("REGIONS")
                year = x.get("YEAR")
                url = x.get("COVER")
                story =  x.get("STORYLINE")
                if directors == None:
                    directors  =  "未知"
                if name == None:
                    name = "未知"
                if alias == None:
                    alias = "未知"
                if actors == None:
                    actors = "未知"
                if directors == None:
                    directors = "未知"
                if genres == None:
                    genres = "未知"
                if scores == None:
                    scores = "未知"
                if votes == None:
                    votes = "未知"
                if languages == None:
                    languages = "未知"
                if regions == None:
                    regions = "未知"
                if year == None:
                    year = "未知"
                if story == None:
                    story = "未知"
                i+=1
                j =  str(i)
                dispatcher.utter_message(text="-------------------"+j+"-----------------")
                # dispatcher.utter_message(text="片名:"+ name + "｜｜"+
                #                               "       别称:"+alias+"｜｜"+
                #                               "        演员列表：" + actors+"｜｜")
                # dispatcher.utter_message(text="片名：" + name)
                # dispatcher.utter_message(text="别称：" + alias)
                # dispatcher.utter_message(text="演员列表：" + actors)
                # dispatcher.utter_message(text="导演列表：" + directors)
                # dispatcher.utter_message(text="类型：" + genres)
                # dispatcher.utter_message(text="豆瓣评分：" + scores)
                # dispatcher.utter_message(text="用户得分：" + votes)
                # dispatcher.utter_message(text="语言：" + languages)
                # dispatcher.utter_message(text="地区：" + regions)
                # dispatcher.utter_message(text="年份：" + year)
                # dispatcher.utter_message(text="简介：" + story)
                dispatcher.utter_message(image = url)
                dispatcher.utter_message(text="-------------------"+j+"-----------------")
                i = int(j)
        return []

class ReturnDirMsg(Action):
    def name(self):
        return 'action_return_director_msg'

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        gyb = pymongo.MongoClient("mongodb://localhost:27017/")

        db = gyb["FilmDB"]

        col = db["Filmdb"]

        # actor = tracker.get_slot("actor")
        director = tracker.get_slot("director")
        # language = tracker.get_slot("language")
        # type = tracker.get_slot("movie_type")
        # movie = tracker.get_slot("movie")

        # Actquery = {"ACTORS": {"$regex": "^" + actor}}
        Dirquery = {"DIRECTORS": {"$regex": "^" + director}}
        # Lanquery = {"LANGUAGES": {"$regex": "^" + language}}
        # Typequery = {"GENRES": {"$regex": "^" + type}}
        # Movquery = {"Name": {"$regex": "^" + movie}}
        flag = col.find_one(Dirquery)
        if (flag == None):
            dispatcher.utter_message(text="对不起，没查到这位导演")
        else:
            mydoc = col.find(Dirquery).limit(3)
            i = 0
            # dispatcher.utter_message(movie)
            # dispatcher.utter_message(actor)
            # dispatcher.utter_message(language)
            # dispatcher.utter_message(type)
            dispatcher.utter_message(director)

            for x in mydoc:
                name = x.get("NAME")
                alias = x.get("ALIAS")
                actors = x.get("ACTORS")
                directors = x.get("DIRECTORS")
                scores = x.get("DOUBAN_SCORE")
                votes = x.get("DOUBAN_VOTES")
                languages = x.get("LANGUAGES")
                regions = x.get("REGIONS")
                year = x.get("YEAR")
                url = x.get("COVER")
                story =  x.get("STORYLINE")
                if directors == None:
                    directors  =  "未知"
                if name == None:
                    name = "未知"
                if alias == None:
                    alias = "未知"
                if actors == None:
                    actors = "未知"
                if directors == None:
                    directors = "未知"
                if scores == None:
                    scores = "未知"
                if votes == None:
                    votes = "未知"
                if languages == None:
                    languages = "未知"
                if regions == None:
                    regions = "未知"
                if year == None:
                    year = "未知"
                if story == None:
                    story = "未知"
                i+=1
                j =  str(i)
                dispatcher.utter_message(text="-------------------"+j+"-----------------")
                dispatcher.utter_message(text="片名：" + name)
                dispatcher.utter_message(text="别称：" + alias)
                dispatcher.utter_message(text="演员列表：" + actors)
                dispatcher.utter_message(text="导演列表：" + directors)
                dispatcher.utter_message(text="豆瓣评分：" + scores)
                dispatcher.utter_message(text="用户得分：" + votes)
                dispatcher.utter_message(text="语言：" + languages)
                dispatcher.utter_message(text="地区：" + regions)
                dispatcher.utter_message(text="年份：" + year)
                dispatcher.utter_message(text="简介：" + story)
                dispatcher.utter_message(image = url)
                dispatcher.utter_message(text="-------------------"+j+"-----------------")
                i = int(j)
        return []

class ReturnMovieMsg(Action):
    def name(self):
        return 'action_return_movie_msg'

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        gyb = pymongo.MongoClient("mongodb://localhost:27017/")

        db = gyb["FilmDB"]

        col = db["Filmdb"]

        # actor = tracker.get_slot("actor")
        # director = tracker.get_slot("director")
        # language = tracker.get_slot("language")
        # type = tracker.get_slot("movie_type")
        movie = tracker.get_slot("movie")

        # Actquery = {"ACTORS": {"$regex": "^" + actor}}
        # Dirquery = {"DIRECTORS": {"$regex": "^" + director}}
        # Lanquery = {"LANGUAGES": {"$regex": "^" + language}}
        # Typequery = {"GENRES": {"$regex": "^" + type}}
        Movquery = {"NAME": {"$regex": "^" + movie}}
        flag  =  col.find_one(Movquery)
        if(flag == None):
            dispatcher.utter_message(text="对不起，没查到这部电影")
        else:
            mydoc = col.find(Movquery)
            i = 0
            # dispatcher.utter_message(movie)
            # dispatcher.utter_message(actor)
            # dispatcher.utter_message(language)
            # dispatcher.utter_message(type)
            # dispatcher.utter_message(director)

            for x in mydoc:
                # dispatcher.utter_message(x)
                name = x.get("NAME")
                alias = x.get("ALIAS")
                actors = x.get("ACTORS")
                directors = x.get("DIRECTORS")
                genres = x.get("GENRES")
                scores = x.get("DOUBAN_SCORE")
                votes = x.get("DOUBAN_VOTES")
                languages = x.get("LANGUAGES")
                regions = x.get("REGIONS")
                year = x.get("YEAR")
                url = x.get("COVER")
                story =  x.get("STORYLINE")
                if directors == None:
                    directors  =  "未知"
                if name == None:
                    name = "未知"
                if alias == None:
                    alias = "未知"
                if actors == None:
                    actors = "未知"
                if directors == None:
                    directors = "未知"
                if genres == None:
                    genres = "未知"
                if scores == None:
                    scores = "未知"
                if votes == None:
                    votes = "未知"
                if languages == None:
                    languages = "未知"
                if regions == None:
                    regions = "未知"
                if year == None:
                    year = "未知"
                if story == None:
                    story = "未知"
                i+=1
                j =  str(i)
                dispatcher.utter_message(text="-------------------"+j+"-----------------")
                dispatcher.utter_message(text="片名：" + name)
                dispatcher.utter_message(text="别称：" + alias)
                dispatcher.utter_message(text="演员列表：" + actors)
                dispatcher.utter_message(text="导演列表：" + directors)
                dispatcher.utter_message(text="类型：" + genres)
                dispatcher.utter_message(text="豆瓣评分：" + scores)
                dispatcher.utter_message(text="用户得分：" + votes)
                dispatcher.utter_message(text="语言：" + languages)
                dispatcher.utter_message(text="地区：" + regions)
                dispatcher.utter_message(text="年份：" + year)
                dispatcher.utter_message(text="简介：" + story)
                dispatcher.utter_message(image = url)
                dispatcher.utter_message(text="-------------------"+j+"-----------------")
                i = int(j)
        return []

class ReturnMovieTypeMsg(Action):
    def name(self):
        return 'action_return_type_msg'

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        gyb = pymongo.MongoClient("mongodb://localhost:27017/")

        db = gyb["FilmDB"]

        col = db["Filmdb"]

        # actor = tracker.get_slot("actor")
        # director = tracker.get_slot("director")
        # language = tracker.get_slot("language")
        type = tracker.get_slot("movie_type")
        # movie = tracker.get_slot("movie")

        # Actquery = {"ACTORS": {"$regex": "^" + actor}}
        # Dirquery = {"DIRECTORS": {"$regex": "^" + director}}
        # Lanquery = {"LANGUAGES": {"$regex": "^" + language}}
        Typequery = {"GENRES": {"$regex": "^" + type}}
        # Movquery = {"NAME": {"$regex": "^" + movie}}
        flag  =  col.find_one(Typequery)
        if(flag == None):
            dispatcher.utter_message(text="对不起，没找到这种类型的电影")
        else:
            mydoc = col.find(Typequery).limit(5)
            i = 0
            # dispatcher.utter_message(movie)
            # dispatcher.utter_message(actor)
            # dispatcher.utter_message(language)
            dispatcher.utter_message(type)
            # dispatcher.utter_message(director)

            for x in mydoc:
                # dispatcher.utter_message(x)
                name = x.get("NAME")
                alias = x.get("ALIAS")
                actors = x.get("ACTORS")
                directors = x.get("DIRECTORS")
                genres = x.get("GENRES")
                scores = x.get("DOUBAN_SCORE")
                votes = x.get("DOUBAN_VOTES")
                languages = x.get("LANGUAGES")
                regions = x.get("REGIONS")
                year = x.get("YEAR")
                url = x.get("COVER")
                story =  x.get("STORYLINE")
                if directors == None:
                    directors  =  "未知"
                if name == None:
                    name = "未知"
                if alias == None:
                    alias = "未知"
                if actors == None:
                    actors = "未知"
                if directors == None:
                    directors = "未知"
                if genres == None:
                    genres = "未知"
                if scores == None:
                    scores = "未知"
                if votes == None:
                    votes = "未知"
                if languages == None:
                    languages = "未知"
                if regions == None:
                    regions = "未知"
                if year == None:
                    year = "未知"
                if story == None:
                    story = "未知"
                i+=1
                j =  str(i)
                dispatcher.utter_message(text="-------------------"+j+"-----------------")
                dispatcher.utter_message(text="片名：" + name)
                dispatcher.utter_message(text="别称：" + alias)
                dispatcher.utter_message(text="演员列表：" + actors)
                dispatcher.utter_message(text="导演列表：" + directors)
                dispatcher.utter_message(text="类型：" + genres)
                dispatcher.utter_message(text="豆瓣评分：" + scores)
                dispatcher.utter_message(text="用户得分：" + votes)
                dispatcher.utter_message(text="语言：" + languages)
                dispatcher.utter_message(text="地区：" + regions)
                dispatcher.utter_message(text="年份：" + year)
                dispatcher.utter_message(text="简介：" + story)
                dispatcher.utter_message(image = url)
                dispatcher.utter_message(text="-------------------"+j+"-----------------")
                i = int(j)
        return []

class ReturnLanguageMsg(Action):
    def name(self):
        return 'action_return_language_msg'

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        gyb = pymongo.MongoClient("mongodb://localhost:27017/")

        db = gyb["FilmDB"]

        col = db["Filmdb"]

        # actor = tracker.get_slot("actor")
        # director = tracker.get_slot("director")
        language = tracker.get_slot("language")
        # type = tracker.get_slot("movie_type")
        # movie = tracker.get_slot("movie")

        # Actquery = {"ACTORS": {"$regex": "^" + actor}}
        # Dirquery = {"DIRECTORS": {"$regex": "^" + director}}
        Lanquery = {"LANGUAGES": {"$regex": "^" + language}}
        # Typequery = {"GENRES": {"$regex": "^" + type}}
        # Movquery = {"Name": {"$regex": "^" + movie}}
        flag  =  col.find_one(Lanquery)
        if(flag == None):
            dispatcher.utter_message(text="对不起，没找到这种类型的电影")
        else:
            mydoc = col.find(Lanquery).limit(5)
            i = 0
            # dispatcher.utter_message(movie)
            # dispatcher.utter_message(actor)
            dispatcher.utter_message(language)
            # dispatcher.utter_message(type)
            # dispatcher.utter_message(director)

            for x in mydoc:
                # dispatcher.utter_message(x)
                name = x.get("NAME")
                alias = x.get("ALIAS")
                actors = x.get("ACTORS")
                directors = x.get("DIRECTORS")
                genres = x.get("GENRES")
                scores = x.get("DOUBAN_SCORE")
                votes = x.get("DOUBAN_VOTES")
                languages = x.get("LANGUAGES")
                regions = x.get("REGIONS")
                year = x.get("YEAR")
                url = x.get("COVER")
                story =  x.get("STORYLINE")
                if directors == None:
                    directors  =  "未知"
                if name == None:
                    name = "未知"
                if alias == None:
                    alias = "未知"
                if actors == None:
                    actors = "未知"
                if directors == None:
                    directors = "未知"
                if genres == None:
                    genres = "未知"
                if scores == None:
                    scores = "未知"
                if votes == None:
                    votes = "未知"
                if languages == None:
                    languages = "未知"
                if regions == None:
                    regions = "未知"
                if year == None:
                    year = "未知"
                if story == None:
                    story = "未知"
                i+=1
                j =  str(i)
                dispatcher.utter_message(text="-------------------"+j+"-----------------")
                dispatcher.utter_message(text="片名：" + name)
                dispatcher.utter_message(text="别称：" + alias)
                dispatcher.utter_message(text="演员列表：" + actors)
                dispatcher.utter_message(text="导演列表：" + directors)
                dispatcher.utter_message(text="类型：" + genres)
                dispatcher.utter_message(text="豆瓣评分：" + scores)
                dispatcher.utter_message(text="用户得分：" + votes)
                dispatcher.utter_message(text="语言：" + languages)
                dispatcher.utter_message(text="地区：" + regions)
                dispatcher.utter_message(text="年份：" + year)
                dispatcher.utter_message(text="简介：" + story)
                dispatcher.utter_message(image = url)
                dispatcher.utter_message(text="-------------------"+j+"-----------------")
                i = int(j)
        return []

class ReturnComment(Action):
    def name(self):
        return 'action_return_comment'

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        gyb = pymongo.MongoClient("mongodb://localhost:27017/")

        db = gyb["FilmDB"]
        col1 = db["Filmdb"]
        col2 = db["Comment"]

        name = tracker.get_slot("movie")
        myquery = {"NAME": {"$regex": "^" + name}}
        flag = col1.find_one(myquery)
        # print("flag1=",flag)
        if (flag == None):
            dispatcher.utter_message(text="对不起，没找到这部电影，没办法看评论喔")     #没在电影表里找到电影
        else:
            id = flag.get("MOVIE_ID")
            myquery2 = {"MOVIE_ID": id}
            flag2 = col2.find_one(myquery2)
            # print("flag2=",flag2)
            doc = col2.find(myquery2)
            if (flag2 == None):
                dispatcher.utter_message(text="没找到这个电影id")
            else:
                i = 0
                dispatcher.utter_message(template="utter_ShowComment")
                for y in doc:
                    content = y.get("CONTENT")
                    if content == None:
                        content == "一般般"
                    else:
                        i += 1
                        j = str(i)
                        dispatcher.utter_message(text="评论" + j + ":" + content)
                        i = int(j)
        return []

class InsertComment(Action):
    def name(self):
        return 'action_insert_comment'

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        gyb = pymongo.MongoClient("mongodb://localhost:27017/")

        db = gyb["FilmDB"]
        col1 = db["Filmdb"]
        col2 = db["Comment"]

        name = tracker.get_slot("movie")
        comment = tracker.get_slot("comment")
        score = tracker.get_slot("score")
        curtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        myquery = {"NAME": {"$regex": "^" + name}}
        flag = col1.find_one(myquery)
        print("flag1=",flag)
        if (flag == None):
            dispatcher.utter_message(text="对不起，没找到这部电影，没办法看评论喔")     #没在电影表里找到电影
        else:
            id = flag.get("MOVIE_ID")
            myquery2 = {"MOVIE_ID": id}
            flag2 = col2.find_one(myquery2)
            print("flag2=",flag2)
            if (flag2 == None):                                                 #没在评论表里找到该电影的评论
                dispatcher.utter_message(text="没找到这个相关评论")
                comid = random.randint(1000000000,10000000000)
                comid2 = str(comid)
                doc = {"COMMENT_ID": comid2,
                       "MOVIE_ID": id,
                       "CONTENT": comment,
                       "COMMENT_TIME": curtime,
                       "RATING": score}
                x = col2.insert_one(doc)
                print("添加的数据:", x)
                dispatcher.utter_message(text="已经添加您的影评！")
                dispatcher.utter_message(text="片名：" + name)
                dispatcher.utter_message(text="评论ID：" + comid2)
                dispatcher.utter_message(text="评论：" + comment)
            else:
                dispatcher.utter_message(text="有相关评论")
                for x in flag2:
                    comid = random.randint(1000000000,10000000000)
                    comid2 = str(comid)
                doc = {"COMMENT_ID": comid2,
                       "MOVIE_ID": id,
                       "CONTENT": comment,
                       "COMMENT_TIME": curtime,
                       "RATING": score}
                x = col2.insert_one(doc)
                print("添加的数据:", x)
                dispatcher.utter_message(text="已经添加您的影评！")
                dispatcher.utter_message(text="片名：" + name)
                dispatcher.utter_message(text="评论ID：" + comid2)
                dispatcher.utter_message(text="评论：" + comment)
        return []

class UrlTest(Action):
    def name(self):
        return 'action_url_test'

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(image="https://image.baidu.com/search/detail?ct=503316480&z=undefined&tn=baiduimagedetail&ipn=d&word=%E9%97%AE%E5%A5%BD%E7%9A%84%E5%9B%BE%E7%89%87url&step_word=&ie=utf-8&in=&cl=2&lm=-1&st=undefined&hd=undefined&latest=undefined&copyright=undefined&cs=1961719932,3096687454&os=3484362129,2163910543&simid=4087382117,363171096&pn=2&rn=1&di=1430&ln=1171&fr=&fmq=1620564155561_R&fm=&ic=undefined&s=undefined&se=&sme=&tab=0&width=undefined&height=undefined&face=undefined&is=0,0&istype=0&ist=&jit=&bdtype=0&spn=0&pi=0&gsm=0&hs=2&objurl=https%3A%2F%2Fgimg2.baidu.com%2Fimage_search%2Fsrc%3Dhttp%253A%252F%252F588ku.izihun.com%252Felement_pic%252F18%252F08%252F16%252Ffc1258e8d9f9b70ae5368303bf522912.jpg%2521%252Ffw%252F820%252Fquality%252F100%252Funsharp%252Ftrue%252Fcompress%252Ftrue%252Fformat%252Fjpeg%26refer%3Dhttp%253A%252F%252F588ku.izihun.com%26app%3D2002%26size%3Df9999%2C10000%26q%3Da80%26n%3D0%26g%3D0n%26fmt%3Djpeg%3Fsec%3D1623156155%26t%3Df262ae49e58de679d729708507818c5d&rpstart=0&rpnum=0&adpicid=0&force=undefined")

        return []