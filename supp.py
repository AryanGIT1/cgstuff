# import requests
# from bs4 import BeautifulSoup
from hashlib import sha256
# import time
from gtts import gTTS
import os


def SHA256(text):
    return str(sha256(text.encode("ascii")).hexdigest())


# def get_soup(url):
#     r = requests.get(url)
    
#     html = r.text
#     soup = BeautifulSoup(html, "html5lib")
#     return soup


# def get_data_toi():
#     url = 'https://timesofindia.indiatimes.com/'
    
#     soup = get_soup(url)
    
#     x = soup.find_all('figcaption')[0:30]
#     links = soup.find_all('a', class_ = '_3SqZy')[0:30]
    
#     vals = []
#     pos = []
    
#     for i in range(0,30):
#         soup = get_soup(links[i]['href'])
#         z = soup.find()
#         if z == None:
#             pos.append(i)
#         else:
#             vals.append(z)
                
#     count = 0
    
#     for i in range(len(pos)):
#         x.pop(pos[i] - count)
#         links.pop(pos[i] - count)
#         count += 1

#     #headline of all articles
    
#     for i in range(len(x)):
#         print(x[i].get_text())
#         print(links[i]['href'])
#         print(vals[i])
#         print("")
    
# def get_data_hidustan_times():
#     url = 'https://www.hindustantimes.com/india-news'
    
#     soup = get_soup(url)
#     print(soup)
#     y = soup.find_all('div', class_ = 'htImpressionTracking')
#     x = soup.find_all('a', class_ = 'cartHolder listView track ')
    
#     links = soup.find('a')
#     print(x,y,links)
    
def text_to_voice(blog):
    text = "Title " + str(blog.title) + ", Author" + str(blog.author) + ". Description: " + str(blog.desc)
    language = 'en' 
    myobj = gTTS(text = text, lang = language, slow = False)
    myobj.save("news.mp3")
    return "news.mp3"
    
if __name__ == '__main__':
    # start = time.time()
    # print("Import Works!!")
    # get_data_toi()
    # get_data_hidustan_times()
    # end = time.time()
    # print("\n"+ str(end - start))
    text_to_voice("There are several APIs available to convert text to speech in Python. One of such APIs is the Google Text to Speech API commonly known as the gTTS API. gTTS is a very easy to use tool which converts the text entered, into audio which can be saved as a mp3 file")
    print("Working!")