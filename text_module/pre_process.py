'''
@author: Terry Ruas 2018-03-12

'''
import re
import os


def simple_textclean(fname, en_stop, tokenizer):
    with open(fname, 'r', encoding='utf-8') as fin:
        contents = fin.read()
        # clean and tokenize document string
        raw = str(contents.lower())
        tokens = tokenizer.tokenize(raw)
        # remove stop words from tokens
        stopped_tokens = [i for i in tokens[:] if not i in en_stop] #[1:] get rid of the 'b'byte if using 'rb'
        # remove numbers
        number_tokens = [re.sub(r'[\d]', ' ', i) for i in stopped_tokens]
        number_tokens = ' '.join(number_tokens).split()
        #removing noise single chars
        no_one_char_tokens = [i for i in number_tokens if not len(i) == 1]
   
    return(no_one_char_tokens)
#simple dataclean - returns a list of tokens-words for a documnet

def doclist_multifolder(folder_name):
    input_file_list = []
    for roots, dir, files in os.walk(folder_name):
        for file in files:
            file_uri = os.path.join(roots, file)
            #file_uri = file_uri.replace("\\","/") #if running on windows           
            if file_uri.endswith('txt'): input_file_list.append(file_uri)
    return input_file_list
#creates list of documents in many folders

def fname_splitter(docslist):
    fnames = []
    for doc in docslist:
        blocks = doc.split('/') # '/' for UNIX # '\\' for WINDOWS
        fnames.append(blocks[len(blocks)-1])
    return(fnames)
#getting the filenames from uri of whatever documents were processed in the input folder   


#===============================================================================
# UNUSED METHODS - 2018-03-30
#===============================================================================

#===============================================================================
# #output files
# bsd_list = "BSID_doc_list.txt"
# doc_list = "DOC_list.txt"
#===============================================================================

#===============================================================================
# def make_bsid_list(docs_folder):
#     #list o BSD-Document file will be produced - the same size as the original (raw-input) file list
#     bsd_file_list = [name for name in listdir(docs_folder) if name.endswith('txt')]
#     bsd_doc_list = open(bsd_list, 'w+')
#     #saving bsid list
#     for file in bsd_file_list:
#         bsd_doc_list.write(file+'\n')
# 
#     bsd_doc_list.close() #BSID list just file name
#     return (bsd_file_list)
# #creates list of BSID-documents based on the initial rwa-files
#===============================================================================


#===============================================================================
# def make_doc_list(folder_name):
#     #read all files in a  folder with .txt format and makes a list of them
#     input_file_list = [folder_name+'/'+name for name in listdir(folder_name) if name.endswith('txt')]
#     doc_data_list = open(doc_list, 'w+')
# 
#     #saving document list
#     for file in input_file_list:
#         doc_data_list.write(file +'\n')
#     doc_data_list.close() #raw-input list with absolute path
#     
#     #show the number of files in the directory
#     print ('Found %s documents under the dir %s .....'%(len(input_file_list), folder_name))
#     return (input_file_list)
# #creates list of documents in a folder
#===============================================================================

#===============================================================================
# def get_doc_binary(docs_folder, en_stop, tokenizer):
#     doc_list = make_doc_list(docs_folder)
# 
#     for fname in doc_list:
#         with open(fname, 'r', encoding='utf-8') as fin:
#             contents = fin.read()
#             # clean and tokenize document string
#             raw = str(contents.lower())
#             tokens = tokenizer.tokenize(raw)
#             # remove stop words from tokens
#             stopped_tokens = [i for i in tokens[:] if not i in en_stop] #[1:] get rid of the 'b'byte if using 'rb'
#             # remove numbers
#             number_tokens = [re.sub(r'[\d]', ' ', i) for i in stopped_tokens]
#             number_tokens = ' '.join(number_tokens).split()
#             #removing noise single chars
#             no_one_char_tokens = [i for i in number_tokens if not len(i) == 1]
#             
#             
#             yield no_one_char_tokens
# #iterator of documents and clean word document
#===============================================================================