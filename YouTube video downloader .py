#!/usr/bin/env python
# coding: utf-8

# In[1]:


# importing the module 
from pytube import YouTube 
  
# where to save 
SAVE_PATH = input("The path where to download the video")
  
# link of the video to be downloaded 
link=input("Paste the link of the video to be downloaded")
  
try: 
    # object creation using YouTube
    # which was imported in the beginning 
    yt = YouTube(link) 
except: 
    print("Connection Error") #to handle exception 
  
# filters out all the files with "mp4" extension 
mp4files = yt.filter('mp4') 
  
#to set the name of the file
yt.set_filename('GeeksforGeeks Video')  
  
# get the video with the extension and
# resolution passed in the get() function 
d_video = yt.get(mp4files[-1].extension,mp4files[-1].resolution) 
try: 
    # downloading the video 
    d_video.download(SAVE_PATH) 
except: 
    print("Some Error!") 
print('Task Completed!') 


# In[ ]:




