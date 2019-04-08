# pgwebcli

A cli tool for pg-web which uses the query api to make the SQL querys.

# Installation

1) Need to have python2.7.
2) Install the `requirements.txt` using `pip install -r requirements.txt`
3) SET enviroment variable `PG_WEB_URL`,`COOKIE_KEY` and `COOKIE_VALUE`. 
  which you have to extract from the pg-web in a web browser.

# How to Use.

1)  ```cat /path/to/sql.sql | python pgweb.py```
2)  ```python pgweb.py```

*Note:* There is a bug due to which you will have to press enter twice to get the shell.
