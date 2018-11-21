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
def queryNews(db, publisher):
    cursor = db.cursor()
    sql = "SELECT * FROM news WHERE publisher = %s ORDER BY newsID DESC"
    news_list = {}
    try:
        cursor.execute(sql, publisher)
        results = cursor.fetchall()
        for row in results:
            tmp = {}
            newsID = row[0]
            tmp["publisher"] = row[1]
            tmp["title"] = row[2]
            tmp["author"] = row[3]
            tmp["content"] = row[4]
            tmp["like_num"] = row[5]
            tmp["dislike_num"] = row[6]
            news_list[str(newsID)] = tmp
    except Exception, Argument:
        print Argument
    return json.dumps(news_list)


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
        # return json.dumps(list_publisher)
        return list_publisher
    except Exception, Argument:
        print Argument
    return "False"


def search_by_keys(db, keyword):
    cursor = db.cursor()
    sql = "SELECT * FROM news WHERE title LIKE \'%"+keyword+"%\'  OR content LIKE \'%"+keyword+"%\' ORDER BY newsID DESC;"
    news_list = {}
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            tmp = {}
            newsID = row[0]
            tmp["publisher"] = row[1]
            tmp["title"] = row[2]
            tmp["author"] = row[3]
            tmp["content"] = row[4]
            tmp["like_num"] = row[5]
            tmp["dislike_num"] = row[6]
            news_list[str(newsID)] = tmp
    except Exception, Argument:
        print Argument
    return json.dumps(news_list)


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


# No such userName: False
# Password not correct: False
# Success: UserID
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
    ret = {}
    if postType == "0":
        ret["returnCode"] = 1
        ret["result"] = checkSubscription(db, userID)
    if postType == "1":
        publisherID = request.form.get('publisherid')
        if subscribePblisher(db, userID, publisherID) == "True":
            ret["returnCode"] = 1
        else:
            ret["returnCode"] = 0
    if postType == "2":
        publisherID = request.form.get('publisherid')
        if unsubscribe(db, userID, publisherID) == "True":
            ret["returnCode"] = 1
        else:
            ret["returnCode"] = 0
    return json.dumps(ret)



# News in json
# postType: 0-get news 1-search news
# 0: return news json by users' subscription
# 1: return news json by keywords
@app.route('/news', methods=['POST', 'GET'])
def getAllNews():
    type = request.form.get('posttype')
    db = connectdb()
    news = "False"
    print type
    if type == "0":
        publisher = request.form.get('publisher')
        print publisher
        news = queryNews(db, publisher)
    if type == "1":
        keyword = request.form.get('keyword')
        news = search_by_keys(db, keyword)
    closedb(db)
    return news


# postType: 0-comment 1-like 2-dislike 3-save
# return True if success
# else return False
# if like or dislike already exist, return False
@app.route('/comment', methods=['POST','GET'])
def makeComment():
    type = request.form.get('posttype')
    userID = request.form.get('userid')
    newsID = request.form.get('newsid')
    db = connectdb()
    ret = "False"
    if type == "0":
        comment = request.form.get('comment')
        ret = userComment(db, userID, newsID, comment)
    if type == "1":
        ret = userComment(db, userID, newsID, "like")
    if type == "2":
        ret = userComment(db, userID, newsID, "dislike")
    if type == "3":
        ret = saveNews(db, userID, newsID)
    closedb(db)
    return ret


# postType: 0-comment 1-like 2-dislike 3-save
# return True if success
# else return False
# if like or dislike already exist, return False
@app.route('/deleteComment', methods=['GET', 'POST'])
def deleteComment():
    type = request.form.get('posttype')
    userID = request.form.get('userid')
    newsID = request.form.get('newsid')
    db = connectdb()
    ret = 0
    if type == "0":
        comment = request.form.get('comment')
        ret = delete_comment(db, userID, newsID, comment)
    if type == "1":
        ret = delete_comment(db, userID, newsID, "like")
    if type == "2":
        ret = delete_comment(db, userID, newsID, "dislike")
    if type == "3":
        ret = deleteSave(db, userID, newsID)
    closedb(db)
    return ret
############################################################################


app.run(debug=True)
