'''
@author: Terry Ruas 2018-03-12
'''
#imports
from nltk.corpus import wordnet as wn

#self-packages
from my_data import SynsetData  # @UnresolvedImport
from text_module import text_process as tp # @UnresolvedImport


def build_synset_data(word, embed_model, refi_flag, *pos):
    synsets_data = []
    if not pos:#for all POS
        synsets = synset_all(word)
    else:#for specific POS
        synsets = synset_pos(word,pos)  
    
    for sys_element in synsets:#create list of Synsets, offset, POS
        if refi_flag: #using refinement model
            key = tp.key_parser(word, sys_element.offset(), sys_element.pos())
            vec = retrieve_synsetvec(key, embed_model)
            #initialize RefiData with retrieved vector-value
            tmp_refi = SynsetData(sys_element, sys_element.offset(), sys_element.pos(), sys_element.definition())
            tmp_refi.vector = vec
            synsets_data.append(tmp_refi)
        else:#using normal mode
            synsets_data.append(SynsetData(sys_element, sys_element.offset(), sys_element.pos(), sys_element.definition()))
    
    return(synsets_data)
#Creates the package for each synset for each given word

#===============================================================================
# Retrieve stuff from WordNet and Model
#===============================================================================

def synset_all(word):
    return wn.synsets(word)  # @UndefinedVariable
#synsets for all POS

def synset_pos(word, cat):
    return wn.synsets(word, cat)  # @UndefinedVariable
#synsets for specific POS

def retrieve_synsetvec(key, model):
    try:
        tmp_vec = model.word_vec(key)
    except KeyError:
        tmp_vec = [0.0] #key not in the model
    return(tmp_vec)
#returns the dimension/values of a key in a word-embedding model

#===============================================================================
# def print_type_feature(word):
#     a = synset_pos(word, 'n')
#     print(a[0])
#     print(a[0].definition())
#     print(type(a[0].definition()))
#     print(a[0].offset())
#     print(a[0].pos())
#     
# #print_type_feature('java')
# 
# 
# def print_synset_features(syn):
#     for sys in syn:
#         ttr = str(sys)
#         print(sys)
#         print('Slice SID: ', ttr[len(ttr)-4:len(ttr)-2])
#         print('-- Offset:\t', sys.offset())
#         print('-- OffsetType:\t', type(sys.offset()))
#         print('-- POS:\t', sys.pos())
#         print('-- Gloss:\t', sys.definition())
#         print('-- Example:\t', sys.examples())
#         print('-- Lemma:\t', sys.lemmas())
#         print('-- Lemma_Names:\t', sys.lemma_names())        
# #take a bunch of features from a synset 
#===============================================================================

#retrieve synset from offset
#f = wn.synset_from_pos_and_offset('n',6901053)  # @UndefinedVariable pos,offset