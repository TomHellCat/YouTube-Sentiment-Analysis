import requests
from bs4 import BeautifulSoup
import re
from textblob import TextBlob

class YoutubeClient(object):

    def __init__(self,keyword):
        self.keyword = keyword
        self.url_list = []
        self.title_list = []
        self.total_views = 0
        self.likes = 0
        self.dislikes = 0
        self.videos_analysed = 0
        self.favourability = 0
        self.unfavourability = 0

    def get_url(self):
        self.search_term = self.keyword
        search_term = re.sub(r"[^a-zA-Z0-9]+", ' ', self.keyword)
        search_term = search_term.replace(" ","+")
        self.url = 'https://www.youtube.com/results?search_query=' + search_term

    def get_search_results(self):
        markup = requests.get(self.url).text
        soup = BeautifulSoup(markup,'html.parser')
        url = 'https://www.youtube.com'
        links = soup.findAll('a',{"class":"yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2 yt-uix-sessionlink spf-link"})
        for link in links:
            url = url + link.get('href')
            self.url_list.append(url)
            self.title_list.append(link.contents)
            url = 'https://www.youtube.com'
            
    def print_url_list(self):
        for i in range(1,len(self.url_list)):
            print(self.title_list[i])
            print(self.url_list[i])

    def analyse(self):
        self.videos_analysed = len(self.url_list)
        for i in range(1,len(self.url_list)):
            self.likes = '0'
            self.dislikes = '0'
            text = self.title_list[i][0]
            text =  ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", text).split())
            analysis = TextBlob(text) 
           
            markup = requests.get(self.url_list[i]).text
            soup = BeautifulSoup(markup,'html.parser')
            links = soup.findAll('button',{ "title":"I dislike this"})
            likes =  soup.findAll('button',{ "title":"I like this"})
            views = soup.findAll('div',{ "class":"watch-view-count"})
            
            if(len(views) > 0):
                v = re.sub(r"[^0-9]+",'',views[0].contents[0])
                self.total_views += int(v)
                
            else:
                print("views info not available this must be a live video")
            if(len(links) > 0):
                span = links[0].findAll('span')
                if(len(span) > 0):
                    self.dislikes += span[0].contents[0]
                else:
                    print("Dislikes not available")
            else:
                print("Some infos aren't available")
            
            if(len(likes) > 0):
                like_span = likes[0].findAll('span')
                if(len(like_span) > 0):
                    self.likes += like_span[0].contents[0]
                else:
                    print("Info not available")
            else:
                print("Some infos aren't available")

            if analysis.sentiment.polarity > 0: 
                #print('positive')
                self.favourability += int(re.sub(r"[^0-9]+",'',self.likes))
                self.unfavourability += int(re.sub(r"[^0-9]+",'',self.dislikes))
            elif analysis.sentiment.polarity == 0: 
                self.favourability += int(re.sub(r"[^0-9]+",'',self.likes))
                self.unfavourability += int(re.sub(r"[^0-9]+",'',self.dislikes))
            else: 
                self.unfavourability += int(re.sub(r"[^0-9]+",'',self.dislikes))
                self.favourability += int(re.sub(r"[^0-9]+",'',self.likes))
                
            pub = soup.findAll('strong',{ "class":"watch-time-text"})
            if(len(pub) > 0):
                print("Time: ",pub[0].contents)
            else:
                print("Info not available")
                

