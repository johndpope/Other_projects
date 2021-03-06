# The system accepts two different text articles and extract several similarity measures, thus it belongs to the field of text processing. 
# In more details the steps of the algorithm are: 
# 	1) It reads a number of files containing pairs of texts
#	2) It pre-processes the texts. The current version supports greek as the language of the text, therefore, it removes accents, capitalises letters, removes the numbers and the english characters.
#	3) It stems the texts.
#	4) It extracts the similarity measures.
# There is optionally the function create_lemmas in case there is no predefined dictionary. 
#
#
# Copyright (C) 2014 Grigorios G. Chrysos
# available under the terms of the Apache License, Version 2.0

import clear_and_stem
import compare_per_two
import warnings

folder = 'text_files/'


for fileIn in ['Epistimi-Total.csv']:		# all files that we want to process, compare pairs of texts
    separ = fileIn.find('.')
    print 'The file ' + fileIn[:separ] + ' will be processed now'
    stemmed_file = fileIn[:separ]+'-2'+fileIn[separ:]
    similar_file = fileIn[:separ]+'-3'+fileIn[separ:]
    print 'Pre-processing and stemming ...'
    with warnings.catch_warnings():                                         # Just to ignore Unicode warnings
        warnings.simplefilter("ignore")
        clear_and_stem.stem_file(folder+fileIn, folder+stemmed_file, '~')
    print 'Comparing news per two ...'
    compare_per_two.text_similarities(folder+stemmed_file, folder+similar_file, '~')
    print 'Done for ' + fileIn[:separ]

