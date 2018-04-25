'''
@author: Terry Ruas 2018-03-12
'''
#imports
from nltk.corpus import wordnet as wn

#self-packages
from my_data import DefiData  # @UnresolvedImport
from my_data import RefiData  # @UnresolvedImport
from text_module import text_process as tp # @UnresolvedImport


def synset_all(word):
    return wn.synsets(word)  # @UndefinedVariable
#synsets for all POS

def synset_pos(word, cat):
    return wn.synsets(word, cat)  # @UndefinedVariable
#synsets for specific POS
   
def build_synset_dict(word, pos=None):
    synset_defidata_list = []

    if not pos:#for all POS
        synsets = synset_all(word)
    else:#for specific POS
        synsets = synset_pos(word,pos)
    
    for sys_element in synsets:#create list of Synsets, offset, POS and their glosses - DefiObject
        synset_defidata_list.append(DefiData(sys_element, sys_element.offset(), sys_element.pos(), sys_element.definition()))

    return(synset_defidata_list)
#list of SYNSET:OFFSET:POS:GLOSS based on DefiData

def build_refi_synset_dict(word, embed_model, *pos):
    synset_refidata_list = []

    if not pos:#for all POS
        synsets = synset_all(word)
    else:#for specific POS
        synsets = synset_pos(word,pos)
    
    for sys_element in synsets:#create list of Synsets, offset, POS
        key = tp.key_parser(word, sys_element.offset(), sys_element.pos())
        tmp_vec = retrieve_synsetvec(key, embed_model)
        #initialize RefiData with retrieved vector-value
        tmp_refi = RefiData(sys_element, sys_element.offset(), sys_element.pos())
        tmp_refi.vector = tmp_vec
        synset_refidata_list.append(tmp_refi)

    return(synset_refidata_list)
#list of SYNSET:OFFSET:POS:GLOSS based on DefiData

def retrieve_synsetvec(key, model):
    try:
        tmp_vec = model.word_vec(key)
    except KeyError:
        tmp_vec = [0.0] #key not in the model
    return(tmp_vec)
#returns the dimension/values of a key in a word-embedding model

#===============================================================================
# TEST CASE
#===============================================================================

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