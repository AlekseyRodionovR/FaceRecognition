import os
import json

directory = "./FaceRecognition"
files = os.listdir(directory)
images = list(filter(lambda x: x.endswith('.jpg'), files))
#print(images)
#print(len(images))
#a= len(images)
#print(images)
per = "jpg"
Myfile = open('./FaceRecognition/Images.txt','a')
for i in range(0,len(images)):
    #print(images[i])
    Myfile.write(str(i+1)+".jpg"+"\n")
lineList = list()
print(images)
with open("./FaceRecognition/SurnameName.txt") as f:
    for line in f:
        lineList.append(line)
    print(lineList)
