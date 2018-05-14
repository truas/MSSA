'''
@author: Terry Ruas - 2018-04-23
Important: work in the same way as wn_manage, but used the synset_vector for the words in the input text

'''
#import
import logging
import gensim
import time
import nltk
import sys
import argparse #for command line arguments
import os

#python module absolute path
pydir_name = os.path.dirname(os.path.abspath(__file__))

#python path definition
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

#from-imports
from datetime import timedelta
from stop_words import get_stop_words

#self-packages
import general_module.index_cost_op as icop #wordnet index cost
import general_module.struct_op as suop
import general_module.vector_op as veop #cosine_cost
import text_module.pos_process as posp
import text_module.pre_process as prep
import text_module.text_process as tp


from distance_reader import DistanceReader #in case of index-cost is used @UnresolvedImport
from my_data import DocData  # @UnresolvedImport



#input/output files/folder - If you need to set input, output and model folders
#in_foname = "C:/tmp_project/BSDExtractor/input"
#ou_foname = "C:/tmp_project/BSDExtractor/output"
#mo_foname = "C:/tmp_project/BSDExtractor/model/300d-5w-5mc-cbow.model" #binary true


#DISTANCES_files_path = 'C:/tmp_datasets/Wordnet/dict_map' #in case index-cost is used

#show logs
logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s',
    level=logging.INFO)

#map_cost = DistanceReader(DISTANCES_files_path + "/distances.bin", DISTANCES_files_path + "/distances.idx") #index-cost path - read
tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
en_stop = get_stop_words('en')
nltk.download('wordnet') #just to guarantee wordnet from nltk is installed

#overall runtime start
start_time = time.monotonic()

#Main core
if __name__ == '__main__':  
    
    #IF you want to use COMMAND LINE for folder path
    parser = argparse.ArgumentParser(description="BSD_Extractor - Transforms text into synsets")
    parser.add_argument('--input', type=str, action='store', dest='inf', metavar='<folder>', required=True, help='input folder to read document(s)')
    parser.add_argument('--output', type=str, action='store', dest='ouf', metavar='<folder>', required=True, help='output folder to write document(s)')
    parser.add_argument('--model', type=str, action='store', dest='mod', metavar='<folder>', required=True, help='trained word embeddings model')
      
    args = parser.parse_args()
        
    #COMMAND LINE  folder paths
    input_folder = args.inf
    output_folder = args.ouf
    model_folder = args.mod
      
    #in/ou relative location - #input/output/model folders are under synset/module/
    in_foname = os.path.join(pydir_name, '../'+input_folder) 
    ou_foname = os.path.join(pydir_name, '../'+output_folder)
    mo_foname = os.path.join(pydir_name, '../'+model_folder)
    
    #Loads
    trained_w2v_model = gensim.models.KeyedVectors.load(mo_foname) #refined model

    #Input list of documents - one or many folders
    documents_list = prep.doclist_multifolder(in_foname)
    doc_names = prep.fname_splitter(documents_list) #remember to adjust the splitter depending on the OS
    counter = 0 #counter for document-name
    

#===============================================================================
# GAMMA Block: Context (make_bsd) - uses refi
#===============================================================================

    for document in documents_list:
        try:
            doc_obj = DocData()
            
            doc_words = prep.simple_textclean(document, en_stop, tokenizer) 
            print('TextClean for Document %s - Done: %s' %(doc_names[counter],(timedelta(seconds= time.monotonic() - start_time))))
            
            doc_obj.wordsdata = tp.build_word_data(doc_words, trained_w2v_model, refi_flag=True)
            print('WordData for Document %s - Done: %s' %(doc_names[counter],(timedelta(seconds= time.monotonic() - start_time))))
                    
            doc_obj.wordsdata = veop.make_bsd(doc_obj.wordsdata, refi_flag=True) #disambiguating words using Former-Latter cosine of synet-glosses-vectors(words) from word embeddings
            #doc_obj.wordsdata = veop.make_bsd_dijkstra(doc_obj.wordsdata, refi_flag=True) #disambiguating synet-glosses-vectors(words) using Dijkstra 
            print('PrimeBSDData for Document %s - Done: %s' %(doc_names[counter],(timedelta(seconds= time.monotonic() - start_time))))
             
            posp.bsid_ouput_file(doc_obj.wordsdata, doc_names[counter], ou_foname) #produce the BSD for every word in the document
            print('Document %s - Saved: %s'  %(doc_names[counter],(timedelta(seconds= time.monotonic() - start_time))))
            counter+=1
        
        #simple try-catch to avoid documents with few words/null or documents which all items are not in our knowledge database - Skip those documents
        except IndexError:
            counter+=1
            continue
    
    print('finished...')
    end_time = time.monotonic() #finish overall time   
    print(timedelta(seconds=end_time - start_time))



#==============================TEST CASES=======================================
#Print Test words in documents
#===============================================================================
# for doc in docs_list:
#     for i in doc.wordsdata:
#         print('Word: ', i.word)
#         print('** Psys_id:\t', i.prime_sys.psys_id)
#         print('** Poffset:\t', i.prime_sys.poffset)
#         print('** Ppos:\t', i.prime_sys.ppos)
#         for j in i.defi:
#             print(j.sys_id)
#             print('----- Offset:\t', j.offset)
#             print('----- POS:\t', j.pos)
#             print('----- Gloss:\t', j.gloss)
#             print('----- Gloss:\t', j.gloss_avg_vec)         
#===============================================================================



    

