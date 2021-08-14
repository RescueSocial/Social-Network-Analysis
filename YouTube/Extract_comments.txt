# -*- coding: utf-8 -*-
"""
Created on Sat Jun 19 10:09:16 2021

@author: nacho
"""

from google_trans_new import google_translator 
import os
from pprint import pprint
import json
import pandas as pd

from googleapiclient.discovery import build

api_key=#Get your api key
service_name='youtube'
api_version='v3'
part_string="snippet, replies"
#Fill this list with the video IDs for those you have extracted the comments. You will need it beacuse 
#of the inherent limit on the API requests. It will allow you to download certain amounts of comments
#After that you have to restart the script to extract the comments for the rest of the videos
found_video_ids=["YDvugsSjI6s", "TTqXl0lCqa0", "MK6TXMsvgQg", "t-wFKNy0MZQ", "nDbeqj-1XOo", "Kjgwjh4H7wg",
           "zjedLeVGcfE", "iNw5TjS63-w", "6SIlp_f6egI", "j1a3WAcVBYo", "ZpVd7k1Uw6A" , "W8Id0-Lsyr0",
           "qr_ByQH2QY0", "KzfqS7oUU2w", "XsLn28TPUT0", "hl_pgTsq4tg", "lXY7MmZ9Ccc", "zeOw5KRVNvc",
           "wPp8eKBjcyA", "nDf-OuK2gKw", "4qAXQxtYsN4", "aYVw2sl-4hA", "HkHb0E3I80I", "ZLTkMYg4zbI",
           "nmZqb2VVc48", "LKE6YKw5Y40", "LsEFAEemnnA", "KXzNo0vR_dU", "KwrETbBQ1DM", "JPFaEG9vJT4", 
           "F3_EXqJ8f-0", "reuQAoXM8bE", "jERWeylLH-s", "aBv8kqKck6E", "ECko3KDC2w8", "Dqn0bm4E9yw",
           "urrqW4_3IBg", "sBmWe5FnSCc", "Cvrprxvazcg", "SsIO10lEa3Y", "OD2gAjFtZ1A", "BddSN2jNS9E",
           "SXH0rUOju3I", "7WJXHY2OXGE", "jifS0fi9WB8", "kTtAm0OHW24", "I8mA0h7dCKI", "hnY2hlo0x_M",
           "h10FaTfkMEY", "VyPcGWOTX54", "p4KLrQKJn3c", "LU-0PTsAPoI", "YRWRRBX3TB0", "4N7Z7nJ4fiI",
           "lSXwG-901yU", "aNVkEi9LKfI", "DCu8mNC1JyE", "9Xvmr3GOOik", "tYM7Ju-YXmE", "uoIbgmGxdmE", 
           "fvYFtCl26Zs", "V-yba3R6IBY", "2pwXfHyTlCo", "g1VNQGsiP8M","QtUcGR0Og6c", "6QTUZNPgpZQ",
           "OJZRvp6w4wc", "zGEc-CMsrQs", "lWx7C47a1KU", "Z9F-cHc5Qog", "kfNln981Dic", "26lkrCzObpQ",
           "LmYCgK2zHCI", "LmfVs3WaE9Y", "ZfIKWxNiinM", "2rdTBmCRSB4", "dA1XQIWW9iM", "To91BJGKr5I",
           "11AiTgL6W_M", "ikWyNJobKuc", "LfjL9uX2leg", "dIgmLc3DBtY", "dxRiG8vRRBk", "mNTgL82D4Xo",
           "Mydfue-vF90", "JqQa-QSMMjs", "b07Z_qfchFk", "pnbx00-L_EI", "CJ3KfEdTT3Y", "2-uUOv7UCkQ", 
           "L9hPwbc8JZo", "bbWAABd9CV4", "Q-z_eQcdQVI", "Kg6_-zEPV-g", "PRTeLIjQ2jk", "vWlXTBaN1Sc",
           "xKhdfuiL1bE", "9iejzhb_-Do", "gLABmqdJZF0", "fPQ9uA_M1Eg", "3JFEmCKHVME", "MnSAB4qeDug",
           "FmxRddgpo-I", "HxN1STgQXW8", "7K53xrggn1Q", "FtA21eiSmT8", "THdMj0-LmRw", "jdP8TiKY8dE",
           "2K7TU1Hh_3U", "aTKIqc6vQXI", "45odEv_1DAY", "hWLjYJ4BzvI", "DbQB1EQ32CE", "y7Rq4vvGMxE",
           "jBfygUiS50g", "yiC4w7Erz8I", "fWkfpGCAAuw", "3RlbqOl_4NA", "OwDiPrFCM0M", "_O2TRzA2ezk",
           "tEpwvvyrAJU", "sslCRVx7nPQ", "cSGf2ZpDENU", "EFhORWVFBUw", "3wj4ncIEDxw", "7sPY0X8SrLo",
           ]
def youtube_comment_search(video_list, file_num=0):

    youtube=build(service_name, api_version, developerKey=api_key)
    
    for v in video_list:
        if v not in found_video_ids:
            index=1
            print("video id", v)
            comment_response=youtube.commentThreads().list(part=part_string,
                                                            videoId=v).execute()
            with open("C:/RESEARCH/Datasets/Christina/Videos/comment_records/comment_details_"+str(v)+"_"+str(index)+".json", "w") as outfile:
                json.dump(comment_response, outfile)
            
            while 'nextPageToken' in comment_response:
                    comment_response = youtube.commentThreads().list(
                            part=part_string, videoId=v, pageToken=comment_response['nextPageToken']
                            ).execute()
                    index+=1
                    with open("C:/RESEARCH/Datasets/Christina/Videos/comment_records/comment_details_"+str(v)+"_"+str(index)+".json", "w") as outfile:
                        json.dump(comment_response, outfile)

        
    
    
if __name__== "__main__":
    
   
    #Populate the video_list with the ID of the videos (copy the vide id 
    #from the youtube link provided)
    video_list=['uretrfMA-Io']
    youtube_comment_search(video_list)