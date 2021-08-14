# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from google_trans_new import google_translator 
import csv
from pprint import pprint
import os
import pandas as pd

from googleapiclient.discovery import build

api_key= #Get your API key
service_name='youtube'
api_version='v3'
part_string="id, contentDetails, statistics, snippet, topicDetails"
#video_ids=["rPNk74BqW2I"]
def youtube_search(video_ids, file_num):
    data=[]
    youtube=build(service_name, api_version, developerKey=api_key)
    # csvFile=open("video_results_"+str(file_num)+".csv", "w")
    # csvWriter=csv.writer(csvFile)
    
    # csvWriter.writerow(["title", "videoID", "etag", "publishedAt", "ChannelId", "description", 
    #                     "viewCount", "likeCount", "disLikeCout", "commentCount", "favoriteCount"])
    
    for v in video_ids:
        print("video id", v)
        video_response=youtube.videos().list(id=v, part="id, snippet, statistics").execute()

 
        if(len(video_response['items'])>0):  
            print(video_response['items'][0]['statistics'])
    
            videoId=video_response['items'][0]["id"]
            etag=video_response['items'][0]['etag']
            publishedAt=video_response['items'][0]['snippet']['publishedAt']
            channelId=video_response['items'][0]['snippet']['channelId']
            if ('viewCount' in video_response['items'][0]['statistics']):
                viewCount=int(video_response['items'][0]['statistics']['viewCount'])
            else:
                viewCount=0
            if ('likeCount' in video_response['items'][0]['statistics']):
                likeCount=int(video_response['items'][0]['statistics']['likeCount'])
            else:
                likeCount=0
            if ('dislikeCount' in video_response['items'][0]['statistics']):
                disLikeCount=int(video_response['items'][0]['statistics']['dislikeCount'])
            else:
                disLikeCount=0
            if ('commentCount' in video_response['items'][0]['statistics']):
                commentCount=int(video_response['items'][0]['statistics']['commentCount'])
            else:
                commentCount=0
            if ('favoriteCount' in video_response['items'][0]['statistics']):
                favoriteCount=int(video_response['items'][0]['statistics']['favoriteCount'])
            else:
                favoriteCount=0
                
            
            detector = google_translator() 
            translator = google_translator()
            
            title=video_response['items'][0]["snippet"]["title"]
            lang="en"
            try:
                detect_title = detector.detect(title)
                print("title language", detect_title)
                lang=detect_title[0]
                if(detect_title[0]!='en'):
                    title = translator.translate(title, lang_tgt='en')  
                    # title=unidecode.unidecode(translate_title)
                else:
                    title=video_response['items'][0]["snippet"]["title"]
            except:
                title=video_response['items'][0]["snippet"]["title"]
                
                
            desc=video_response['items'][0]["snippet"]["description"]
            
            if(len(desc)>0):
                try:           
                    detect_desc = detector.detect(desc)
    
                    if(detect_desc[0]!='en'):
                        desc = translator.translate(desc,lang_tgt='en')  
                        # desc=unidecode.unidecode(translate_desc)
                    else:
                        desc=video_response['items'][0]["snippet"]["description"]
                except:
                    desc=video_response['items'][0]["snippet"]["description"]
                
            data.append({"videoId":videoId, "etag":etag, "title":title, "language":lang, 
                         "description":desc, "publishedAt":publishedAt, 'channelId':channelId,
                         "viewCount": viewCount, "likeCount":likeCount, 
                         "dislikeCount":disLikeCount, "commentCount":commentCount, 
                         "favoriteCount":favoriteCount})
                
            # csvWriter.writerow([translate_title, videoId, etag, publishedAt, channelId, translate_desc, 
            #            viewCount, likeCount, disLikeCount, commentCount, favoriteCount])
    
            # csvWriter.writerow(["title", "videoID", "etag", "publishedAt", "ChannelId", "description", 
            #                 "viewCount", "likeCount", "disLikeCout", "commentCount", "favoriteCount"])
            # pprint([translate_title, videoId, etag, publishedAt, channelId, translate_desc, 
            #            viewCount, likeCount, disLikeCount, commentCount, favoriteCount])
    df=pd.DataFrame().from_dict(data)
	
	#To save the data in csv format 
    df.to_csv("C:/RESEARCH/Datasets/Christina/Videos/"+str(file_num)+".csv")


if __name__== "__main__":
	
	#populate video ids extrcated from the CSV files
    video_ids=['uretrfMA-Io']
    
    youtube_search(video_ids, "amber")
    # index=0

    # path="C:/RESEARCH/Datasets/WH_YouTube/videos_list"
    # file_list=[]
    # for root, dirs, files in os.walk(path):
    #     for f in files:
    #         file_list.append(f)
    # # print(file_list[index].split('_')[1].split('.')[0])
    # while(index<len(file_list)):
    #     videos_df=pd.read_csv(os.path.join(path, file_list[index]))
    #     vids=videos_df.iloc[0:, 0]
    #     video_ids=[i for i in vids if i!='#NAME?']
    #     print(file_list[index].split('_')[1].split('.')[0])
    #     youtube_search(video_ids, int(file_list[index].split('_')[1].split('.')[0]))
    #     index+=1
                    