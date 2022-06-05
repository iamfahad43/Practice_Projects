#!/usr/bin/env python
# coding: utf-8

# In[3]:


import sys
import os
import requests as r
import wget
Video_dir = os.path.join('')#Enter the path you want the video to be
try:
    LINK = input("Enter URL of the video") #url of video to be downloaded
    html = r.get(LINK)
except r.ConnectionError as e:
    print("Error in connecting")
except r.Timeout as e:
    print("Timeout")
except r.RequestException as e:
    print("Invalid URL")
except (KeyboardInterrupt, SystemExit):
    print("System has quit")
    sys.exit(1)
except TypeError:
    print("Video seems to be private ")
else:
    print("\n")
    print("Video Quality:Normal " )
    print("[+] Starting Download")
wget.download(LINK,Video_dir)
print("\n")
print("Video downloaded")


# In[ ]:




