# coding=UTF-8
import json
import pymysql
from flask import Flask, render_template, request

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


######################database#################################
def connectdb():
    print "connecting"
    conn = pymysql.Connect(host="127.0.0.1", user="root", passwd="123qweasd", db="APP", charset="utf8")
    print "connection successful"
    return conn


# insert
def insertdb(db, newsData):

    cursor = db.cursor()
    sql = 'INSERT INTO news (publisher, title, author, date, content) ' \
          'VALUES (%s, %s, %s, %s, %s);'

    try:
        cursor.execute("USE APP;")
        cursor.execute(sql, ("REUTERS", newsData['title'], newsData['author'], newsData['time'], newsData['content']))
        db.commit()
    except Exception, Argument:
        # Rollback in case there is any error
        print Argument
        db.rollback()


def newUser(db, userName, password):
    cursor = db.cursor()
    sql1 = "SELECT * FROM user WHERE userName = %s"
    try:
        cursor.execute("USE APP;")
        cursor.execute(sql1, (userName))
        db.commit()
        results = cursor.fetchall()
        if len(results) != 0:
            return "False"
    except Exception, Argument:
        # Rollback in case there is any error
        print Argument
        db.rollback()

    sql = 'INSERT INTO user (userName, password) VALUES (%s, %s);'
    try:
        cursor.execute("USE APP;")
        cursor.execute(sql, (userName, password))
        db.commit()
    except Exception, Argument:
        # Rollback in case there is any error
        print Argument
        db.rollback()
    return "True"


def subscribePblisher(db, userID, publisherID):
    cursor = db.cursor()
    sql = "INSERT INTO subscribe (userID, publisherID) VALUES (%s, %s);"
    try:
        cursor.execute("USE APP;")
        cursor.execute(sql, (userID, publisherID))
        db.commit()
        return "True"
    except Exception, Argument:
        # Rollback in case there is any error
        print Argument
        db.rollback()
    return "False"


def userComment(db, userID, newsID, comment):
    cursor = db.cursor()
    if (comment == "like") | (comment == "dislike"):
        sql1 = "SELECT * FROM comment WHERE userID = %s and newsID = %s and comment = %s;"
        try:
            cursor.execute("USE APP;")
            cursor.execute(sql1, (userID, newsID, comment))
            db.commit()
            results = cursor.fetchall()
            if len(results) != 0:
                return "False"
        except Exception, Argument:
            # Rollback in case there is any error
            print Argument
            db.rollback()

    sql = "INSERT INTO comment (userID, newsID, comment) VALUES (%s, %s, %s);"
    try:
        cursor.execute("USE APP;")
        cursor.execute(sql, (userID, newsID, comment))
        db.commit()
        return "True"
    except Exception, Argument:
        # Rollback in case there is any error
        print Argument
        db.rollback()
    return "False"


def saveNews(db, userID, newsID):
    cursor = db.cursor()
    sql1 = "SELECT * FROM save WHERE userID = %s and newsID = %s;"
    try:
        cursor.execute("USE APP;")
        cursor.execute(sql1, (userID, newsID))
        db.commit()
        results = cursor.fetchall()
        if len(results) != 0:
            return "False"
    except Exception, Argument:
        # Rollback in case there is any error
        print Argument
        db.rollback()

    sql = "INSERT INTO save (userID, newsID) VALUES (%s, %s);"
    try:
        cursor.execute("USE APP;")
        cursor.execute(sql, (userID, newsID))
        db.commit()
        return "True"
    except Exception, Argument:
        # Rollback in case there is any error
        print Argument
        db.rollback()
    return "False"


# query
def allNews(db):
    cursor = db.cursor()
    sql = "SELECT * FROM news;"
    news_list = []
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            tmp = {}
            newsID = row[0]
            tmp["publisher"] = row[1]
            sql = "SELECT publisherID FROM APP.publisher WHERE publisherName = %s;"
            cursor.execute(sql, tmp["publisher"])
            publisher = cursor.fetchall()
            tmp["publisherID"] = publisher[0][0]
            tmp["title"] = row[2]
            tmp["author"] = row[3]
            tmp["time"] = row[4]
            tmp["content"] = json.loads(row[5])
            for item in tmp["content"]:
                if item["type"] == "image":
                    tmp["thumbnail"] = item["content"]
                    break
            tmp["like_num"] = row[6]
            tmp["dislike_num"] = row[7]
            tmp["newsID"] = newsID
            # news_list[str(newsID)] = tmp
            news_list.append(tmp)
    except Exception, Argument:
        print Argument
    return news_list


def queryNews(db, publisher):
    cursor = db.cursor()
    sql = "SELECT * FROM news WHERE "
    for index, name in enumerate(publisher):
        if index != 0:
            sql = sql + " OR "
        sql = sql + "publisher = '" + str(name) + "'"
    sql = sql + " ORDER BY newsID DESC;"
    news_list = []
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            tmp = {}
            newsID = row[0]
            tmp["publisher"] = row[1]
            sql = "SELECT publisherID FROM APP.publisher WHERE publisherName = %s;"
            cursor.execute(sql, tmp["publisher"])
            publisher = cursor.fetchall()
            tmp["publisherID"] = publisher[0][0]
            tmp["title"] = row[2]
            tmp["author"] = row[3]
            tmp["time"] = row[4]
            tmp["content"] = json.loads(row[5])
            for item in tmp["content"]:
                if item["type"] == "image":
                    tmp["thumbnail"] = item["content"]
                    break
            tmp["like_num"] = row[6]
            tmp["dislike_num"] = row[7]
            tmp["newsID"] = newsID
            # news_list[str(newsID)] = tmp
            news_list.append(tmp)
    except Exception, Argument:
        print Argument
    return news_list


def checkPassword(db, userName, password):
    cursor = db.cursor()
    sql = "SELECT * FROM user where userName = %s;"
    try:
        cursor.execute(sql, userName)
        results = cursor.fetchall()
        print results
        if len(results) > 0:
            if password == results[0][2]:
                return str(results[0][0])
            else:
                return "False"
        else:
            return "False"
    except Exception, Argument:
        print Argument
    return "False"


def checkSubscription(db, userID):
    cursor = db.cursor()
    sql = "SELECT * FROM subscribe where userID = %s;"
    sql_publisher = "SELECT publisherName FROM publisher where publisherID = '%d';"
    try:
        cursor.execute(sql, userID)
        results = cursor.fetchall()
        publisherID = []
        for row in results:
            publisherID.append(row[1])
        publisherName = []
        for i in publisherID:
            cursor.execute(sql_publisher % i) #publisherID
            publisher = cursor.fetchall()
            publisherName.append(publisher[0][0])
        list_publisher = {}
        list_publisher["publisher"] = publisherName
        return list_publisher
    except Exception, Argument:
        print Argument
    return "False"

def getPublisher(db):
    cursor = db.cursor()
    sql = "SELECT * FROM publisher;"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        publisher_list = []
        for row in results:
            tmp = {}
            tmp["publisherID"] = row[0]
            tmp["publisherName"] = row[1]
            publisher_list.append(tmp)
        return publisher_list
    except Exception, Argument:
        print Argument
    return "False"


def search_by_keys(db, keyword):
    cursor = db.cursor()
    sql = "SELECT * FROM news WHERE title LIKE \'%"+keyword+"%\'  OR content LIKE \'%"+keyword+"%\' ORDER BY newsID DESC;"
    news_list = []
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            tmp = {}
            newsID = row[0]
            tmp["publisher"] = row[1]
            sql = "SELECT publisherID FROM APP.publisher WHERE publisherName = %s;"
            cursor.execute(sql, tmp["publisher"])
            publisher = cursor.fetchall()
            tmp["publisherID"] = publisher[0][0]
            tmp["title"] = row[2]
            tmp["author"] = row[3]
            tmp["time"] = row[4]
            tmp["content"] = json.loads(row[5])
            for item in tmp["content"]:
                if item["type"] == "image":
                    tmp["thumbnail"] = item["content"]
                    break
            tmp["like_num"] = row[6]
            tmp["dislike_num"] = row[7]
            tmp["newsID"] = newsID
            # news_list[str(newsID)] = tmp
            news_list.append(tmp)
    except Exception, Argument:
        print Argument
    return news_list


