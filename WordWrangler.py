"""
Student code for Word Wrangler game
July 22, 2014
Kaili Liu
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists
# PHASE 1: function 1
def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    nodups_list = []
    coplist = list(list1)
    for item in coplist:
        count = coplist.count(item)
        while count > 1:
            coplist.pop(coplist.index(item))
            count = coplist.count(item)
        if count == 1:
            nodups_list.append(item)
    
    return nodups_list


# PHASE 1: function 2
def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    newlist = []
    for item in list1:
        if item in list2:
            newlist.append(item)
                                       
    return newlist


# Functions to perform merge sort
# PHASE 2: function 1
def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing all of the elements that
    are in either list1 and list2.

    This function can be iterative.
    """
    coplistone = list(list1)
    coplisttwo = list(list2)
    new_list = []
    while (len(coplistone) > 0) and (len(coplisttwo) > 0):
        element_one = coplistone[0]
        element_two = coplisttwo[0]
        
        if element_one < element_two:            
            new_list.append(coplistone.pop(0))
            
        elif element_two < element_one:            
            new_list.append(coplisttwo.pop(0))
            
        elif element_one == element_two:            
            new_list.append(coplistone.pop(0))            
            new_list.append(coplisttwo.pop(0))
                    
    if len(coplistone) > 0:        
        new_list.extend(coplistone)
    elif len(coplisttwo) > 0:
        new_list.extend(coplisttwo)
        
    return new_list


#PHASE 2: function 2
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    if len(list1) <= 1:
        return list1
    else:
        hlone_length = len(list1) // 2 
        half_list_one = list1[ : hlone_length]
        half_list_two = list1[hlone_length : ]
        return merge(merge_sort(half_list_one), merge_sort(half_list_two))




# Function to generate all strings for the word wrangler game
# PHASE 3: function 1
def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    ans_list = []
    if len(word) == 0:
        ans_list.append('')
        
    elif len(word) > 0:        
        first = word[0]
        rest = word[1 : len(word)]
        rest_strings = gen_all_strings(rest)
        ans_list.extend(rest_strings)
        for string in rest_strings:
            for pos in range(len(string)):
                ans_list.append(string[ : pos] + first + string[pos : ])
            ans_list.append(string + first)
            
    return ans_list

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    string_list = []
    url = codeskulptor.file2url(filename)
    the_file = urllib2.urlopen(url)
    for line in the_file.readlines():
        the_line = line[:-1]
        string_list.append(the_line)
    return string_list

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
# run()
 
    
