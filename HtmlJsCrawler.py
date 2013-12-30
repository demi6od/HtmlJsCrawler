#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import os
import sys
from bs4 import BeautifulSoup
import re
import urllib2

HTML_FILE_DIR = os.getcwd() + "\\crawlHtml\\"
JS_FILE_DIR = os.getcwd() + "\\crawlJs\\"

IS_CRAWL_HTML = True
IS_CRAWL_JS = True

TIME_OUT = 2

gHtmlCntMax = 0
gJsCntMax = 0
gHtmlCnt = 0 
gJsCnt = 0 

gHtmlIdx = 0 
gJsIdx = 0 

gHtmlList = []
gJsList = []


def writeFile(url, fileType):
    try:
        global gHtmlIdx
        global gJsIdx
        global gHtmlCnt 
        global gJsCnt 

        page = urllib2.urlopen(url, timeout = TIME_OUT)
        src = page.read()
        if fileType == "html":
            output = open(HTML_FILE_DIR + str(gHtmlIdx) +".html", "w")
            gHtmlIdx += 1
            gHtmlCnt += 1
        elif fileType == "js":
            output = open(JS_FILE_DIR + str(gJsIdx) +".js", "w")
            gJsIdx += 1
            gJsCnt += 1
        else:
            print "[-] WriteFile else"
        output.write(src)
        output.close()

    except Exception,data:
        print "[-] Write file exception"
        print Exception,":",data


def crawl(url, deep):
    try:
        html = urllib2.urlopen(url, timeout = TIME_OUT)
        src = html.read()
        soup = BeautifulSoup(src)

        if gJsCnt < gJsCntMax:
            scripts = soup.findAll("script", src=re.compile(".js"))
            for tag in scripts:
                jsHref = tag.get("src", )
                if jsHref:
                    if not re.match(r'http://', jsHref):
                        jsHref = url + jsHref 
                    if not jsHref in gJsList:
                        gJsList.append(jsHref)
                        writeFile(jsHref, "js")

        anchors = soup.findAll("a")
        for tag in anchors:
            href = tag.get("href")
            if href:
                href = href.split("?")[0].split("#")[0].split("javascript:")[0]
                if len(href) > 0 and href[len(href)-1] == '/':
                    href = href[:-1]
                if not re.match(r'http://', href):
                    href = url + href
                if not href in gHtmlList:
                    print "[+] " + href.encode('utf-8')
                    gHtmlList.append(href)
                    if gHtmlCnt < gHtmlCntMax:
                        writeFile(href, "html")
                    if deep > 0 and (gHtmlCnt < gHtmlCntMax or gJsCnt < gJsCntMax) :
                        crawl(href, deep-1)
    except Exception,data:
        print "[-] Crawl exception"
        print Exception,":",data


def main():
    print "[+] Start"

    global gHtmlCntMax
    global gJsCntMax 
    global gHtmlCnt 
    global gJsCnt 

    crawlList = open("crawlList.txt")
    while True:
        line = crawlList.readline()
        if not line:
            break

        tokens = line.split(",")
        if tokens[0][0] == '#':
            continue

        url = tokens[0].strip()
        recDeep= int(tokens[1].strip())
        gHtmlCntMax = int(tokens[2].strip())
        gJsCntMax = int(tokens[2].strip())

        print "[+] Url: " + url + ", recursive deep: " + str(recDeep) \
            + ", html count: " + str(gHtmlCntMax) + ", js count: " + str(gJsCntMax)

        gHtmlCnt = 0 
        gJsCnt = 0 

        gHtmlList.append(url)
        crawl(url, recDeep)

    print "[+] Finish"
        
if __name__ == "__main__":
    main()
		
