# from task04_path

import re
import os
import shutil

from pathlib import Path


##########################################################
img_f = ['.jpeg', '.png', '.jpg', '.svg', ".bmp"]
mov_f = ['.avi', '.mp4', '.mov', '.mkv', ".webm", ".wmv", ".flv"]
doc_f = ['.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx', ".ini", ".cmd", ".ppt", ".xml", ".msg", ".cpp", ".hpp"]
mus_f = ['.mp3', '.ogg', '.wav', '.amr', ".aiff"]
arch_f = ['.zip', '.gz', '.tar'] # shutil.ReadError: Unknown archive format gz-format
# https://stackoverflow.com/questions/55040442/how-to-register-gz-format-in-shutil-register-archive-format-to-use-same-format

##########################################################
CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

CATEGORIES = { "images" : img_f, "video" : mov_f, "documents" : doc_f, "audio": mus_f, "archives" : arch_f }
TRANS = {}
for c, t in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = t
    TRANS[ord(c.upper())] = t.upper()

###########################################################

def getCategory(pathFile):              # (string fileName)
    for cat, exts in CATEGORIES.items():
        if pathFile.suffix.lower() in exts:
            return cat, True            #(string, Bool)
    return "others", False               #(string, Bool)

###########################################################
def normalize(name):
    rename = name.translate(TRANS)
    rename = re.sub(r'[^a-zA-Z0-9 -]', "_", rename)
    return rename
###########################################################
def parse_folder(root, ipath):

    if not Path(root).exists(): return False

    # check if current directory is root.
    absPath = root if ipath == "" else ipath

    folders = []
    path = Path(absPath)
    absPath += "/"

    #print("-->>" + absPath)

    for i in path.iterdir():
        if i.is_dir():
            folders.append(i.name)
            empties = False
        
        elif i.is_file():
            pathFile = Path(absPath + i.name)
            cat, success = getCategory(pathFile)  #(string, Bool)
            if success:
                newName = normalize(pathFile.stem)

                # prepare target folder for category
                targetDir = Path(root + "/" + cat)
                #print(targetDir.absolute())
                if not targetDir.exists():
                    targetDir.mkdir()
                
                #print(newName)

                targetFile = Path(root + "/" + cat + "/" + newName + pathFile.suffix)
                if not targetFile.exists():
                    pathFile.replace(targetFile)

                    if cat == "archives":
                        shutil.unpack_archive(targetFile.absolute(), root + "/" + cat + "/" + newName)

                    #print(str(targetFile.absolute()))
                #else:
                #    print("already exist")

            #print(cat + ": ", absPath + i.name, pathFile.stem)

    #*********************************

    for i, dirName in enumerate(folders):
        if parse_folder(root, absPath + dirName) == True:
            rmDir = Path(absPath + dirName)
            rmDir.rmdir()

    empties = True
    for iter in path.iterdir():
        if iter.is_file() or iter.is_dir():
            empties = False
            break

    return empties

#############################################################

parse_folder("C:/Downloads", "")
# C:/Users/APodoba/Downloads/[Categories]

