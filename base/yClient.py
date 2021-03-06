import os
from bs4 import BeautifulSoup
import requests
import json
import googleapiclient.discovery
from datetime import datetime, timedelta
import re
from textblob import TextBlob
import matplotlib.pyplot as plt 
from .flair_nlp import find_tags

class VideoInfo(object):

    def __init__(self, title, date, DEVELOPER_KEY, video_id,keyword):
        self.title = title
        self.date = date[:7]
        self.getStats(DEVELOPER_KEY, video_id)
        self.formatTitle()
        self.getSentiment()
        self.getTags(keyword)

    def getStats(self, DEVELOPER_KEY, video_id):
        url = f"https://www.googleapis.com/youtube/v3/videos?part=statistics&id={video_id}&key={DEVELOPER_KEY}"
        json_url = requests.get(url)
        data = json_url.json()  
        #print(data)     
        items = data['items']
        #print(items)
        """self.views = items[0]['statistics']['viewCount']
        self.likes = items[0]['statistics']['likeCount']
        self.dislikes = items[0]['statistics']['dislikeCount']"""
        if(items[0]['statistics'].get('viewCount')):
            self.views = items[0]['statistics'].get('viewCount')
        else:
            self.views = 0
        if(items[0]['statistics'].get('likeCount')):
            self.likes = items[0]['statistics'].get('likeCount')
        else:
            self.likes = 0
        if(items[0]['statistics'].get('dislikeCount')):
            self.dislikes = items[0]['statistics'].get('dislikeCount')
        else:
            self.dislikes = 0
        """print(self.views)
        print(self.likes)
        print(self.dislikes)"""

    def formatTitle(self):
        self.title = self.title.replace("&quot;", "\"")
        self.title = self.title.replace("&#39;", "'")
        self.title = re.sub(r'[^a-zA-Z0-9 ]',"",self.title)


    def getSentiment(self):
        text = self.title
        #print("text: ", text.encode("utf-8"))
        #text =  ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", text).split())
        #print(text)
        self.analysis = TextBlob(text)
        analysis = self.analysis.sentiment.polarity
        if(analysis >= 0):
            self.analysis = True
        else:
            self.analysis = False

    def getTags(self,keyword):
        #print(self.title)
        self.tags = find_tags(self.title,keyword)
        #print(self.tags)


class YouTubeClient(object):

    def __init__(self,keyword):

        self.initialize(keyword)
        self.createVideoObject(keyword)
        """self.createVideoObject(keyword)
        self.getTotalStats()
        self.mlist = self.monthlist_fast(self.months[0],self.months[len(self.months)-1])
        self.y1 = self.get_Y_Axis(self.mlist, self.fav_m)
        self.y2 = self.get_Y_Axis(self.mlist, self.unfav_m)
        #self.plot2(mlist,self.y1,self.y2)"""


    def createVideoObject(self,keyword):
        self.videoList = []
        #self.months = []
        #tags = []
        for _ in self.response['items']:
            video_id = _['id']['videoId']
            date = _['snippet']['publishedAt']
            title = _['snippet']['title']
            #print(video_id," ", date, " ", title)
            videoStats = VideoInfo(title,date,self.DEVELOPER_KEY,video_id,keyword)
            self.videoList.append(videoStats)
            #print(videoStats.tags)
            """for _ in videoStats.tags:
                tags.append(_)
        
        self.tags = [i for n, i in enumerate(tags) if i not in tags[:n]]""" 
        

    def strToDate(self,str):
        format = "%Y-%m-%d"
        date = datetime.strptime(str,format)
        return date


    def getTotalStats(self):
        self.views = 0
        self.likes = 0
        self.dislikes = 0
        self.positive = 0
        self.negative = 0
        self.fav_likes = 0
        self.fav_dislikes = 0
        self.unfav_likes = 0
        self.unfav_dislikes = 0
        self.fav_views = 0
        self.unfav_views = 0
        self.fav_m = []
        self.unfav_m = []

        for video in self.videoList:
            self.views += int(video.views)
            self.likes += int(video.likes)
            self.dislikes += int(video.dislikes)
            self.months.append(self.strToDate(video.date))
            if(video.analysis.sentiment.polarity >= 0):
                self.positive += 1
                self.fav_likes += int(video.likes)
                self.fav_dislikes += int(video.dislikes)
                self.fav_views += int(video.views)
                self.fav_m.append(self.strToDate(video.date))
            else:
                self.negative += 1
                self.unfav_likes += int(video.likes)
                self.unfav_dislikes += int(video.dislikes)
                self.unfav_views += int(video.views)
                self.unfav_m.append(self.strToDate(video.date))

        """print("Total views: ", self.views)
        print("Total likes: ", self.likes)
        print("Total dislikes: ", self.dislikes)
        print("Total positive: ", self.positive)
        print("Total negative: ", self.negative)"""
        self.months = sorted(self.months)
        #print(self.months)

    def monthlist_fast(self,start,end):
        #start, end = [datetime.strptime(_, "%d %b %Y") for _ in dates]
        total_months = lambda dt: dt.month + 12 * dt.year
        mlist = []
        for tot_m in range(total_months(start)-1, total_months(end)):
            y, m = divmod(tot_m, 12)
            mlist.append(datetime(y, m+1, 1).strftime("%Y-%m"))

        return mlist

    def get_Y_Axis(self,mlist,months):
        y = [0] * len(mlist)
        for i in range(len(months)):
            for j in range(len(mlist)):
                if(months[i].strftime("%Y-%m") == mlist[j]):
                    y[j]+=1
        return y


    def initialize(self,keyword):
        self.keyword = keyword
        api_service_name = "youtube"
        api_version = "v3"
        self.DEVELOPER_KEY = "AIzaSyBc-5LCpZtOmjgU7IPDs_Xa8ulAH3iLnGo"

        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey = self.DEVELOPER_KEY)

        request = youtube.search().list(q=self.keyword, part='snippet',type='video', maxResults=50)
        self.response = request.execute()

    def plot2(self,x,y1,y2):
        plt.plot(x,y1,"g")
        plt.plot(x,y2,"r")
        plt.xlabel('Months') 
        plt.ylabel('Videos Published') 
        plt.title('Timeline of Videos Published') 
        plt.show()

def main():
   Yclient = YouTubeClient("Andrew Yang")
   print(type(Yclient.videoList[0].date))
   for _ in Yclient.videoList:
       #print(_.title," ",_.date, " ",_.views," ",_.dislikes, " ",_.likes)   
       #print(_.analysis)
       print(_.tags)
       print(_.date)   


if __name__ == "__main__":
    main()