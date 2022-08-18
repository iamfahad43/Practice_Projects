import os
import io
from google.cloud import vision
from google.oauth2 import service_account
import PIL.Image
import PIL.ExifTags

# here is the path where our REST APi is
credentials = service_account.Credentials.from_service_account_file('/mnt/d/Important_documents/apicredentials.json')

client = vision.ImageAnnotatorClient(credentials=credentials)

def detect_labels(ImagesToGetTags):
    print("detect_labels() was called")
    print(f"This is what was passed to detect_labels() - {ImagesToGetTags}\n")
    #client = vision.ImageAnnotatorClient(credentials=credentials)
    with io.open(ImagesToGetTags, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.label_detection(image=image)
    labels = response.label_annotations
    print('Labels:')
    
    img = PIL.Image.open(ImagesToGetTags)
    exif = {
    PIL.ExifTags.TAGS[k]: v
    for k, v in img._getexif().items()
    if k in PIL.ExifTags.TAGS
    }

    LabelsList = []
    for label in labels:
        LablDescription = label.description
        LablScore = label.score 
        print(f"{LablDescription}: ({round(LablScore * 100)}%)")
        LabelsList.append(LablDescription)
    
    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    LabelsStr = "\n".join(LabelsList)
    exif["Labels"] = LabelsStr

def FetchAllDirectories(dirname):
    subfolders= [f.path for f in os.scandir(dirname) if f.is_dir()]
    for dirname in list(subfolders):
        subfolders.extend(FetchAllDirectories(dirname))
    return subfolders

def GetImageTags(folderpath):
    infoList = []

    for images in os.listdir(folderpath):
        if images[-4:] == ".JPG" or images[-4:] == ".jpg":
            ImagesToGetTags = folderpath + "/" + str(images)
            OutPutTags = detect_labels(ImagesToGetTags)
            infoList.append(OutPutTags)
            print("\n")
    return infoList


if __name__== "__main__":
    
    ListSubfolders = [f.path for f in os.scandir("/mnt/d/Work/") if f.is_dir()]
    for index, dr in enumerate(ListSubfolders):
        print(index+1, dr)
    UserChoice = int(input("\nPlease select User by Number:\n"))
    
    folderpath = ListSubfolders[UserChoice-1]
    OutPut = FetchAllDirectories(folderpath)
    
    print(f"\nList of subdirectories from given path are: {OutPut}\nTatal number of directories wea re working on is: {len(OutPut)}\n")
    TotalImagesPassed = 0
    for index, filepaths in enumerate(OutPut):
        print(f"\nWorking with Images in path: {filepaths}\n")
        ListOut = GetImageTags(filepaths)
        print(f"Completed {index+1} directory \n")
        TotalImagesPassed = TotalImagesPassed + len(ListOut)
    
    print(f"Successfully passed {TotalImagesPassed} Images")