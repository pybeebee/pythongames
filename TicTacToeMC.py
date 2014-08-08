"""
Monte Carlo Tic-Tac-Toe Player
June 29, 2014
Kaili Liu
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# Change as desired
NTRIALS = 100   # Number of trials to run
MCMATCH = 1.0  # Score for squares played by the machine player
MCOTHER = 1.0  # Score for squares played by the other player


# Add your functions here.
def mc_trial(board, player):
    """
    This function modifies the board input.
    """
    current_player = player
    while board.check_win() == None:
        choice_list = board.get_empty_squares() 
        spot_choice = choice_list[random.randrange(len(choice_list))]        
        board.move(spot_choice[0], spot_choice[1], current_player)
        current_player = provided.switch_player(current_player)


def mc_update_scores(scores, board, player):
    """
    This function scores the completed board and updates the scores grid.
    """
    dimensions = board.get_dim()
    for row in range(dimensions):
        for column in range(dimensions):
            if board.check_win() == player:
                if board.square(row, column) == player:
                    scores[row][column] += MCMATCH
                elif board.square(row, column) == provided.switch_player(player):
                    scores[row][column] -= MCOTHER            

            elif board.check_win() == provided.switch_player(player):
                if board.square(row, column) == player:
                    scores[row][column] -= MCMATCH
                elif board.square(row, column) == provided.switch_player(player):
                    scores[row][column] += MCOTHER
            
                
def get_best_move(board, scores):
    """
    This function finds all of the empty squares with the maximum score and 
    randomly returns one of them as a (row, column) tuple.
    """   
    poss_sqrs = []
    max_score = -1000
    emp_sqr_places = board.get_empty_squares()          
    
    if len(emp_sqr_places) == 0:
        return (0, 0)
    for item in emp_sqr_places: 
        value = scores[item[0]][item[1]]
        if value > max_score:
            max_score = value
            
    for item in emp_sqr_places:
        value = scores[item[0]][item[1]]
        if value == max_score:
            poss_sqrs.append(item)
    
    the_index = random.randrange(len(poss_sqrs))
    return poss_sqrs[the_index]       
        
def mc_move(board, player, trials):
    """
    This function uses the Monte Carlo simulation to return a move for the 
    machine player in the form of a (row, column) tuple.
    """    
    scores = [[0 for dummy_row in range(board.get_dim())] for dummy_column in range (board.get_dim())]   

    for dummy_item in range(trials):
        the_clone = board.clone()
        mc_trial(the_clone, player)
        mc_update_scores(scores, the_clone, player)    
    return get_best_move(board, scores)

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.


#provided.play_game(mc_move, NTRIALS, False)        
#poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
