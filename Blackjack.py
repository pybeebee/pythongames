"""
Kaili Liu
May 10, 2014
"""
# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcomept1 = ""
outcomept2 = ""
outcomept3 = ""
outcomept4 = ""
score = 0
deck = []
pos =  [20, 160]

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


    
# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
  
        
        
# define hand class        
class Hand:
    # create Hand object
    def __init__(self):
        self.hand = []	

    # return a string representation of a hand
    def __str__(self):
        S = ""
        for i in self.hand:
            S += " "
            S += str(i)  
        return S	

    # add a card object to a hand        
    def add_card(self, card):
        self.hand.append(card)	
        card = str(card)

    # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
    # compute the value of the hand, see Blackjack video
    def get_value(self):  
        hand_value = 0  
        yes_ace = False
        for i in self.hand:
            hand_value += VALUES[i.get_rank()] 
            if i.get_rank() == 'A':
                yes_ace = True

        if yes_ace == False:
            return hand_value        
        else:
            if hand_value + 10 <= 21:
                return hand_value + 10
            else: 
                return hand_value

    # draw a hand on the canvas, use the draw method for cards    
    def draw(self, canvas, pos):
        for i in self.hand:
            i.draw(canvas, [40 + CARD_SIZE[0]*self.hand.index(i), pos[1]])
 
 
 
    
    
# define deck class 
class Deck:
    # create a Deck object
    def __init__(self):
        self.deck = []
        for r in RANKS:
            for s in SUITS:
                self.deck.append(Card(s, r))

    # shuffle the deck         
    def shuffle(self):
        random.shuffle(self.deck)
        
    # deal a card object from the deck
    def deal_card(self):
        if len(self.deck) > 0:
            return self.deck.pop(0)        

    # return a string representing the deck 
    def __str__(self):
        D = ""
        for i in self.deck:
            D += " "
            D += str(i)  
        return D	

#define event handlers for buttons
def deal():
    global score, in_play, deck, player_hand, dealer_hand, outcomept1, outcomept2, outcomept3
    # your code goes here     
    
    outcomept1 = "Hit or stand?"
    if in_play:
        outcomept1 = "Player Lost."
        score -= 1
    
    deck = Deck()
    deck.shuffle()
    player_hand = Hand()
    dealer_hand = Hand()  
    
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())

    outcomept2 = ""
    outcomept3  = ""
    in_play = True
  
        
    

# replace with your code below
# if the hand is in play, hit the player
# if busted, assign a message to outcome, update in_play and score
def hit():
    global score, player_hand, dealer_hand, outcomept1, outcomept2, outcomept3, in_play    
    if in_play: 
        outcomept1 = "Hit or stand?"
        player_hand.add_card(deck.deal_card())
    if player_hand.get_value() > 21:
        in_play = False
        score -= 1
        outcomept1 = "Player busted."
        outcomept2 = "Dealer wins! :("
        outcomept3 = "New deal?"
        
            
# replace with your code below
# if hand is in play, repeatedly hit dealer until his hand has value 17 or more
# assign a message to outcome, update in_play and score       
def stand():
    global score, player_hand, dealer_hand, outcomept1, outcomept2, outcomept3, in_play    
    while dealer_hand.get_value() < 17:
        if in_play:
            outcomept1 = "Hit or stand?"
            dealer_hand.add_card(deck.deal_card())

    outcomept1 = ""
        
    if dealer_hand.get_value() > 21:
        in_play = False
        score += 1
        outcomept1 = "Dealer busted."
        outcomept2 = "Player wins! :)"
        outcomept3 = "New deal?"
    elif player_hand.get_value() <= dealer_hand.get_value():
        in_play = False
        score -= 1
        outcomept1 = "Dealer wins! :("
        outcomept2 = "New deal?"
        outcomept3 = ""
    else:
        in_play = False
        score += 1
        outcomept1 = "Player wins! :)"
        outcomept2 = "New deal?"
        outcomept3 = ""
                        
        

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below  
    player_hand.draw(canvas, [40, 430])
    dealer_hand.draw(canvas, [40, 230])
    canvas.draw_text("Player:", (5, 400), 40, 'Black', 'sans-serif')
    canvas.draw_text("Dealer:", (5, 200), 40, 'Black', 'sans-serif')
    if in_play:
        canvas.draw_image(card_back, (35.5, 48), CARD_BACK_SIZE, (75.5, 278), CARD_BACK_SIZE)
    canvas.draw_text("Blackjack", (350, 90), 70, 'Olive', 'sans-serif')
    canvas.draw_text(outcomept1, (425, 200), 40, 'Aqua', 'sans-serif')
    canvas.draw_text(outcomept2, (425, 275), 40, 'Yellow', 'sans-serif')
    canvas.draw_text(outcomept3, (425, 350), 40, 'Lime', 'sans-serif')
    canvas.draw_text(outcomept4, (425,425), 40, 'Lime', 'sans-serif')
    canvas.draw_text("Score:" + str(score), (5, 100), 45, 'Fuchsia', 'monospace')

# initialization frame
frame = simplegui.create_frame("Blackjack", 700, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric