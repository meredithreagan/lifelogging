
import os
import sys
import PIL
from PIL import Image


def list_files(dir):
    r = []
    for root, dirs, files in os.walk(dir):
        for name in files:
            r.append(os.path.join(root, name))
    return r


def resize_images(dir):

    filePaths = list_files(dir)

    for filePath in filePaths:

        print filePath

        baseheight = 500
        img = Image.open(filePath)
        hpercent = (baseheight / float(img.size[1]))
        wsize = int((float(img.size[0]) * float(hpercent)))
        img = img.resize((wsize, baseheight), PIL.Image.ANTIALIAS)
        img.save(filePath)


if __name__ == '__main__':

    input_dir = sys.argv[1]

    resize_images(input_dir + '/')
