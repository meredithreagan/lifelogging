
import sys
import os
import shutil


def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]


if __name__ == '__main__':

    input_dir = sys.argv[1]
    print input_dir
    
    pathiter = (os.path.join(root, filename)
        for root, _, filenames in os.walk(input_dir)
        for filename in filenames
        )
    for path in pathiter:
        newname = path.replace(':', '-')
        if newname != path:
            print newname
            os.rename(path, newname)
