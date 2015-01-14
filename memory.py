"""
    Implementation of classic arcade game Memory    
    simplegui and other dependencies are contained within
    CodeSkulptor online service (www.codeskulptor.org)

    This code can be accessed and run online via
    http://www.codeskulptor.org/#user14_BEsvCFDuxcBGMP1.py
"""

import simplegui
import random

#globals
cards = [] # the global numbers to be shown
state = range(17) # the boolean list of whether card is faceup/facedown
exposed = [] # the list of cards exposed
state_machine = 0 # the logic counter of game
moves = 0 # the score
CARD_WIDTH = 50 #50px
CARD_HEIGHT = 100 #100px
HEIGHT = 100
WIDTH = 800
TOPCARD = HEIGHT-CARD_HEIGHT-1
FONT_SIZE = 52

# helper function to initialize globals
def init():
    global cards, moves, state_machine, tmp1, tmp2
    cards = get_nums()
    (moves, tmp1, tmp2, state_machine) = (0,0,0,0)
    label.set_text("Moves = 0")
    for i in range(17):
        state[i]=False

#define helper functions
def get_nums():
    nums = range(9) + range(9)
    random.shuffle(nums)
    return nums
    
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global moves, state_machine
    global tmp1, tmp2
    idx = get_index(pos[0])
    
    if not state[idx]:
        set_moves()
        
        if state_machine == 0:
            state[idx] = True
            state_machine = 1
            tmp1 = idx
            
                
        elif state_machine == 1:
            state[idx] = True
            state_machine = 2
            tmp2 = idx
            
                        
        else:
            state[idx] = True
            state_machine = 1
            if cards[tmp1] != cards[tmp2]:
                state[tmp1] = False
                state[tmp2] = False
                tmp1 = idx
                tmp2 = 0
            else:
                state[tmp1] = True
                state[tmp2] = True
                tmp1 = idx
                tmp2 = 0
            
 

    
#get the index of where the mouse clicked
def get_index(x):
    for i in range(17):
        start = CARD_WIDTH*i
        end = start + CARD_WIDTH
        if x > start and x < end:
            return i

def set_moves():
    global moves, state_machine, exposed
    moves += 1
    label.set_text("Moves = " + str(moves))
        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    #draw the cards
      
    for i in range(17):
        if not state[i]:
            topright = (CARD_WIDTH*i,TOPCARD)
            topleft = (CARD_WIDTH*i+CARD_WIDTH,TOPCARD)
            bottomleft = (CARD_WIDTH*i+CARD_WIDTH,HEIGHT)
            bottomright = (CARD_WIDTH*i,HEIGHT)
            canvas.draw_polygon([topright,topleft,bottomleft,bottomright],
                                1, "Black", "Green")
    #draw the numbers
    for i in range(17):
        if state[i]:
            x = CARD_WIDTH*i+12
            y = CARD_HEIGHT/2 + 14
            canvas.draw_text(str(cards[i]),(x,y),FONT_SIZE,"Black")


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", WIDTH, HEIGHT)
frame.set_canvas_background("White")
frame.add_button("Restart", init)
label = frame.add_label("Moves = 0")

# initialize global variables
init()

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
frame.start()
# Always remember to review the grading rubric