#delete
def unsubscribe(db, userID, publisherID):
    cursor = db.cursor()
    sql = "DELETE FROM subscribe WHERE userID = %s and publisherID = %s;"
    try:
        cursor.execute("USE APP;")
        cursor.execute(sql, (userID, publisherID))
        db.commit()
        return "True"
    except Exception, Argument:
        # Rollback in case there is any error
        print Argument
        db.rollback()
    return "False"

def delete_comment(db, userID, newsID, comment):
    cursor = db.cursor()
    sql = "DELETE FROM comment WHERE userID = %s and newsID = %s and comment = %s;"
    try:
        cursor.execute("USE APP;")
        cursor.execute(sql, (userID, newsID, comment))
        db.commit()
        return "True"
    except Exception, Argument:
        # Rollback in case there is any error
        print Argument
        db.rollback()
    return "False"


def deleteSave(db, userID, newsID):
    cursor = db.cursor()
    sql = "DELETE FROM save WHERE userID = %s and newsID = %s;"
    try:
        cursor.execute("USE APP;")
        cursor.execute(sql % (userID, newsID))
        db.commit()
        return "True"
    except Exception, Argument:
        # Rollback in case there is any error
        print Argument
        db.rollback()
    return "False"


# update
# likeFlag = 1 for like, 0 for dislike
# exeCode = 1 for add, 0 for minus
def updateLike(db, userID, newsID, likeFlag, exeCode):
    cursor = db.cursor()
    if exeCode == 0:
        num = ["dislike_num", "like_num"]
        sql1 = "SELECT % FROM news where userID = %s and newsID = %s;"
        try:
            cursor.execute("USE APP;")
            cursor.execute(sql1 % (num[likeFlag], userID, newsID))
            db.commit()
            results = cursor.fetchall()
            if results[0][0] == "0":
                return "False"
        except Exception, Argument:
            # Rollback in case there is any error
            print Argument
            db.rollback()

    like = ["dislike_num", "like_num"]
    exe  = ["-", "+"]
    sql = "UPDATE news SET %s = %s %s 1 WHERE newsID = %s;"
    try:
        cursor.execute("USE APP;")
        cursor.execute(sql % (like[likeFlag], like[likeFlag], exe[exeCode], newsID))
        db.commit()
        return "True"
    except Exception, Argument:
        # Rollback in case there is any error
        print Argument
        db.rollback()
    return "False"

# close
def closedb(db):
    db.close()


##########################api###############################################
app = Flask(__name__)


# Success: return True
# the userName already exist: return False
@app.route('/logon', methods=['GET', 'POST'])
def logon():
    username = request.form.get('username')
    password = request.form.get('password')
    db = connectdb()
    ret = newUser(db, username, password)
    closedb(db)
    result = {}
    if ret == "False":
        result["returnCode"] = 0
    else:
        result["returnCode"] = 1
    return json.dumps(result)


# No such userName： returnCode = 0
# Password not correct: returnCode = 0
# Success: returnCode = 1, UserID
@app.route('/login', methods=['GET', 'POST'])
def login():
    userName = request.form.get('username')
    password = request.form.get('password')
    db = connectdb()
    ret = checkPassword(db, userName, password)
    closedb(db)
    result = {}
    if ret == "False":
        result["returnCode"] = 0
    else:
        result["returnCode"] = 1
        result["userID"] = ret
    return json.dumps(result)


