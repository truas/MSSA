'''
@author: Terry Ruas 2018-03-12
'''
from functools import total_ordering

#'SynsetData' object in the 'WordsData' (synset_pack) class
@total_ordering
class SynsetData(object): 
    def __init__(self, sys_id, offset, pos, gloss):
        self.sys_id = sys_id #the actual synset (as a whole)
        self.offset = offset
        self.pos = pos
        self.gloss = gloss
        self.gloss_avg_vec = list() #the average vector for that word-synset gloss
        self.vector = [] #vector for this synset token in case our model is made out of synsets
    
    #Necessary methods to implement heapq from Dijkstra
    def __eq__(self, other):
        return False
    def __lt__(self, other):
        return self.offset < other.offset
        
#'WordsData' object for word in a 'Document'
class WordsData(object):
    def __init__(self, word):
        self.word = word #word itself
        self.synset_pack = None #list of 'SynsetData' objects or #list of 'RefiData' objects depending if the model is provided
        self.prime_sys = None #the 'PrimeData' containing SynsetID, Offset and POS for later retrieval   

#prime 'SynsetData'(prime_sys) in  'WordsData'   
class PrimeData(object):
    def __init__(self, psys_id, poffset, ppos):
        self.psys_id = psys_id
        self.poffset = poffset
        self.ppos = ppos      

#Document Wrapper
class DocData(object):
    def __init__(self):
        self.wordsdata = None


       