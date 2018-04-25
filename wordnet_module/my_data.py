'''
@author: Terry Ruas 2018-03-12
'''
from functools import total_ordering

#'DefiData' object in the 'WordsData' (drefi) class
@total_ordering
class DefiData(object): 
    def __init__(self, sys_id, offset, pos, gloss):
        self.sys_id = sys_id
        self.offset = offset
        self.pos = pos
        self.gloss = gloss
        self.gloss_avg_vec = list() #the average vector fo that word-synset gloss
    
    #Necessary methods to implement heapq from 
    def __eq__(self, other):
        return False
    def __lt__(self, other):
        return self.offset < other.offset

class RefiData(object): 
    def __init__(self, sys_id, offset, pos):
        self.sys_id = sys_id
        self.offset = offset
        self.pos = pos
        self.vector = [] #embedding of that given word-offset-pos
        
#'WordsData' object for word in a 'Document'
class WordsData(object):
    def __init__(self, word):
        self.word = word #word itself
        self.drefi = None #list of 'DefiData' objects or #list of 'RefiData' objects depending if the model is provided
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


       