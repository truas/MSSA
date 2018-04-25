'''
@author: Terry Ruas 2018-03-12

'''
import os
                
def count_files(docs_folder):
    return len(os.listdir(docs_folder)) # dir is your directory path, everything in folder
#number of elements in a folder 