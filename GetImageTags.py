# Input is Images Directory 
# print metadata 

# import libraries
import subprocess
import os

def GetImageTags(folderpath):
    infoDict = {}
    exifToolPath = 'exiftool'
    for images in os.listdir(folderpath):

        imgPath = folderpath + "/" + str(images)    

        # use Exif tool to get the metadata 
        process = subprocess.Popen([exifToolPath,imgPath],stdout=subprocess.PIPE, stderr=subprocess.STDOUT,universal_newlines=True) 
        
        for tag in process.stdout:
            line = tag.strip().split(':')
            infoDict[line[0].strip()] = line[-1].strip()

    return infoDict



if __name__== "__main__":
    folderpath = input("Enter folder path:\n")
    
    DictOut = GetImageTags(folderpath)
    for k,v in DictOut.items():
        print(k,':', v)
        
    

#/mnt/d/PICTURES