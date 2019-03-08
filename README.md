#BSD_Extractor
=======================================

Transforms raw-text files into their disambiguated Synset versions, producing a file with the following content structure:

word \t synset \t \offset \t pos For all the words that exist in wordnet (except stopwords)

A list of these new files is also produced.

The program uses Python 3.X, Wordnet 3.0 (from nltk library), numpy, functools and a trained word embeddings model (binary or not).

Transforms text files into synset word files considering WSD via glosses

COMMAND LINE (wn_manage.py) :
==============
	python3 wn_manage.py  --input <input-location> --output <output-location> --recur <bool> --abase <bool> --model <model-file>

- <--input> : Input folder with .txt files or folders with .txt
- <--output>: Ouput folder where the files will be saved
- <--recur> : [OPTIONAL  and case sensitive] True (default): Use synset-embeddings (trained on the output of this algorithm); False: Use word-embeddings (e.g. GoogleNews);
  - Important: The synset embeddings consider this structure *word#offset#pos* as keys. However, to make things more flexible, the ouput of this program produces *word\tsynset\toffset\tpos*. Pleave refer to BSD_Parser to filter/parser the components you require;
- <--abase> : [OPTIONAL and case sensitive] True (default): Disambiguation via Base MSSA; False - Disambiguation via Dijkstra;
- <--model>: Word-Embedding (e.g. GoogleNews) OR Synset-Embbedding model used. This should be in .vector format, but it can be changed to binary. Synset-Embbeddings consider the following canonical format: *word#offset#pos* . These are the keys to look up the embeddings.

UPDATES:
==========
[2019-03-07]
1. Moving project from personal repository and renaming it

[2019-01-31]
1. CommandLine class implemented - Refactor

[2019-01-11]
1. Ignore ASCII error when reading and cleaning files

[2018-12-06]
1. Refinement script removed. Everything is done via command line using wn_manage.py only
2. New instructions added on how to run
3. General refactoring
4. Enhancement: Gloss-avg-vect was being calculated regardless if recurrent/refinement model was used (synset-embeddings). It doesn't affect the result, but add substantial computing time.
5. Left some toy input files for testing

[2018-05-14]
1. Several refactoring performed
2. If document parsed has not synset-tokens, this document won't be produced (output file is discarded)
3. Dijkstra with Refinement model implemented

[2018-05-09]
1. Fix: If document has only one word we pick the Most Common Sense  (MCS) to represent that word (single-word-document). Only for normal approach (wn_manage.py - uses word2vec)
2. To-Do: Implement the same thing for refinement approach (refi_manage - uses synset2vec)

[2018-04-24]
1. Circular references fixed
2. No need to use PYTHONPATH=.. anymore
3. adjust on import modules
4. Pytho path fixed

[2018-04-24]
1. refi_manage.py included. Works in the same way as 'wn_manage', but uses the synset_vector (synset2vec) for the words in the input text
2. Model used for 'refi_manage' has to be in the format of synset2vec (word#offset#pos)
3. Minor errors on Dijkstra approach fixed - cost function altered to distance instead of similarity

[2018-03-30]
1. Improved method for reading/cleaning text input
2. Code working with multiple-folder-input (folder inside folder with input files) - files/input holds a toy example which can be executed directly
3. fname_splitter for UNIX and WINDOWS structure
4. Refactored in some items

[2018-03-12]
1. PYTHONPATH=.. must be used in command line to avoid problems with local-import between packages
2. folders with input;folder;model must be under synset_module/ to run with command-line
3. If nltk-wordnet is not install run python3 import nltk nltk.download('wordnet') or include it in the program 
			
[2018-03-02] 
CosineDistance for Dijsktra; CosineSimilarity for Window-context; Implemented INDEX-COST look-up table based on a mapping created from the Wordnet dictionary using a Crystal program (look at Block BETA (wn_manage.py) and distance_reader.py for details)

[2018-03-01] Dijkstra implemented for disambiguating word-synset-nodes based on cosine distance (using priority queue) ;Synset disambiguation based on window-word context [-/+1]; Numpy applied to vector operations (averaging gloss-vector); CosineDistance/CosineSimilarity updated; Execution time (naive) for control issues
			