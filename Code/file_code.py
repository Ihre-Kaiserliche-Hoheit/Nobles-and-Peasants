import os
import shutil as sht


def txt_to_list(filename):
    file = open(filename, "r")
    file = file.read().splitlines()
    return(file)
    
def delete_file(filename):
    os.remove(filename)

def delete_folder(foldername):
    sht.rmtree(foldername)

def rename_file(filename, new_name):
    os.rename(filename, new_name)

    
def move_file(file, target):
    sht.move(file, target)
