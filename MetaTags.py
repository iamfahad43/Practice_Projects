
# Get Images tags using API

import os
import io
from google.cloud import vision
from google.oauth2 import service_account

# here is the path where our REST APi is
credentials = service_account.Credentials.from_service_account_file('/var/services/homes/dev2_img/Python_Script/apicredentials.json')

client = vision.ImageAnnotatorClient(credentials=credentials)

def detect_labels(ImageName, DirectoryPath):
    ImagesToGetTags = DirectoryPath + "/" + str(ImageName)
    print("detect_labels() was called")
    print(f"This is what was passed to detect_labels() - {ImagesToGetTags}\n")
    #client = vision.ImageAnnotatorClient(credentials=credentials)
    with io.open(ImagesToGetTags, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.label_detection(image=image)
    labels = response.label_annotations
    print('Labels:')
    
    FinalFileName = os.path.join(DirectoryPath, ImageName+".Exif")
    with open(FinalFileName, 'a') as exiffile:
        for label in labels:
            LablDescription = label.description
            LablScore = label.score 
            print(f"{LablDescription}: ({round(LablScore * 100)}%)")
            exiffile.write(f"{LablDescription}: {LablScore} ")
    
        if response.error.message:
            raise Exception(
                '{}\nFor more info on error messages, check: '
                'https://cloud.google.com/apis/design/errors'.format(
                    response.error.message))
        exiffile.close()
        print("successfully wrote to exif file")

def FetchAllDirectories(dirname):
    subfolders= [f.path for f in os.scandir(dirname) if f.is_dir()]
    for dirname in list(subfolders):
        subfolders.extend(FetchAllDirectories(dirname))
    return subfolders

def GetImageTags(folderpath):
    infoList = []

    for images in os.listdir(folderpath):
        if images[-4:] == ".JPG" or images[-4:] == ".jpg":
            OutPutTags = detect_labels(images, folderpath)
            infoList.append(OutPutTags)
            print("\n")
    return infoList

if __name__== "__main__":
    folderpath = input("Enter folder path:\n")
    OutPut = FetchAllDirectories(folderpath)
    
    print(f"\nList of subdirectories from given path are: {OutPut}\nTatal number of directories wea re working on is: {len(OutPut)}\n")
    for index, filepaths in enumerate(OutPut):
        print(f"\nWorking with Images in path: {filepaths}\n")
        ListOut = GetImageTags(filepaths)
        print(f"Completed {index+1} directory \n")
    