# postType: 0-check 1-subscribe 2-unsubscribe
# 0: return subscribe list
# 1: return True or False
# 2: return True or False
@app.route('/subscribe', methods=['POST', 'GET'])
def subscribe():
    postType = request.form.get('posttype')
    userID = request.form.get('userid')
    db = connectdb()
    ret = "False"
    if postType == "0":
        ret = checkSubscription(db, userID)
    if postType == "1":
        publisherID = request.form.get('publisherid')
        ret = subscribePblisher(db, userID, publisherID)
    if postType == "2":
        publisherID = request.form.get('publisherid')
        ret = unsubscribe(db, userID, publisherID)
    result = {}
    if ret == "False":
        result["returnCode"] = 0
    else:
        result["returnCode"] = 1
        if ret != "True":
            result["returnContent"] = ret
    return json.dumps(result)


# get all publishers 
@app.route('/publisher', methods=['GET'])
def publisher():
    db = connectdb()
    ret = getPublisher(db)
    closedb(db)
    result = {}
    if ret == "False":
        result["returnCode"] = 0
    else:
        result["returnCode"] = 1
        result["publisher"] = ret
    return json.dumps(result)



# News in json
# postType: 0-get news 1-search news
# 0: return news json by users' subscription
# 1: return news json by keywords
# 2: return all the news
@app.route('/news', methods=['POST', 'GET'])
def getAllNews():
    type = request.form.get('posttype')
    db = connectdb()
    news = "False"
    if type == "0":
        publisher = request.form.get('publisher')
        publishers = publisher.split(" ")
        news = queryNews(db, publishers)
    if type == "1":
        keyword = request.form.get('keyword')
        news = search_by_keys(db, keyword)
    if type == "2":
        news = allNews(db)
    closedb(db)
    result = {}
    if news == "False":
        result["returnCode"] = 0
    else:
        result["returnCode"] = 1
        result["returnContent"] = news
    return json.dumps(result)


# postType: 0-comment 1-like 2-dislike 3-save
# returnCode = 1 if success
# else returnCode = 0
# if like or dislike already exist, returnCode = 0
@app.route('/comment', methods=['POST','GET'])
def makeComment():
    type = request.form.get('posttype')
    userID = request.form.get('userid')
    newsID = request.form.get('newsid')
    db = connectdb()
    ret = "False"
    ret2 = "False"
    if type == "0":
        comment = request.form.get('comment')
        ret = userComment(db, userID, newsID, comment)
        ret2 = "True"
    if type == "1":
        ret = userComment(db, userID, newsID, "like")
        ret2 = updateLike(db, userID, newsID, 1, 1)
    if type == "2":
        ret = userComment(db, userID, newsID, "dislike")
        ret2 = updateLike(db, userID, newsID, 0,1)
    if type == "3":
        ret = saveNews(db, userID, newsID)
        ret2 = "True"
    result = {}
    if (ret == "False") | (ret2 == "False"):
        result["returnCode"] = 0
        db.rollback()
    else:
        result["returnCode"] = 1
    closedb(db)
    return json.dumps(result)


# postType: 0-comment 1-like 2-dislike 3-save
# returnCode = 1 if success
# else returnCode = 0
@app.route('/deleteComment', methods=['GET', 'POST'])
def deleteComment():
    type = request.form.get('posttype')
    userID = request.form.get('userid')
    newsID = request.form.get('newsid')
    db = connectdb()
    ret = "False"
    ret2 = "False"
    if type == "0":
        comment = request.form.get('comment')
        ret = delete_comment(db, userID, newsID, comment)
        ret2 = "True"
    if type == "1":
        ret = delete_comment(db, userID, newsID, "like")
        ret2 = updateLike(db, userID, newsID, 1, 0)
    if type == "2":
        ret = delete_comment(db, userID, newsID, "dislike")
        ret2 = updateLike(db, userID, newsID, 0, 0)
    if type == "3":
        ret = deleteSave(db, userID, newsID)
        ret2 = "True"
    result = {}
    if (ret == "False") | (ret2 == "False"):
        result["returnCode"] = 0
        db.rollback()
    else:
        result["returnCode"] = 1
    closedb(db)

    return json.dumps(result)
############################################################################


app.run(debug=True)
