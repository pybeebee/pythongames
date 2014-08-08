"""
April 5, 2014
Kaili Liu
"""
import random 
def name_to_number(name):
    if name == "rock":
        name = 0
    elif name == "Spock":
        name = 1
    elif name == "paper":
        name = 2
    elif name == "lizard":
        name = 3
    elif name == "scissors":
        name = 4
    else:
        print 'Error- invalid name.'
    return name


def number_to_name(number):   
    if number == 0:
        number = 'rock'
    elif number == 1:
        number = 'Spock'
    elif number == 2:
        number = 'paper'
    elif number == 3:
        number = 'lizard'
    elif number == 4:
        number = 'scissors'
    else:
        print 'Error- invalid number.'
    return number
        

def rpsls(name): 
    print ''
    print "Player chooses", name
    player_number = name_to_number(name)
    comp_number = random.randrange(0,5)
    comp_choice = number_to_name(comp_number)
    print 'Computer chooses', comp_choice
    difference = (comp_number - player_number) % 5
    if difference == 1:
        print 'Computer wins!'
    elif difference == 2:
        print 'Computer wins!'
    elif difference == 3:
        print 'Player wins!'
    elif difference == 4:
        print 'Player wins!'
    else: 
        print 'Player and computer tie!'
    
    

    
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")


