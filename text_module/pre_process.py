'''
@author: Terry Ruas 2018-03-12

'''
import re
import os
import gensim

#===============================================================================
#PREPROCESSING
#===============================================================================

def simple_textclean(fname, en_stop, tokenizer):
    with open(fname, 'r', encoding='utf-8', error = 'ignore') as fin:
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
#simple dataclean - returns a list of tokens-words for a document

#===============================================================================
# FOLDER/FILE/INPUT-Param - Reading
#===============================================================================
def checkAlgorithmCost(algorithm_type=True):
    if(algorithm_type):
        return(True)
    else:
        return(False)
#check which cost is used during Disambiguation: DIJKSTRA or MSSA Base (Default)

def checkModelLoad(model_folder, model=True):
    if(model):
        token_embeddings_model = gensim.models.KeyedVectors.load(model_folder)
    else:
        token_embeddings_model = gensim.models.KeyedVectors.load_word2vec_format(model_folder, binary=True) #googlevector model
    return(token_embeddings_model)
#checks which kind of word-embedding will be used WORD (Google) or SYNSET(MSSA)(default)

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
