from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.base import JobLookupError
import requests
import datetime
import maya
import feedparser

import google_news_dbmanager

class GoogleNewsCron():
    def __init__(self):
        print ('크론 시작')
        self.scheduler = BackgroundScheduler(job_defaults={'max_instances': 10, 'coalesce': False})
        self.scheduler.start()
        self.dbManager = google_news_dbmanager.GoogleNewsDBManager()
        self.country = 'ko'
        self.keyword = ''

    def __del__(self): 
        self.stop()

    def exec(self):
        print ('Google News Cron Start: ' + datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
        URL = 'https://news.google.com/rss/search?q={}+when:1d'.format(self.keyword)
        if self.country == 'en':
            URL += '&hl=en-NG&gl=NG&ceid=NG:en'
        elif self.country == 'ko':
            URL += '&hl=ko&gl=KR&ceid=KR:ko'

        try: 
            self.dbManager.queryCreateGoogleNewsTable(self.keyword)
            res = requests.get(URL)
            if res.status_code == 200:
                datas = feedparser.parse(res.text).entries
                for data in datas:
                    data['published'] = maya.parse(data.published).datetime(to_timezone="Asia/Seoul", naive=True) 
                    data['source'] = data.source.title
                    self.dbManager.queryInsertGoogleNewsTable(data)
            else:
                print ('Google 검색 에러')
        except requests.exceptions.RequestException as err:
            print ('Error Requests: {}'.format(err))
    
    def run(self, mode, country, keyword):
        print ("실행!")
        self.country = country
        self.keyword = keyword
        if mode == 'once':
            self.scheduler.add_job(self.exec)
        elif mode == 'interval':
            self.scheduler.add_job(self.exec, 'interval', seconds=10)
        elif mode == 'cron':
            self.scheduler.add_job(self.exec, 'cron', second='*/10')

    def stop(self):
        try: self.scheduler.shutdown() 
        except: pass
        try: self.dbManager.close() 
        except: pass
