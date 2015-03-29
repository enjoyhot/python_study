# 说明

### 1、前文
虽然目前CSDN支持markdown，但以前的文章都是用xeditor编辑器写的，不能导出，所以调研了方法。
总体而言有两种方法，但好像没多少人采用，因为格式可能不好。
1.爬取页面，导出html，然后在放在hexo中，目录为/source/\_post/，直接放html文件，然后设置layout：false，那么hexo会忽略对html的编译，在浏览时直接超链接到html文件
2.将html文件再用程序转换为markdown
3.直接用代码爬取页面然后生成markdown文件

第1种方法可能会遇到html文件中格式不支持的情况，没得到解决；
第2种方法发现在线转换效果也不好，就寻求代码解决，github上有一段[程序](https://github.com/baizhebz/html2markdown4blog)，作者说可行，不过我环境没搭成功，不懂php，更何况要装curl（这个之前做android时NDK开发时也很难配置），后来用第3种方法就直接写python爬虫程序，参考github的一段[程序](https://github.com/kesalin/PythonSnippet/blob/master/ExportCSDNBlog.py)，不过程序有些问题，也有些不符合如今CSDN的布局，所以我大改了一下，转为markdown的那一部分程序脉络是差不多的，这个也是最关键的部分，直接影响到markdown的显示，不过我也做得不太好。

### 2、程序说明
所需安装库：
BeautifulSoup
根据版本不同可能要改动相应的代码，一般不用改。
