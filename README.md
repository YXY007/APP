<h1>README</h1>
<h2>File Description</h2>
DB4APP.sql: file exported from localhost.

API4APP.py: python file for API

<h2>DB4APP</h2>
First import the sql file into localhost.

Host is 127.0.0.1.

Username is root .

Password is 123qweasd.

Database name is APP.

<h2>API4APP</h2>

Before you run the .py file, you should install the following package.

	brew install json-c
	sudo pip install PyMySQL
	sudo pip install flask

If pip and homebrew are not installed in your mac, you should install then first.

	sudo easy_install pip
	ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

After installing the packages, you can run the .py file. You will see the following words in red.

	 * Restarting with stat
	 * Debugger is active!
	 * Debugger PIN: 507-069-010

Then you can visit "**http://127.0.0.1:5000**" to check the API.

 <h3>Logon</h3>

 Address: http://127.0.0.1:5000/logon
 
 Post: username and password
 
 Return: **returnCode = 1** if logon succeed. **returnCode = 0** if the username already exist.

 <h3>Login</h3>

 Address: http://127.0.0.1:5000/login

 Post: username and password
 
 Return: **returnCode = 1** if login succeed. **returnCode = 0** if the username not exist or password incorrect.

 <h3>Subscribe</h3>
 Address: http://127.0.0.1:5000/subscribe
 
 Post: posttype (0, 1, 2), userid, publisherid (if needed)

* posttype = 0
	 Get all the publishers subscribed by the user. 
	 
	 **posttype** and **userid** are needed. publisherid is not necessary.
	 
	 Return: A list of publisher names in json.

	 **returnCode = 1** for success, **returnCode = 0** for fail


* posttype = 1
	 Subscribe a publisher by publisherID. 
	 
	 **posttype**, **userid** and **publisherid** are needed.
	 
	 Return: **returnCode = 1** if subscribing succeed. **returnCode = 0** if fail.
	 

* posttype = 2
	 
	 Unsubscribe a publisher by publisherID. 
	 
	 **posttype**, **userid** and **publisherid** are needed.

	 Return: **returnCode = 1** if unsubscribing succeed. **returnCode = 0** if fail.

<h3>News</h3>

Address: http://127.0.0.1:5000/news

Post: posttype (0, 1), publisher (if needed), keyword(if needed)

* posttype = 0

	Get all the news by publisher name ordered by the date when the news is published. 
	
	**posttype** and **publisher** (name) are needed. keyword is not necessary.

	publisher is a string of publishers. For example, when you need to find all the news published by Neuters and New York Times, youshould post "NEUTERS NYTIMES".

	Return: A list of news in json.

* posttype = 1
	Search news according to the keyword. 
	
	**posttype** and **keyword** are needed. **publisher** is not necessary.

	Return: A list of news in json, the result of searching.

<h3>Comment</h3>

Address: http://127.0.0.1:5000/comment

Post: posttype (0, 1, 2, 3), userid, newsid, comment (if needed)

* posttype = 0
	
	Add comment to the news.

	**posttype**, **userid**, **newsid** and **comment** are needed.

	Return: **returnCode = 1** if making comment succeed. **returnCode = 0** if fail.

* posttype = 1
	
	Add like to the news.
	
	**posttype**, **userid** and **newsid** are needed. comment is not necessary.
	
	Return: **returnCode = 1** if like succeed. **returnCode = 0** if fail.

* posttype = 2
	
	Add dislike to the news.

	**posttype**, **userid** and **newsid** are needed. comment is not necessary.

	Return: **returnCode = 1** if dislike succeed. **returnCode = 0** if fail.

* posttype = 3

	Save the news.
	
	**posttype**, **userid** and **newsid** are needed. comment is not necessary.
	
	Return: **returnCode = 1** if saving succeed. **returnCode = 0** if fail.

<h3>Delete Comment</h3>

Address: http://127.0.0.1:5000/deleteComment

Post: posttype (0, 1, 2, 3), userid, newsid, comment (if needed)

* posttype = 0
	
	Delete comment of the news.

	**posttype**, **userid**, **newsid** and **comment** are needed.

	Return: **returnCode = 1** if deleting comment succeed. **returnCode = 0** if fail.

* posttype = 1

	Delete like of the news.

	**posttype**, **userid** and **newsid**are needed. comment is not necessary.

	Return: **returnCode = 1** if deleteing like succeed. **returnCode = 0** if fail.

* posttype = 2
	
	deleting dislike to the news.
	
	**posttype**, **userid** and **newsid** are needed. comment is not necessary.

	Return: **returnCode = 1** if deleting dislike succeed. **returnCode = 0** if fail.

* posttype = 3
	Save the news.

	**posttype**, **userid** and **newsid** are needed. comment is not necessary.
	
	Return: **returnCode = 1** if succeed. **returnCode = 0** if fail.

<h3>Add Evaluation</h3>

Address: http://127.0.0.1:5000/evaluate

Post: newsid, like\_or\_dislike, operation

* like\_or\_dislike
	
	**like** for like, **dislike** for dislike

* operation
	
	**1** for add, **-1** for subtract

* returnCode
	
	**0** for success, **1** for fail
