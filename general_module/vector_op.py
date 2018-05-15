'''
@author: Terry Ruas 2018-03-12

'''
import numpy
import sys
import random
from scipy import spatial
from heapq import heappush, heappop

#Global - Definitions
PRECISION_COS = 7

#self-packages
import wordnet_module.my_data as md
import wordnet_module.synset_tracker as st
#from wordnet_module.my_data import PrimeData

#===============================================================================
# NewBSD  and DijkstraBSD
#===============================================================================
def make_bsd(words_data, refi_flag = False):
    last_index = (len(words_data)-1)
    
    if(len(words_data)==1):#if single-word-document pick MCS to represent it
        only_sys = st.synset_all(words_data[last_index].word)
        sys = md.PrimeData(only_sys[0], only_sys[0].offset(), only_sys[0].pos())
        words_data[last_index].prime_sys = sys
    else:
        for index, wd in enumerate(words_data):
            current = wd.synset_pack
            alfa = 0.0
            beta = 0.0
            #prepare former, latter and current wordsdata to be evaluated
            if (index > 0) and (index < last_index ) : #middle words
                former = words_data[index-1].synset_pack
                latter = words_data[index+1].synset_pack
             
                alfa, sys_a = synset_data_handler(current, former, refi_flag)
                beta, sys_b = synset_data_handler(current, latter, refi_flag)
            
            elif index == 0: #first word
                #former = None
                latter = words_data[index+1].synset_pack
                alfa, sys_a = synset_data_handler(current, latter, refi_flag)
       
            else:#last word
                #latter = None
                former = words_data[index-1].synset_pack
                alfa, sys_a = synset_data_handler(current, former, refi_flag)
    
            #pick the highest cosine-prime_obj   
            if alfa > beta:
                sys = sys_a
            elif beta > alfa:
                sys = sys_b
            else:
                pick_random = [sys_a, sys_b]
                sys = random.choice(pick_random)
            
            wd.prime_sys = sys
        
    return(words_data)    
#evaluates which SID represents a word considering its context of +1 and -1
#refi_flag indicates if algorithm will consider the (defi) gloss-average vector (using raw-words model) or
#it will consider (refi) synsets model (synset2vec)

def make_bsd_dijkstra(words_data, refi_flag=False):
    queue = [] #[] literal is faster than list[] in theory
    seen = set() #visited nodes
    num_words = len(words_data)

    for defi_initial in words_data[0].synset_pack:#node containing DefiData(Synset,offset,pos,gloss,average_gloss
        heappush(queue, (0, 0, [defi_initial])) # (queue,(weight, word_no, path)) - put the first word-node in the queue heap
        
    while queue:#as long we have something on the queue do
        weight, word_no, path = heappop(queue) #Pop and return the smallest item from the heap (based on the weight-cost), maintaining the heap invariant
        node_id = (word_no, path[-1].offset, path[-1].pos) #make a tuple of the word_no:offset:pos from the current node being evaluated

        if node_id in seen: #if the current node (poped out from the queue) was already seen continue to the next node
            continue
       
        seen.add(node_id) #else: add the current node as evaluated
        word_no += 1 #move to the next node
        
        if word_no == num_words: #found shortest path - if we are the last word-node, all of them were visited
            for word, synset_final in zip(words_data, path): #we zip the build shortest path with the words-node to retrieve the words-synset-features: synset id (lowest weight-cost), offset, pos
                word.prime_sys = md.PrimeData(synset_final.sys_id, synset_final.offset, synset_final.pos)
            return words_data #return the word-node with its PrimeData representation
        #else: calculate the weight (cosine) from the current discovered path and update
        for synset_final in words_data[word_no].synset_pack: #for all DefiData(synsets-gloss-avg) in the current node
            if refi_flag:
                pencil = path[-1].vector
                needle = synset_final.vector
            else:
                pencil = path[-1].gloss_avg_vec
                needle = synset_final.gloss_avg_vec
            diff = cosine_distance(pencil, needle) #cost from previous node to new node 
            
            heappush(queue, (weight + diff, word_no, path + [synset_final]))#put in the queue-heap the updated cost for the word node 
    print('Something went wrong while Dijkstra was running...')
#decides the lowest path-cost from the first word to the last in the document -kind of 'global chain'
#it takes into account the cosine-distance as cost (weight) in the edges from word to word
#uses Dijkstra's Algorithm

#===============================================================================
# HANDLERs
#===============================================================================

def synset_data_handler(prime, not_prime, refi_flag):
    highest_so_far = sys.float_info.min #value of dist.cost (1 - cosine.similarity) to initialize    
    sys_prime = prime[0].sys_id #just give a Synset to initialize it
    offset_prime = prime[0].offset
    pos_prime = prime[0].pos
    
    #keep the synsetdata with the highest cosine
    for current in prime:
        for evaluated in not_prime:
            
            if refi_flag:
                needle = current.vector
                pencil = evaluated.vector
            else:
                needle = current.gloss_avg_vec
                pencil = evaluated.gloss_avg_vec  
             
            tmp_highest = cosine_similarity(needle, pencil) #using gloss-average cosine
            
            if tmp_highest > highest_so_far:
                highest_so_far = tmp_highest
                sys_prime = current.sys_id
                offset_prime = current.offset
                pos_prime = current.pos
    
    prime_obj = md.PrimeData(sys_prime, offset_prime, pos_prime)
    return (highest_so_far, prime_obj)


#===============================================================================
# Vector Operations - Similarity and distance
#===============================================================================
def cosine_similarity(v1, v2):
    if not numpy.any(v1) or not numpy.any(v2): return(0.0) #in case there is an empty vector we return 0.0
    cos_sim = 1.0 - round(spatial.distance.cosine(v1, v2), PRECISION_COS)
    #if math.isnan(cos_dist): cos_dist = 0.0  #just to avoid NaN on the code-output for the cosine-dist value -  some word vectors might be 0.0 for all dimensions
    return (cos_sim)
#cosine distance for v1 and v2 with precision of PRECISION_COS
#spatial.distance.cosine(v1, v2) gives distance, so 1 - X; will give similarity - so the highest the value the more similar two vectors are

def cosine_distance(v1, v2):
    if not numpy.any(v1) or not numpy.any(v2): return(0.0) #in case there is an empty vector we return 0.0
    cos_dist = round(spatial.distance.cosine(v1, v2), PRECISION_COS)
    #if math.isnan(cos_dist): cos_dist = 0.0  #just to avoid NaN on the code-output for the cosine-dist value -  some word vectors might be 0.0 for all dimensions
    return (cos_dist)
#get the distance of two vectors: heapp pos the lowest value so distance is required
