"""
April 12, 2014
Kaili Liu
"""
# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
import random
import math

# initialize global variables used in your code
num_range = 100
num_guesses = 7
secret_number = 0


# helper function to start and restart the game
def new_game():
    global num_guesses
    global num_range
    global secret_number    
    if num_range == 100:
        num_guesses = 7
        secret_number = random.randrange(0, 100)
        print ""
        print "New game. Range is from 0 to 100."
        print "Number of remaining guesses is 7."
    elif num_range == 1000:
        num_guesses = 10
        secret_number = random.randrange(0, 1000)
        print ""
        print "New game. Range is from 0 to 1000."
        print "Number of remaining guesses is 10."

# define event handlers for control panel
def range100():
    global num_guesses
    global num_range
    global secret_number 
    num_range = 100
    num_guesses = 7
    new_game()   
  

def range1000():   
    global num_guesses
    global num_range
    global secret_number
    num_range = 1000
    num_guesses = 10
    secret_number = random.randrange(0, 1000)
    print ""
    print "New game. Range is from 0 to 1000."
    print "Number of remaining guesses is 10."

    
def input_guess(guess):
    # main game logic goes here
    global secret_number
    global num_guesses
    guess = int(guess)
    print ""
    print "Guess was", guess
    num_guesses = num_guesses - 1
    print "Number of guesses remaining is", num_guesses 
    
    if guess == secret_number:
        print "Correct!"
        new_game()        
    elif num_guesses == 0:
        print "You ran out of guesses. The number was", secret_number
        new_game()    
    elif guess > secret_number:
        print "Lower."        
    elif guess < secret_number:
        print "Higher."
         
    
# create frame
frame = simplegui.create_frame("Guess the Number", 200, 200)


# register event handlers for control elements
frame.add_button("Range is 0 to 100", range100, 200)
frame.add_button("Range is 0 to 1000", range1000, 200)
frame.add_input("Enter your guess here:", input_guess, 200)


# call new_game and start frame
new_game()
frame.start()
