'''
@author: Terry Ruas 2018-03-12
'''
#imports
from nltk.corpus import wordnet as wn

#self-packages
from my_data import SynsetData  # @UnresolvedImport
from text_module import text_process as tp # @UnresolvedImport

def build_synset_data(word, embed_model, refi_flag):
    synsets_data = []
      
    synsets = wn.synsets(word) # @UndefinedVariable
    last_synset_added = -1 #to keep track of the last synset added for each word
    for sys_element in synsets:#create list of Synsets, offset, POS
        synsets_data.append(SynsetData(sys_element, sys_element.offset(), sys_element.pos(), sys_element.definition()))#all synsets are added for each word regardless 
        if refi_flag: #using recurrent model we retrieve the word-sense vector
            key = tp.key_parser(word, sys_element.offset(), sys_element.pos())
            vec = retrieveWordSynsetVector(key, embed_model)
            synsets_data[last_synset_added].vector = vec
        else:
            pass
    return(synsets_data)
#Creates the package for each synset for each given word

#===============================================================================
# Retrieve stuff from WordNet and Model
#===============================================================================
def retrieveWordSynsetVector(key, model):
    try:
        tmp_vec = model.word_vec(key)
    except KeyError:
        tmp_vec = [0.0] #key not in the model
    return(tmp_vec)
#returns the dimension/values of a key in a token-embedding model

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