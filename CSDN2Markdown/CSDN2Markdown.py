#! /usr/bin/env python
#coding=utf-8
import urllib2
from bs4 import BeautifulSoup
import logging
import re
import threading
import traceback
import time 
import datetime

import sys
reload(sys)
sys.setdefaultencoding('gb18030')


# global variable
blog = "http://blog.csdn.net"
url = "http://blog.csdn.net/gugugujiawei?viewmode=contents"
outputDir = 'F:\\linux\\Share\\github\\article\\'
gRetryCount = 4


def decodeHtmlSpecialCharacter(htmlStr):
    specChars = {"&ensp;" : "", \
                 "&emsp;" : "", \
                 "&nbsp;" : "", \
                 "&lt;" : "<", \
                 "&gt" : ">", \
                 "&amp;" : "&", \
                 "&quot;" : "\"", \
                 "&copy;" : "®", \
                 "&times;" : "×", \
                 "&divide;" : "÷", \
                 }
    for key in specChars.keys():
        htmlStr = htmlStr.replace(key, specChars[key])
    return htmlStr

def repalceInvalidCharInFilename(filename):
    specChars = {"\\" : "", \
                 "/" : "", \
                 ":" : "", \
                 "*" : "", \
                 "?" : "", \
                 "\"" : "", \
                 "<" : "小于", \
                 ">" : "大于", \
                 "|" : " and ", \
                 "&" :" or ", \
                 }
    for key in specChars.keys():
        filename = filename.replace(key, specChars[key])
    return filename


def getPageUrlList(url):
    
    global blog
    
    #获取所有的页面的 url
    user_agent = 'Mozilla/4.0 (compatible;  MSIE 5.5; Windows NT)'  
    header = { 'User-Agent' : user_agent } 

    request = urllib2.Request(url, None, header)
    response = urllib2.urlopen(request)
    data = response.read()

    #print data
    soup = BeautifulSoup(data)
    pageListDocs = soup.find_all(id="article_list")
    
    # artclie----{url:title}
    articleUrlTitle = {}
    
    #print len(pageListDocs)
    
    for pageList in pageListDocs:
        
        h1List = pageList.find_all('h1')
        
        for articleList in h1List:            
        
            hrefDocs = articleList.find_all("a")
        
        
            if len(hrefDocs) > 0:
                articleHrefDoc = hrefDocs[0]                            
                
                #print "hello",articleHrefDoc
                articleUrl =  blog + articleHrefDoc["href"]
                articleTitle = articleHrefDoc.text
                articleUrlTitle[articleUrl] = articleTitle

    print 'the count of articles is',len(articleUrlTitle)
    '''
    for s in articleUrlTitle:
        print s,'--',articleUrlTitle[s]
    '''
    return articleUrlTitle


def download(url, title):
    # 下载文章，并保存为 markdown 格式
    logging.info(" >> download: " + url)
    print 'downloading the article',title

    data = None
    title = '"' + title + '"'
    categories = ""
    content = ""
    #postDate = datetime.datetime.now()

    global gRetryCount
    count = 0
    while True:
        if count >= gRetryCount:
            break
        count = count + 1
        try:            
            time.sleep(2.0) #访问太快会不响应
            user_agent = 'Mozilla/4.0 (compatible;  MSIE 5.5; Windows NT)'  
            header = { 'User-Agent' : user_agent }    
            request = urllib2.Request(url, None, header)
            response = urllib2.urlopen(request)            
            data = response.read()
            break
        except Exception,e:
            exstr = traceback.format_exc()
            logging.info(" >> failed to download " + url + ", retry: " + str(count) + ", error:" + exstr)
            pass

    if data == None:
        logging.info(" >> failed to download " + url)
        return

    #print data
    
    soup = BeautifulSoup(data)

    #date=link_postdate


    manageDocs = soup.find_all("div", "article_manage")
    for managerDoc in manageDocs:
        categoryDoc = managerDoc.find_all("span", "link_categories")
        if len(categoryDoc) > 0:                            
            categories = categoryDoc[0].a.get_text().encode('UTF-8').strip()
            categories  = categories.decode('utf-8').encode('gb2312')            

        postDateDoc = managerDoc.find_all("span", "link_postdate")
        if len(postDateDoc) > 0:
            postDateStr = postDateDoc[0].string.encode('UTF-8').strip()
            postDate = datetime.datetime.strptime(postDateStr, '%Y-%m-%d %H:%M')
            print 'date',postDate

    contentDocs = soup.find_all(id="article_content")
    for contentDoc in contentDocs:
        htmlContent = contentDoc.prettify().encode('UTF-8')
        #print htmlContent
        #file = open('F:\\linux\\Share\\github\\out2.txt','a+')
        #file.write(htmlContent)        
        content = htmlContent2String(htmlContent)
        
    exportToMarkdown(outputDir, postDate, categories, title, content)

# htmlContent2String 是整个程序的关键，用于将html转换为markdown格式
def htmlContent2String(contentStr):
    
    # 因为格式中可能会有点乱，换行符乱入，所以用[\s\S]匹配任何字符，包括换行符，注意其中的？是为了去除贪婪匹配
    # <img src="http://img.blog.csdn.net/20150118194525562" align="middle" width="400 height="300" alt=""> 
    # 图片链接   
    patternImg = re.compile(r'(<img[\s\S]+?src=")([\s\S]+?)("[\s\S]+?>)')    
    
    # <a target="_blank" href="http://blog.csdn.net/gugugujiawei/article/details/42558411">博文</a>
    # 文字链接
    patternHref = re.compile(r'(<a[\s\S]+?href=")([\s\S]*?)("[\s\S]*?>)([\s\S]+?)(</a>)')
    
    # 去除html各种标签，这里的？则是指匹配0次或1次
    patternRemoveHtml = re.compile(r'</?[^>]+>')

    resultContent = patternImg.sub(r'![image_mark](\2)', contentStr)
    resultContent = patternHref.sub(r'[\4](\2)', resultContent)
    resultContent = re.sub(patternRemoveHtml, r'', resultContent)
    resultContent = decodeHtmlSpecialCharacter(resultContent)
    
    #file = open('F:\\linux\\Share\\github\\out3.txt','a+')
    #file.write(resultContent)
        
    return resultContent




def exportToMarkdown(exportDir, postdate, categories, title, content):
    titleDate = postdate.strftime('%Y-%m')
    contentDate = postdate.strftime('%Y-%m-%d %H:%M:%S %z')
    filename = title
    filename = repalceInvalidCharInFilename(filename)
    filepath = exportDir + filename + '.txt'

    #newFile = open(unicode(filepath, "utf8"), 'w') 
    newFile = open(filepath,'a+')
    
    # 根据自己需要选择去留注释,这里categores和tag用了一样的
    
    # newFile.write('---' + '\n')
    # newFile.write('layout: post' + '\n')    
    newFile.write('title: ' + title + '\n')
    newFile.write('date: ' + contentDate + '\n')
    # newFile.write('comments: true' + '\n')
    newFile.write('categories: [' + categories + ']' + '\n')
    newFile.write('tags: [' + categories + ']' + '\n')
    
    #newFile.write('description:' + title + '\n')
    # newFile.write('keywords: ' + categories + '\n')
    
    newFile.write('---' + '\n\n')
    
    
    content = content.decode('utf-8').encode('gb18030')
    #print content
    newFile.write(content)
    newFile.write('\n')
    newFile.close()



if __name__ == "__main__":
    
    global url    
    articleUrlTitle = getPageUrlList(url)
    
    '''
    for s in articleUrlTitle:
        print s,'--',articleUrlTitle[s]
    '''
    
    #multithread download
    threads = []
    for url in articleUrlTitle:
        patternTitle = re.compile('\r\n *(.+) *\r\n')
        title = patternTitle.sub(r'\1',articleUrlTitle[url])
        # print 'title',title
        t = threading.Thread(target = download,args = (url,title))    
        t.start()
        threads.append(t)
        
            
    for i in threads:
        i.join()
    
    print "success"
    
    

