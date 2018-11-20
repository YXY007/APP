<h1>README</h1>
<h2>File Description</h2>
<p>DB4APP.sql: file exported from localhost.</p>
<p>API4APP.py: python file for API</p>
<h2>DB4APP</h2>
<p>First import the sql file into localhost.</p>
<p>Host is 127.0.0.1.</p>
<p>Username is root .</p>
<p>Password is 123qweasd.</p>
<p>Database name is APP.</p>
<h2>API4APP</h2>
<p>Before you run the .py file, you should install the following package.</p>

	brew install json-c
	sudo pip install PyMySQL
	sudo pip install flask

<p>If pip and homebrew are not installed in your mac, you should install then first.</p>

	sudo easy_install pip
	ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

<p>After installing the packages, you can run the .py file. You will see the following words in red.</p>

	 * Restarting with stat
	 * Debugger is active!
	 * Debugger PIN: 507-069-010

 <p>Then you can visit "**http://127.0.0.1:5000**" to check the API.</p>
 <h3>Logon</h3>
 <p>Address: http://127.0.0.1:5000/logon</p>
 <p>Post: username and password</p>
 <p>Return: **True** if logon succeed. **False** if the username already exist.</p>

 <h3>Login</h3>
 <p>Address: http://127.0.0.1:5000/login</p>
 <p>Post: username and password</p>
 <p>Return: **True** if login succeed. **False** if the username not exist or password incorrect.</p>

 <h3>Subscribe</h3>
 <p>Address: http://127.0.0.1:5000/subscribe</p>
 <p>Post: posttype (0, 1, 2), userid, publisherid (if needed)</p>

 * posttype = 0
	 <p>Get all the publishers subscribed by the user. </p>
	 <p>**posttype** and **userid** are needed. publisherid is not necessary.</p>
	 <p>Return: A list of publisher names in json.</p>

* posttype = 1
	 <p>Subscribe a publisher by publisherID. </p>
	 <p>**posttype**, **userid** and **publisherid** are needed.</p>
	 <p>Return: **True** if subscribing succeed. **False** if fail.</p>
	 
* posttype = 2
	 <p>Unsubscribe a publisher by publisherID. </p>
	 <p>**posttype**, **userid** and **publisherid** are needed.</p>
	 <p>Return: **True** if unsubscribing succeed. **False** if fail.</p>

<h3>News</h3>
<p>Address: http://127.0.0.1:5000/news</p>
<p>Post: posttype (0, 1), publisher (if needed), keyword(if needed)</p>

* posttype = 0
	<p>Get all the news by publisher name ordered by the date when the news is published. </p>
	<p>**posttype** and **publisher** (name) are needed. keyword is not necessary.</p>
	<p>publisher is a string of publishers. For example, when you need to find all the news published by Neuters and New York Times, youshould post "NEUTERS NYTIMES".</p>
	<p>Return: A list of news in json.</p>

* posttype = 1
	<p>Search news according to the keyword. </p>
	<p>**posttype** and **keyword** are needed. **publisher** is not necessary.</p>
	<p>Return: A list of news in json, the result of searching.</p>

<h3>Comment</h3>
<p>Address: http://127.0.0.1:5000/comment</p>
<p>Post: posttype (0, 1, 2, 3), userid, newsid, comment (if needed)</p>

* posttype = 0
	<p>Add comment to the news.</p>
	<p>**posttype**, **userid**, **newsid** and **comment** are needed.</p>
	<p>Return: **True** if making comment succeed. **False** if fail.</p>

* posttype = 1
	<p>Add like to the news.</p>
	<p>**posttype**, **userid** and **newsid** are needed. comment is not necessary.</p>
	<p>Return: **True** if like succeed. **False** if fail.</p>

* posttype = 2
	<p>Add dislike to the news.</p>
	<p>**posttype**, **userid** and **newsid** are needed. comment is not necessary.</p>
	<p>Return: **True** if dislike succeed. **False** if fail.</p>

* posttype = 3
	<p>Save the news.</p>
	<p>**posttype**, **userid** and **newsid** are needed. comment is not necessary.</p>
	<p>Return: **True** if saving succeed. **False** if fail.</p>

<h3>Delete Comment</h3>
<p>Address: http://127.0.0.1:5000/deleteComment</p>
<p>Post: posttype (0, 1, 2, 3), userid, newsid, comment (if needed)</p>

* posttype = 0
	<p>Delete comment of the news.</p>
	<p>**posttype**, **userid**, **newsid** and **comment** are needed.</p>
	<p>Return: **True** if deleting comment succeed. **False** if fail.</p>

* posttype = 1
	<p>Delete like of the news.</p>
	<p>**posttype**, **userid** and **newsid**are needed. comment is not necessary.</p>
	<p>Return: **True** if deleteing like succeed. **False** if fail.</p>

* posttype = 2
	<p>deleting dislike to the news.</p>
	<p>**posttype**, **userid** and **newsid** are needed. comment is not necessary.</p>
	<p>Return: **True** if deleting dislike succeed. **False** if fail.</p>

* posttype = 3
	<p>Save the news.</p>
	<p>**posttype**, **userid** and **newsid** are needed. comment is not necessary.</p>
	<p>Return: **True** if succeed. **False** if fail.</p>
