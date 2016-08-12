import os
import sys
import json

folder_scan = {}


def read_folders(scanpath):
    print("scanning folders --- change name(?)")
    dirs = os.listdir(scanpath)
    print(dirs)
    dossier = {}
    for folder in dirs:
        path = os.path.join(scanpath, folder)
        if ' - ' in folder and os.path.isdir(path):
            print('processing', folder)
            prefix, suffix = folder.split(' - ', 1)
            dossier[prefix] = {"name": suffix, "path": path}
        else:
            print('skipping', folder)
    return dossier

def save_folder(dossier):
    print("saving folders from scan")
    with open("folders.txt", "w") as f:
        json.dump(dossier, f, indent = 4)
    print(dossier)


print("scanning folder, needs to check for removed folders")
s = read_folders("\\\\SERVER/Data_Topco_Srv_2012/Gemeenschappelijk_Srv_2012/VC - EPB lopende werven")  

save_folder(s)




