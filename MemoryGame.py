"""
Kaili Liu
May 3, 2014
"""
# implementation of card game - Memory

import simplegui
import random

# global variables
card_deck = range(0, 8) + range(0, 8)
exposed = [False for num in card_deck]
card_state = 0
card1_num = 0
card2_num = 0
Turns = 0

# helper function to initialize globals
def new_game():
    global card_deck, Turns, exposed, card_state
    random.shuffle(card_deck)   
    Turns = 0
    exposed = [False for num in card_deck]
    label.set_text('Turns ='+ str(Turns))
    card_state = 0

     
# define event handlers
def mouseclick(position):
    # add game state logic here
    global exposed, card_state, card1_num, card2_num, Turns
    index = position[0]//50        
    if exposed[index] == False:
        exposed[index] = True 
        if card_state == 0:
            card_state = 1
        elif card_state == 1:
            card_state = 2
            Turns += 1
            label.set_text('Turns ='+ str(Turns))
        else:             
            if card_deck[card1_num] == card_deck[card2_num]:                
                exposed[card1_num] = True
                exposed[card2_num] = True
                card_state = 1                
            else:
                exposed[card1_num] = False
                exposed[card2_num] = False
                card_state = 1
        card2_num = card1_num
        card1_num = index
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global card_deck, exposed
    for num in range(16):
        if exposed[num] == True:
            canvas.draw_text(str(card_deck[num]), ((num*50)+13, 70), 60, 'White')
        else:
            canvas.draw_polygon([((50*num), 0),((50*(num+1)), 0), ((50*(num+1)), 99), ((50*num), 99)], 5, 'Yellow', 'Navy')

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric