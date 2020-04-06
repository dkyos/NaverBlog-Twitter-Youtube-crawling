#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import urllib
import time
import pandas as pd
import re
from pandas import DataFrame, Series
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver as wd
from selenium.webdriver.common.keys import Keys
import GetOldTweets3 as got
import datetime
from random import uniform
from tqdm import tqdm_notebook

# Ref: https://jeongwookie.github.io/2019/06/10/190610-twitter-data-crawling/

def crawling():

    keyword = input('Keyword : ')

    # 가져올 범위를 정의
    # 예제 : 2019-04-21 ~ 2019-04-24
    days_range = []

    start = datetime.datetime.strptime("2020-03-01", "%Y-%m-%d")
    end = datetime.datetime.strptime("2020-03-10", "%Y-%m-%d")
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]

    for date in date_generated:
        days_range.append(date.strftime("%Y-%m-%d"))

    print("=== 설정된 트윗 수집 기간은 {} 에서 {} 까지 입니다 ===".format(days_range[0], days_range[-1]))
    print("=== 총 {}일 간의 데이터 수집 ===".format(len(days_range)))
    print(""*3)

    # 특정 검색어가 포함된 트윗 검색하기 (quary search)

    # 수집 기간 맞추기
    for i in range(len(days_range)):
        start_date = days_range[i]
        end_date = (datetime.datetime.strptime(days_range[i], "%Y-%m-%d") 
            + datetime.timedelta(days=1)).strftime("%Y-%m-%d") # setUntil이 끝을 포함하지 않으므로, day + 1

        print("=== 트윗 수집 기간은 {} 에서 {} 까지 ===".format(start_date, end_date))

        # 트윗 수집 기준 정의
        tweetCriteria = got.manager.TweetCriteria().setQuerySearch(keyword)\
            .setSince(start_date)\
            .setUntil(end_date)\
            .setMaxTweets(-1)

        # 수집 with GetOldTweet3
        print("Collecting data start.. from {} to {}".format(start_date, end_date))
        start_time = time.time()

        tweet = got.manager.TweetManager.getTweets(tweetCriteria)

        print("Collecting data end.. {0:0.2f} Minutes".format((time.time() - start_time)/60))
        print("=== Total num of tweets is {} ===".format(len(tweet)))

        # initialize
        tweet_list = []

        # 원하는 변수 골라서 저장하기
        for index in tqdm_notebook(tweet):
            # 메타데이터 목록 
            username = index.username
            link = index.permalink 
            content = index.text
            tweet_date = index.date.strftime("%Y-%m-%d")
            tweet_time = index.date.strftime("%H:%M:%S")
            retweets = index.retweets
            favorites = index.favorites
            # 결과 합치기
            info_list = [tweet_date, tweet_time, username, content, link, retweets, favorites] 
            #print(info_list)

            tweet_list.append(info_list)

        print('The data is being written to the csv file.')
        dataframe = pd.DataFrame(tweet_list, columns=["date", "time", "username", "content", "link", "retweets", "favorites"] )
        dataframe.to_csv('../data/twitter_comment.csv', mode = 'a', index = False)


    print('Finish working')


    '''
    TWITTER_URL = 'https://twitter.com/search?l=&q='

    data = []
    keyword = input('Keyword : ')

    driver = wd.Chrome('./tool/chromedriver.exe')
    driver.maximize_window()

    driver.get(TWITTER_URL + keyword)

    print('The scroll is starting to move bottom')

    # 페이지 스크롤을 끝날 때까지 계속 내림
    # 스크롤을 내리기 전의 화면 높이와 내렸을 때의 화면 높이가 같다면 더 이상 내려갈 곳이 없다는 의미이므로 무한 루프를 탈출함.
    last_height = driver.execute_script("return document.body.scrollHeight")
    print('height: ' + str(last_height))
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(1)
        new_height = driver.execute_script("return document.body.scrollHeight")
        print('height: ' + str(new_height))
        
        if new_height == last_height:
            # Wait to load page
            time.sleep(1)
            new_height = driver.execute_script("return document.body.scrollHeight")
            
            if(new_height == last_height):
                break
        break
        last_height = new_height
    print('Arrived at the end of the page')
    print('Start twitter crawling')
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # 트위터의 게시글에는 각각의 고유의 아이디가 있어서 트위터 사이트에서 모든 게시글 아이디를 리스트형으로 가져옴
    pattern = re.compile('stream-item-tweet-\d+')
    items = pattern.findall(str(soup))
    print(items)
    print(len(items))
    for item in items:
        # 위에서 가져온 고유 아이디를 이용하여 게시글 본문을 css selector를 이용하여 가져
        text = driver.find_element_by_css_selector('#'+ item +' > div > div.content > div.js-tweet-text-container > p').text

        # 특수기호를 없애는 작
        for idx in range(len(text)):
            if not ((0 <= ord(text[idx]) < 128) or (0xac00 <= ord(text[idx]) <= 0xd7af)):
                text = text.replace(text[idx], ' ')

        print(text)
        data.append(text)

    driver.close()
    
    print('Finish crawling')
    print('The data is being written to the csv file.')
    dataframe = pd.DataFrame(data, columns=["content"])
    dataframe.to_csv('../data/twitter_comment.csv', mode = 'a')
    print('Finish working')
    '''
    
