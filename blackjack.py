"""
    Implementation of the card game Blackjack    
    simplegui and other dependencies are contained within
    CodeSkulptor online service (www.codeskulptor.org)

    This code can be accessed and run online via
    http://www.codeskulptor.org/#user15_88huJiZ8wiJqZxM.py
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
    def __init__(self):
        # create Hand object
        self.cards = []
        self.has_ace = False
        
    def __str__(self):
        # return a string representation of a hand
        output = ""
        for i in self.cards:
            output += "("+ i.get_suit() + "," + i.get_rank() + ") "
        return output

    def get_cards(self):
        return self.cards
    
    def add_card(self, card):
        # add a card object to a hand
        if card.get_rank() == 'A':
            self.has_ace = True
        self.cards.append(card)
        

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        val = 0
        for card in self.cards:
            val += VALUES[card.get_rank()]
        
        if not self.has_ace:
            return val
        else:
            if val + 10 <= 21:
                val = val + 10
                return val
            else:
                return val
        
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        index = 0
        for card in self.cards:           
            pos[0] = pos[0] + CARD_SIZE[0]
            card.draw(canvas,pos)
            index += 1
 
        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.burn = []
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(suit,rank))

    def shuffle(self):
        #TODO: correct this function so that it resets the deck properly
        # add cards back to deck and shuffle
        # use random.shuffle() to shuffle the deck
        if len(self.burn) > 0:
            self.deck = self.deck + self.burn
            self.burn = []
        random.shuffle(self.deck)
        #print str(self.deck)

    def deal_card(self):
        # deal a card object from the deck
        self.burn.append(self.deck.pop())
        #print self.burn[-1]
        return self.burn[-1]
    
    def __str__(self):
        # return a string representing the deck
        output = ""
        for card in self.deck:
            output += str(card) + " "
        return output
    
    def draw(self, canvas, pos):
        # draws a deck of cards on the screen
        for i in range(len(self.deck)):
            canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, 
                              [pos[0] + CARD_BACK_CENTER[0]+2.5*i, pos[1] + CARD_BACK_CENTER[1]], 
                              CARD_SIZE)

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
player = Hand()
dealer = Hand()
casino = Deck()
    
#define event handlers for buttons
def deal():
    global outcome, score, in_play, player, dealer, casino
    
    if in_play:
        player_lost("newDeal")
    
    else:
        in_play = True
        outcome = "Hit or Stand?"
        
        player = Hand()
        dealer = Hand()
        casino = Deck()
        
        casino.shuffle()
        
        dealer.add_card(casino.deal_card())
        player.add_card(casino.deal_card())
        dealer.add_card(casino.deal_card())
        player.add_card(casino.deal_card())
        #print "Player " + str(player) + " Value: " + str(player.get_value())
        #print "Dealer " + str(dealer) + " Value: " + str(dealer.get_value())

    
def player_lost(word):
    # TODO: Correct this function, so that outcome shows "you lost" rather than "busted".
    global in_play, outcome, score
    in_play = False
    score -= 1
    if word == "lost":
        outcome = "You lost. New Deal?"
    elif word == "newDeal":
        outcome = "You lost. New Deal. Hit or Stand?"
    else:
        outcome = "You Have Busted. New Deal?"
    #print outcome, score    
    
def hit():
    # if the hand is in play, hit the player
    # if busted, assign a message to outcome, update in_play and score
    
    if in_play:
        if player.get_value() <= 21:
            player.add_card(casino.deal_card())
            if player.get_value() >= 21: 
                player_lost("busted")        
        else:
            player_lost("lost")
            
        #print "Player Hit: " + str(player) + " Value: " + str(player.get_value())
    else:
        pass

       
def player_win():
    global score, in_play, outcome
    score += 1
    in_play = False
    outcome = "You Win! New Deal?"
        
def stand():
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    # assign a message to outcome, update in_play and score
    global outcome
    if in_play:
        while(dealer.get_value() <= 17):
            dealer.add_card(casino.deal_card())
            #print "Dealer Hit: " + str(dealer) + " Value: " + str(dealer.get_value())
        if (dealer.get_value() >= player.get_value()):
            if dealer.get_value() <= 21:
                player_lost("lost")
            else: 
                player_win()
        else:
            player_win()
            
    else:
        outcome = "You Have Busted. New Deal?"
    #print outcome, score

def draw_hole(canvas, pos):
    index = 0
    #nudging pos to match the other card positions
    pos[0] = pos[0] + CARD_SIZE[0] + CARD_CENTER[0]
    pos[1] = pos[1] + CARD_CENTER[1] 
   
    for card in dealer.get_cards():
        if index == 0:
            #draw hole
            canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [pos[0], pos[1]],CARD_SIZE)
        else:
            #draw rest of the cards
            card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(card.rank), CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(card.suit))
            #nudging pos back to position
            pos[0] = pos[0] + CARD_CENTER[0]
            pos[1] = pos[1] - CARD_CENTER[1]
            canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        index +=1        
        
# draw handler    
def draw(canvas):
    global outcome
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_text("Black Jack!", [10, 50], 52, "White")
    canvas.draw_text("Status:", [10, 140], 30, "Black")
    canvas.draw_text("Player:", [10, 190], 40, "Black")
    canvas.draw_text("Dealer:", [10, 400], 40, "Black")
    canvas.draw_text(("Score: " + str(score)), [10, 70], 24, "White") 
        
    canvas.draw_text(outcome, [150, 140], 30, "Black")
    
    casino.draw(canvas, [300, 10])
    player.draw(canvas, [10, 210])
    
    if in_play:
        draw_hole(canvas, [10, 460])
    else:
        dealer.draw(canvas, [10, 460])

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
frame.start()
