ReactJS_flask

# ReactJS_flask


----------
This is a simple demo built with ```Flask + ReactJS + ChartJS + boostrap3```, originally from [@lkoczwara][1] but has changed much, in order that sometimes we can use for showing our presentation or managing Databases.

Particularly, it is initially run with [Spark][2], so do make sure your machine has install [Spark][3] and modify the file **run.sh**.

# Overview

----------
Post and show.

![这里写图片描述](http://img.blog.csdn.net/20160726160152194)

Spark example.

![这里写图片描述](http://img.blog.csdn.net/20160726160219540)



# Install & Run

----------
```
$ npm install
$ bower install
$ ./run.sh
```
For some reason it may go wrong, so you should install extra softwares, like some Python packages you can add to ```/project/site-packages``` or just using 
```
$ pip install [packages name] 
```
If your machines don't support Spark,you can just modify the file **run.sh** and remove several code-lines in project/app/main/views.py.

# Your Programs


----------

 - Modify bootstrap :
```
/project/app/static/bower_components/bootstrap
```
-  Modify html file :
```
/project/app/templates
```

- Modify controller views :
```
/project/app/main/views.py
/project/app/auth/views.py
```
- Modify js:
```
/project/app/static/js/reactjsx/main.js
```
Transform jsx to js
```shell
$ gulp transform
```


  [1]: https://github.com/lkoczwara/ReactJS_Dashboard/
  [2]: https://github.com/apache/spark
  [3]: https://github.com/apache/spark