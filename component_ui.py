'''

@author: jrosner
'''

import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--input',  
                    required=True, 
                    help='the input bam file')

parser.add_argument('--output',  
                    required=True, 
                    help='the output bam file')

parser.add_argument('--options',
					default=None,
					help='please specify the options for view ')


args, unknown = parser.parse_known_args()
