import pandas as pd
import glob
from re import sub

dct = {
    'sentence': [],
    'label': []
}


for filename in glob.glob('sentence_labels/*.txt'):
    


    f = open(filename, 'r')
    
    filename = filename[filename.find('\\') + 1:filename.find('.')]

    d = open('md/{}.md'.format(filename), 'w')
    
    d.write('## intent:tt8613070\n')

    for line in f:

        
        if len(line.split()) < 4 or len(line.split()) > 20:
            continue

        d.write('- {}'.format(line))


