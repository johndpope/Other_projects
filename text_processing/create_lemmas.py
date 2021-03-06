# greg, 2 August 2014: Creates a list with all the lemmas found in the *.csv files of news articles.
# Call: python create_lemmas.py '[name_of_input_file]'
# Similarity with clear_and_stem.py in the stemming part.
#
#
# Copyright (C) 2014 Grigorios G. Chrysos
# available under the terms of the Apache License, Version 2.0

import csv
import unicodedata  # for removing accents
import re
import stemming as stem
import sys


# function that removes the accents from strings (including greek characters) from http://stackoverflow.com/a/518232/1716869
def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')


# check whether a string contains a number
_digits = re.compile('\d')
def contains_digits(d):
    return bool(_digits.search(d))


def search_and_create_data(fileIn,data):
    csv.register_dialect('perispwmeni', delimiter='~')
    f = open(fileIn, 'r')
    try:
        reader = csv.reader(f, dialect='perispwmeni')

        cnt_row = 0
        new_data = []
        for row in reader:  # reads per line
            #print row
            cnt_row = cnt_row +1
            if len(row)>1:                                  # if len(row) == 1, then it is an empty line, skip it
                for elem in [5, 6]:                         # The text (news articles) is in columns 6,7 in the current format
                    line1 = row[elem]
                    words = line1.split()
                    for word in words:                      # loop over each element of list "words"
                        ww = stem.get_decoded_input(word)   # it was 'str' before and becomes 'unicode' from type (ww)
                        last_char_spec =''.encode('utf-8')
                        last_char = ww[-1]                          # if the last character is a special
                        if last_char == ',' or last_char == '.' or last_char == '!' or last_char == ';':    # char (',','.','!',';'), we trim it
                            ww = ww[:-1]
                            #last_char_spec = last_char.encode('utf-8')
                        if len(ww) <= 4:                      # cut down the articles and small words
                            continue
                        ww = strip_accents(ww)
                        english_char = re.search('[a-zA-Z]', ww)    # Check whether the word contains English characters
                        cont_dig = not contains_digits(ww)
                        if (not ww[0].isupper()) and (english_char is None) and cont_dig:
                        # if the first letter is capital, it contains English characters or it is a number,
                        # then we don't want to stem it
                            ww = ww.upper()
                            stemmed = stem.stem(ww)
                            stemmed = stemmed.lower()
                            stemmed = stemmed.encode('utf-8')
                            try:                                    # try to locate the word in the current list
                                data.index(stemmed)
                            except:
                                try:                                # try to locate the word in the new list
                                    new_data.index(stemmed)
                                except:                             # if it's not in neither of them, append it to the new list
                                    new_data.append(stemmed)
                                    print stemmed
    finally:
        f.close()
    return new_data


def write_data(fileIn):
    name_lemma = 'text_files/lemmas.dict'
    try:
        f_r = open(name_lemma, 'r+')
        data = f_r.read().split('\n')
    except:
        f_r = open(name_lemma, 'w')
        data = []
    finally:
        new_data = search_and_create_data(fileIn,data)
        f_r.write('\n'.join(new_data)) # write in a text file, one word per line
        f_r.close()


# call from terminal with full argument list:
if __name__ == '__main__':
    args = len(sys.argv)
    if args < 1:
        print "Not enough arguments for selecting an option in " + sys.argv[0]
        print "We need one argument in this function,  the input file with the news (csv format)"
        raise Exception()
    write_data(sys.argv[1])
