import argparse
import distutils.util as util

class CommandLine:
    input_folder = None
    output_folder = None
    model_folder = None
    recur_typee = None
    abase_type = None
    
    def __init__(self):
        parser = self.commandLineParameters()
        args = parser.parse_args()
        self.input_folder = args.inf
        self.output_folder = args.ouf
        self.model_folder = args.mod
        self.recur_type = args.rec
        self.abase_type = args.aba
    #constructor for parameters

    def commandLineParameters(self):
        parser = argparse.ArgumentParser(description="BSD_Extractor - Transforms text into synsets")
        parser.add_argument('--input', type=str, action='store', dest='inf', metavar='<folder>', 
                            required=True, help='input folder to read document(s)')
        parser.add_argument('--output', type=str, action='store', dest='ouf', metavar='<folder>', 
                            required=True, help='output folder to write document(s)')
        parser.add_argument('--model', type=str, action='store', dest='mod', metavar='<parameter>', 
                            required=True, help='trained word embeddings model')
        parser.add_argument('--recur', type=util.strtobool, action='store', dest='rec', metavar='<parameter>', 
                            required=False, help='[optional] selects type of embeddings is use: [false] word-based or [true] synset-based <default>',choices=[True, False])
        parser.add_argument('--abase', type=util.strtobool, action='store', dest='aba', metavar='<parameter>', 
                            required=False, help='[optional] selects between [true] Base algorithm <default> or [false] Dijkstra', choices=[True, False])  
        
        return(parser)
    #parameter list for command line