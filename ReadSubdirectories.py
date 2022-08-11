# In this file I can read all the images under given directory includes all subdirectories
# Later on I'll change it and given our NAS drive path in a list so you can change accordingly

import subprocess
import os

def FetchAllDirectories(dirname):
    subfolders= [f.path for f in os.scandir(dirname) if f.is_dir()]
    for dirname in list(subfolders):
        subfolders.extend(FetchAllDirectories(dirname))
    return subfolders


def GetImageTags(folderpath):
    infoDict = {}
    exifToolPath = 'exiftool'
    for images in os.listdir(folderpath):
        imgPath = folderpath + "/" + str(images) 
        process = subprocess.Popen([exifToolPath,imgPath],stdout=subprocess.PIPE, stderr=subprocess.STDOUT,universal_newlines=True) 
        
        for tag in process.stdout:
            line = tag.strip().split(':')
            infoDict[line[0].strip()] = line[-1].strip()
    return infoDict


if __name__== "__main__":
    folderpath = input("Enter folder path:\n")
    OutPut = FetchAllDirectories(folderpath)
    
    for filepaths in OutPut:
        DictOut = GetImageTags(folderpath)
        for k,v in DictOut.items():
            print(k,':', v)
    
