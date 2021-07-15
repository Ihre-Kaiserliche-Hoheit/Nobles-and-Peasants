import os
import shutil as sht


def rename_file(filename, new_name):
    os.rename(filename, new_name)

def move_file(file, target):
    sht.move(file, target)
