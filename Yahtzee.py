"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
July 7, 2014
Kaili Liu
"""

# Used to increase the timeout, if necessary
import random
import codeskulptor
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    hiscore_class = []    
    for item in hand:
        the_sum = hand.count(item) * item
        hiscore_class.append(the_sum)
                        
    return max(hiscore_class)


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value of the held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """

    total_score = 0.0
    outcomes = range(1, num_die_sides+1)
    all_outcomes = gen_all_sequences(outcomes, num_free_dice)
    for hand in all_outcomes:
        newhand = hand + held_dice
        total_score += score(newhand)   
    return float(total_score) / float(len(all_outcomes))



    
def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    answer_set = set([()])
    for item in list(hand):
        temp_set = set()
        for partial_sequence in answer_set:
            for num in [0,1]:
                if num:
                    new_sequence = list(partial_sequence)
                    temp_set.add(tuple(new_sequence))
                else:
                    temp_set.add(partial_sequence+(item,)) 
        answer_set = temp_set
    return answer_set

def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    high_exp = 0.0
    high_play = ()
        
    all_seqs = gen_all_holds(hand)
    for item in all_seqs:
        exp_val = expected_value(item, num_die_sides, len(hand) - len(item))
        if exp_val > high_exp:
            high_exp = exp_val
            high_play = item

    return (high_exp, high_play)


    

def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
    
#run_example()


#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)

#import user35_uLOFnLQSJV29rFh_5 as expected_value_testsuite
#expected_value_testsuite.run_suite(expected_value)                                       