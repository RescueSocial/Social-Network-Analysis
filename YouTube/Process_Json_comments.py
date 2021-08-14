# -*- coding: utf-8 -*-
"""
Created on Sun Jun 20 12:40:13 2021

@author: nacho
"""

import json
import os
import pandas as pd
from google_trans_new import google_translator 

start_video_index=1

while start_video_index<125: #total number of videos

    filelist=[]
    allvideos=[]
    ind=1
	#get the video ids from the csv (path to the list of videos)
    path="C:/RESEARCH/Datasets/WH_YouTube/video_details/"
    for root, dirs, files in os.walk(path):
        for f in files:
            if f.endswith("csv"):
                filelist.append(f)
    while(ind<len(filelist)):
        videos_df=pd.read_csv(os.path.join(path, filelist[ind]))
        vids=videos_df.iloc[0:, 1]
        allvideos.extend([i for i in vids if i!='#NAME?'])
        ind+=1
            
    # print((set(ids1).intersection(set(ids2))).intersection(set(ids3)))
        # for i in range(len(data['items'])):
        #     print(data['items'][i].keys())
        # for p in data['items']:
        #     print('Name: ' + p['name'])
        #     print('Website: ' + p['website'])
        #     print('From: ' + p['from'])
        #     print('')
        
    
        
    path="C:/RESEARCH/Datasets/WH_YouTube/comment_thread_jsons/video"+str(start_video_index)+"/"  #Path to the JSON files with comments
    list_of_files=[]
    for root, dirs, files in os.walk(path):
        for f in files:
            list_of_files.append(f)
    
    print("processing for video %d"%start_video_index )
    print("Number of files: %d"%len(list_of_files))
    
    
    comments=[]
    replies=[]
    # sample_file=list_of_files[0]
    for f in list_of_files:
        with open(os.path.join(path, f)) as json_file:
                data = json.load(json_file)
                print(f, len(data['items']))
                for i in range(len(data['items'])):
                    Id=data['items'][i]['id']
            
                    commentId=data['items'][i]['snippet']['topLevelComment']['id']
                    commentEtag=data['items'][i]['snippet']['topLevelComment']['etag']
                    videoId=data['items'][i]['snippet']['videoId']
                    originalCommentText=data['items'][i]['snippet']['topLevelComment']['snippet']['textOriginal']
                    commentAuthorName=data['items'][i]['snippet']['topLevelComment']['snippet']['authorDisplayName']
                    commentAuthorChannelId=data['items'][i]['snippet']['topLevelComment']['snippet']['likeCount']
                    commentPublishedAt=data['items'][i]['snippet']['topLevelComment']['snippet']['publishedAt']
                    commentUpdatedAt=data['items'][i]['snippet']['topLevelComment']['snippet']['updatedAt']
                    replyCount=data['items'][i]['snippet']['totalReplyCount']
                    comment_lang=""
                    detector = google_translator() 
                    translator = google_translator()
                    
                    transCommentText=data['items'][i]['snippet']['topLevelComment']['snippet']['textOriginal']
                    
                    try:
                        
                        detect_comment = detector.detect(originalCommentText)
                        # print("comment language", detect_comment)
                        comment_lang=detect_comment[0]
                        if(detect_comment[0]!='en'):
                            transCommentText = translator.translate(originalCommentText, lang_tgt='en')
                    except:
                        transCommentText=data['items'][i]['snippet']['topLevelComment']['snippet']['textDisplay']
                        
                    comments.append({"videoId":videoId, "commentId":commentId, 'commentPublishedAt': commentPublishedAt,
                                      "commentUpdatedAt":commentUpdatedAt, "commentAuthorChannelId": commentAuthorChannelId,
                                      "commentAuthorName":commentAuthorName, "commentOriginalText": originalCommentText,
                                      "commentTransText": transCommentText, "language":comment_lang,
                                      "replyCount": replyCount})
                    if(replyCount>0):
                        print("Reply Count %d"%replyCount)     
                    
                    if ((replyCount>0) & ('replies' in data['items'][i])):
                        for reply in data['items'][i]['replies']['comments']:
                            replyId=reply['id']
                            videoId=reply['snippet']['videoId']
                            parentCommentId=reply['snippet']['parentId']
                            replyAuthorName=reply['snippet']['authorDisplayName']
                            replyauthorChannelId=reply['snippet']['authorChannelId']['value']
                            replyLikeCount=reply['snippet']['likeCount']
                            replyPublishedAt=reply['snippet']['publishedAt']
                            replyUpdatedAt=reply['snippet']['updatedAt']
                            reply_lang=""
                            originalReplyText=reply['snippet']['textOriginal']
                            detector = google_translator() 
                            translator = google_translator()
                            
                            transReplyText=reply['snippet']['textOriginal']
                            
                            try:
                        
                                detect_reply = detector.detect(originalReplyText)
                                # print("comment language", detect_comment)
                                reply_lang=detect_reply[0]
                                if(detect_reply[0]!='en'):
                                    transReplyText = translator.translate(originalReplyText, lang_tgt='en')
                            except:
                                transReplyText=reply['snippet']['textDisplay']
                            
                            replies.append({"videoId":videoId, "replyId":replyId, 'replyPublishedAt': replyPublishedAt,
                                      "replyUpdatedAt":replyUpdatedAt, "replyAuthorChannelId": replyauthorChannelId,
                                      "replyAuthorName":replyAuthorName, "replyOriginalText": originalReplyText,
                                      "replyTransText": transReplyText, "language":reply_lang, "parentCommentID": parentCommentId})
                            
    df_comments=pd.DataFrame().from_dict(comments)
    df_replies=pd.DataFrame().from_dict(replies)
    
    print(len(df_comments), len(df_replies))
    sorted_video=start_video_index
    for v in allvideos:
        if v in list_of_files[0]:
            sorted_video=v
    print("Video ID", sorted_video)
    df_comments.to_csv("C:/RESEARCH/Datasets/WH_YouTube/Comment_Reply_Formatted_v2/comments_"+str(sorted_video)+".csv")
    df_replies.to_csv("C:/RESEARCH/Datasets/WH_YouTube/Comment_Reply_Formatted_v2/replies_"+str(sorted_video)+".csv")
    start_video_index+=1                