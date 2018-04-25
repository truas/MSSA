'''
@author Goran Topic - 2018/02/25
@altered Terry Ruas - 2018/03/01

python interface that uses distances.bin (binary) and distances.index (index)
to map the shortest distance between two synset nodes [pos_1, offset_1][pos_2, offset_2]

These distances are calculated using Crystal (language) that reads the Wordnet dictionary
calculating the shortest path (Dijsktra) between two synset-nodes using any link from
one synset to the other. 

* To build the program execute: 'shards build' under the main folder
* To create the bin/index execute:  'bin/wordnet_distances'

The  cost(weight) and depth (limit) can be tuned in the config.yaml file where all definitions
are located. If any configuration is altered the bin/index have to be recreated.
This might take a long time: 117,000 need to be traversed (for WordNet 3.0 dictionary) 

Inside /python the .py code to access the binindex is provided with 
a sample example on how to retrieve the distance between two nodes.  
'''

DISTANCES_files_path = 'C:/tmp_datasets/Wordnet/dict_map'


import struct
from nltk.corpus import wordnet as wn

def readstruct(f, s, n=None):
    if n is not None:
        return s.iter_unpack(f.read(s.size * n))
    else:
        return s.unpack(f.read(s.size))
    
#class-object that loads the index and binary files with wordnet map distances
class DistanceReader:
    S_IDX_NUM_SYNSETS = struct.Struct('=i')
    S_IDX_SYNSET = struct.Struct('=icq')

    S_DIST_HEADER = struct.Struct('=ici')
    S_DIST_DISTS = struct.Struct('=icf')

    def __init__(self, dist_file, index_file):
        self.dist_file = dist_file
        self.index = {}
        with open(index_file, 'rb') as f:
            num_synsets, = readstruct(f, self.S_IDX_NUM_SYNSETS)
            for synset_idx in range(num_synsets):
                offset, pos, loc = readstruct(f, self.S_IDX_SYNSET)
                self.index[pos.decode('us-ascii'), offset] = loc

    def __getitem__(self, pos_offset):
        pos, offset = pos_offset
        loc = self.index[pos, offset]
        result = { pos_offset: 0 }
        with open(self.dist_file, "rb") as f:
            f.seek(loc)
            r_offset, r_pos, num_dists = readstruct(f, self.S_DIST_HEADER)
            for target_offset, target_pos, dist in readstruct(f, self.S_DIST_DISTS, num_dists):
                result[pos, target_offset] = dist
        return result

    @staticmethod
    def between(distances1, offset2, pos2):
        return distances1.get((offset2, pos2), float('inf'))

#===============================================================================
# TEST CASES for distance_reader
#===============================================================================
#if __name__ == '__main__':
    #import os.path
    #script_dir = os.path.dirname(os.path.abspath(__file__)) #if the file is in the same folder as the program
    #w1 = wn.synsets('chocolate')[0]  # @UndefinedVariable
    #w2 = wn.synsets('coffee')[0]  # @UndefinedVariable
    
    #dr = DistanceReader(DISTANCES_files_path + "/distances.bin", DISTANCES_files_path + "/distances.idx")
    #w1_dists = dr['n', w1.offset()]
    #print(w1_dists[w2.pos(),w2.offset()])
    #dist_to_w2 = DistanceReader.between(w1_dists, 'n', w2.offset())
    
    #dr['n', w1.offset()]['n', w2.offset()]
    #print('Distance between ', w1.name(),'and ',  w2.name(), ' : %s' % dr['n', w1.offset()]['n', w2.offset()])
    #print("Distance between %s and %s: %s" % (w1_dists, w2, dist_to_w2))
#===============================================================================
# TEST CASE for distance_reader
#===============================================================================
#===============================================================================
# if __name__ == '__main__':
#     import os.path
#     script_dir = os.path.dirname(os.path.abspath(__file__))
#     dr = DistanceReader(script_dir + "/../distances.bin", script_dir + "/../distances.idx")
# 
#     from nltk.corpus import wordnet as wn
# 
#     while True:
#         w1 = input("W1: ")
#         w1s = wn.synsets(w1)
#         if w1s:
#             break
#         else:
#             print("Unknown word, please enter again")
#     while True:
#         w2 = input("W2: ")
#         w2s = wn.synsets(w2)
#         if w2s:
#             break
#         else:
#             print("Unknown word, please enter again")
# 
#     results = []
#     for s1 in w1s:
#         try:
#             dt = dr[s1.pos(), s1.offset()]
#             for s2 in w2s:
#                 d = dr.to(dt, s2.pos(), s2.offset())
#                 results.append((d, s1, s2))
#         except KeyError:
#             print("No record of distances for %s" % s1)
#     results.sort()
#     for dist, s1, s2 in results:
#         print("%s\n%s\n%s\n" % (dist, s1.definition(), s2.definition()))
#===============================================================================
