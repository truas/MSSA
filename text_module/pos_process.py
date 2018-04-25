'''
@author: Terry Ruas 2018-03-12

'''

def bsid_ouput_file(words_data, bsd_fname, bsd_folder):  
    #print('Saving %s Document' %bsd_fname)
    bsd_doc = open(bsd_folder +'/'+ bsd_fname, 'w+')  
    #currently using just Word \t SynsetID \t offset  \t pos
    for wd_element in words_data:
        bsd_doc.write(wd_element.word +'\t'+ str(wd_element.prime_sys.psys_id) +'\t'+ str(wd_element.prime_sys.poffset) +'\t'+ wd_element.prime_sys.ppos + '\n')
    bsd_doc.close()
    #print('%s Document saved' %bsd_fname)  
#save each document(word, synset, offset, pos)