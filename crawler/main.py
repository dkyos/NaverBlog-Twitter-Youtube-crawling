#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import naver_crawler
import youtube_crawler
import twitter_crawler

MAX_MENU = 5
NAVER_CRAWLING = 1
TWITTER_CRAWLING = 2
YOUTUBE_CRAWLING = 3
YOUTUBE_URL_CRAWLING = 4
YOUTUBE_COMMENT_CRAWLING = 5

def menu():
    print('Crawling Program >> Please select menu')
    print('=======================================')
    print('1. Naver Blog Crawling')
    print('2. Twitter Crawling')
    print('3. Youtube Crawling')
    print('4. Youtube URL Crawling')
    print('5. Youtube Comment Crawling (need 4)')
    print('=======================================')
    
if __name__ == "__main__":

    menu()
    try:
        menu_num = int(input('Menu : '))
    except :
        print('Please press valid menu number')
        sys.exit(1)
    if(not( 1 <= menu_num <= MAX_MENU )):
        print('Please press valid menu number (1~3)')
        sys.exit(1)


    if(menu_num == NAVER_CRAWLING):
        naver_crawler.crawling()

    elif(menu_num == TWITTER_CRAWLING):
        twitter_crawler.crawling()
        
    elif(menu_num == YOUTUBE_CRAWLING):
        youtube_crawler.video_url_crawling()
        youtube_crawler.video_comment_crawling()

    elif(menu_num == YOUTUBE_URL_CRAWLING):
        youtube_crawler.video_url_crawling()
    
    elif(menu_num == YOUTUBE_COMMENT_CRAWLING):
        youtube_crawler.video_comment_crawling()

