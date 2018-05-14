'''
@author: Terry Ruas 2018-03-12

'''
import sys
import random
from heapq import heappush, heappop

#Global - Definitions

#self-packages
import wordnet_module.my_data as md



def bsd_dijkstra_index(words_data, index_cost):
    queue = list() #[] literal is faster
    seen = set() #visited nodes
    num_words = len(words_data)
    #object that contains the index
    
    for defi_initial in words_data[0].synset_pack:#node contianing DefiData(Synset,offset,pos,gloss,average_gloss
        heappush(queue, (0, 0, [defi_initial])) # (queue,(weight, word_no, path)) - put the first word-node in the queue heap
        
    while queue:#as long we have something on the queue do
        weight, word_no, path = heappop(queue) #Pop and return the smallest item from the heap (based on the weight-cost), maintaining the heap invariant
        node_id = (word_no, path[-1].offset, path[-1].pos) #make a tuple of the word_no:offset:pos from the current node being evaluated
              
        if node_id in seen: #if the current node (poped out from the queue) was already seen continue to the next node
            continue
       
        seen.add(node_id) #else: add the current node as evaluated
        word_no += 1 #move to the next node
        
        if word_no == num_words: #found shortest path - if we are the last word-node, all of them were visited
            for word, defi_final in zip(words_data, path): #we zip the build shortest path with the words-node to retrieve the words-synset-features: synset id (lowest weight-cost), offset, pos
                word.prime_sys = md.PrimeData(defi_final.sys_id, defi_final.offset, defi_final.pos)
            return words_data #return the word-node with its PrimeData representation
        
        from_node_map = validate_map_dimension(path[-1].pos, path[-1].offset, index_cost) #retrieve synset from index-cost map
        
        for defi_final in words_data[word_no].synset_pack: #for all DefiData(synsets-gloss-avg) in the current node
            #diff = cosine_distance(path[-1].gloss_avg_vec, defi_final.gloss_avg_vec) #cost from previous node to new node 
            
            if from_node_map is False:
                diff = 10.0
            else:
                diff = cost_map_nodes(from_node_map, defi_final.pos, defi_final.offset) #retrieve the target
            heappush(queue, (weight + diff, word_no, path + [defi_final]))#put in the queue-heap the updated cost for the word node 
    print('Something went wrong while Dijkstra was running...')
#decides the lowest path-cost from the first word to the last in the document
#it takes into account the cosine-distance as cost (weight) in the edges from word to word
#uses Dijkstra's Algorithm

def bsd_index(words_data, index_cost):
    last_index = (len(words_data)-1)
    for index, wd in enumerate(words_data):
        current = wd.synset_pack
         
        alfa = 1.0
        beta = 1.0
                    
        #prepare former, latter and current wordsdata to be evaluated
        if (index > 0) and (index < last_index ) : #middle words
            former = words_data[index-1].synset_pack
            latter = words_data[index+1].synset_pack
            alfa, sys_a = defidata_index_handler(current, former, index_cost)
            beta, sys_b = defidata_index_handler(current, latter, index_cost)  
        elif index == 0: #first word
            #former = None
            latter = words_data[index+1].synset_pack
            alfa, sys_a = defidata_index_handler(current, latter, index_cost)           
        else:#last word
            #latter = None
            former = words_data[index-1].synset_pack
            alfa, sys_a = defidata_index_handler(current, former, index_cost)
 
        #pick the highest cosine-prime_obj   
        if alfa < beta:
            sys = sys_a
        elif beta < alfa:
            sys = sys_b
        else:
            pick_random = [sys_a, sys_b]
            sys = random.choice(pick_random)
        
        wd.prime_sys = sys
        
    return(words_data)    
#evaluates which SID represents a word considering its context of +1 and -1
#here the cosine is not used so we wnat the lowest cost from one node to the other

def cost_map_nodes(map_cost_current, next_pos, next_offset): #map_cost_current[sys_id.pos,sys_id.offset][required]
    try:
        travel_cost = map_cost_current[next_pos, next_offset]  
    except KeyError:
        travel_cost = 10.0 #high travel-cost since it is not mapped on binary/index
    return(travel_cost)    
#returns the lowest path cost between synsets, if there is none float '10.0' is returned
#the map_cost_current already has the first dimension from the mapping 

def defidata_index_handler(prime, not_prime, index_cost):
    lowest_so_far = sys.float_info.max  
    sys_prime = prime[0].sys_id #just give a Synset to initialize it
    offset_prime = prime[0].offset
    pos_prime = prime[0].pos
    
    #keep the synsetdata with the highest cosine
    for current in prime:
        cost = validate_map_dimension(current.pos, current.offset, index_cost)
        if cost is False:
            tmp_lowest = 10.0
        else:            
            for evaluated in not_prime:
                tmp_lowest = cost_map_nodes(cost, evaluated.pos, evaluated.offset) #cost of synset passed in 'cost' and 'evaluated'
                if tmp_lowest <= lowest_so_far:
                    lowest_so_far = tmp_lowest
                    sys_prime = current.sys_id
                    offset_prime = current.offset
                    pos_prime = current.pos
    
    prime_obj = md.PrimeData(sys_prime, offset_prime, pos_prime)
    return (lowest_so_far, prime_obj)
#Given two DefiData it returns the 'Synset' for the 'current' with the highest cosine dist value

def validate_map_dimension(pos, offset, cost_map):
    try:
        valid_dim = cost_map[pos, offset]
    except KeyError:
        valid_dim = False
    return(valid_dim)
#verifies if the first synset exist in the index