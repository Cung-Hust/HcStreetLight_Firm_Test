from mega import Mega
import os
from os import listdir
from os.path import isfile, join

mega = Mega()
mega._login_user("Cungdd.bkhn@gmail.com", "Cung_21091997")


def absoluteFilePaths(directory):
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            yield os.path.abspath(os.path.join(dirpath, f))


directory = "/home/rd/Desktop/RD_StreetLight/UploadFile/Mega/test.txt"
file_path_generator = absoluteFilePaths(directory)

Folder = mega.find("Logs")  # change it with the folder in your mega
print(Folder)
print(Folder[0])
for file_path in file_path_generator:
    mega.upload(file_path, Folder[0])
