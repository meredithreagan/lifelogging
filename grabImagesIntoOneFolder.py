
import sys
import os
import shutil


def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]


if __name__ == '__main__':

    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    print input_dir, output_dir

    subdirs = get_immediate_subdirectories(input_dir)
    print subdirs

    for subdir in subdirs:
        #halfDayDirs.append(subdir)
        print subdir
        halfDayDirs = get_immediate_subdirectories(input_dir + '/' + subdir)
        for halfDayDir in halfDayDirs:
            print halfDayDir
            thisPath = input_dir + '/' + subdir + '/' + halfDayDir
            files = os.listdir(thisPath)
            for file1 in files:
                print file1
                shutil.copyfile(thisPath + '/' + file1, output_dir + '/' + file1)
