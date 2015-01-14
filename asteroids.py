"""
    Implementation of the classic arcade game Asteroids   
    simplegui and other dependencies are contained within
    CodeSkulptor online service (www.codeskulptor.org)

    This code can be accessed and run online via
    http://www.codeskulptor.org/#user16_ohybXSjMVFe1nDl.py
"""

import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5
ACCEL = 0.5
ANG_VEL = 0.1
MISSLE_SPEED = 0.3
FRICTION = 0.05
KEY_MOVE = {}
KEY_ROT = {}
started = False
ship_crash = False
countdown = 60
ship_orientation = {}

def init():
    global KEY_ROT, KEY_MOVE
    KEY_ROT = {37: -ANG_VEL, 39: ANG_VEL}
    KEY_MOVE = {38: ACCEL, 40: -ACCEL}

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
#missile_info = ImageInfo([5,5], [10, 10], 3, 50) #class specified
missile_info = ImageInfo([5,5], [10, 10], 3, 44) #personal specification
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_blue2.png")
# ship explosion a different color 
ship_explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_orange.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.accel = 0
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
       
    def get_pos(self):
        return self.pos
    
    def get_vel(self):
        return self.vel
    
    def get_radius(self):
        return self.radius
    
    def get_angle(self):
        return self.angle
    
    def get_thrusters(self):
        self.image_center[0] += self.image_size[0]

    def remove_thrusters(self):
        self.image_center[0] -= self.image_size[0]
        
    def move(self,a):
        self.accel = a
        self.thrust = True
        self.get_thrusters()
    
    def stop(self):
        self.accel = 0
        self.thrust = False
        self.remove_thrusters()
        
    def set_angle(self,ang):
        self.angle = ang
    
    def set_angle_vel(self,v):
        self.angle_vel = v
    
    def remove_angle_vel(self):
        self.angle_vel = 0
    
    def draw(self,canvas):
        canvas.draw_image(self.image, self.image_center,self.image_size,self.pos,self.image_size,self.angle)
    
    def update(self):
        self.angle += self.angle_vel
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        for i in (0,1): 
            self.vel[i] *= (1-FRICTION)
        forward = angle_to_vector(self.angle)
        if self.thrust:
            for i in (0,1):
                self.vel[i] += forward[i]*self.accel
        
    def shoot(self):
        vec = angle_to_vector(self.angle)
        pos_x = self.pos[0] + vec[0] * self.radius
        pos_y = self.pos[1] + vec[1] * self.radius
        vel_x = 10 * vec[0] + self.vel[0]
        vel_y = 10 * vec[1] + self.vel[1]
        missile_group.add(Sprite([pos_x, pos_y], [vel_x, vel_y], self.angle, 0, missile_image, missile_info, missile_sound))
        
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        #self.scale_size = self.image_size
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
    #uncommenting this will lead to a bug in the rock.
    #@TODO: Implement properly
#    def scale(self,factor):
#        for i in (0,1):
#            self.scale_size[i] *= factor
    
    def draw(self, canvas):
        if self.animated:
            idx = self.age % self.lifespan
            width = self.image_size[0]
            center = [self.image_center[0]+idx*width,self.image_center[1]]
            canvas.draw_image(self.image, center ,self.image_size,self.pos,self.image_size,self.angle)
        else: 
            canvas.draw_image(self.image, self.image_center,self.image_size,self.pos,self.image_size,self.angle)
    
    def update(self):
        self.angle += self.angle_vel
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT 
        self.age += 1
        if self.age <= self.lifespan:
            return False
        else:
            return True

    def get_pos(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def collide(self,other):
        return (dist(self.pos,other.get_pos()) < (self.radius + other.get_radius()))
            
           
def draw(canvas):
    global time,lives, score, countdown
    
    #reset test/if true, reset
    reset()
    
    #if ship crashes, begin countdown, then reset ship location
    if ship_crash:
        countdown -= 1
        if countdown < 0:
            reset_ship()
    
    # animiate background
    time += 1
    center = debris_info.get_center()
    size = debris_info.get_size()
    wtime = (time / 8) % center[0]
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, [center[0] - wtime, center[1]], [size[0] - 2 * wtime, size[1]], 
                                [WIDTH / 2 + 1.25 * wtime, HEIGHT / 2], [WIDTH - 2.5 * wtime, HEIGHT])
    canvas.draw_image(debris_image, [size[0] - wtime, center[1]], [2 * wtime, size[1]], 
                                [1.25 * wtime, HEIGHT / 2], [2.5 * wtime, HEIGHT])

    # draw ship
    if not ship_crash:
        my_ship.draw(canvas)
    
    # draw rocks, collision checking   
    process_sprite_group(canvas,rock_group)
    if group_collide(rock_group, my_ship, True):
        lives -= 1
    
    #draw missiles, collision checking
    process_sprite_group(canvas,missile_group)
    score += group_group_collide(rock_group, missile_group)
    
    #draw explosions, collision checking
    process_sprite_group(canvas,explosion_group)
    process_sprite_group(canvas,ship_explosion_set)
    
    #draw text
    canvas.draw_text("Lives Remaining: " + str(lives), [5,20], 24, "White")
    canvas.draw_text("Score: " + str(score), [WIDTH-100,20], 24, "White")
    
    # update ship position
    if not ship_crash:
        my_ship.update()
    
    #splash screen introduction
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], splash_info.get_size())
        txt_loc_x = splash_info.get_center()[0] + 65
        txt_loc_y = splash_info.get_center()[1] + 230
        canvas.draw_text("Use Arrow Keys & Spacebar to Play", 
                         [txt_loc_x, txt_loc_y], 18, "White")
    

def click(pos):
    global started
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True    
    
def down_key(k):
    global a_missle
    if k in KEY_ROT:
        my_ship.set_angle_vel(KEY_ROT[k])
    if k in KEY_MOVE:
        my_ship.move(KEY_MOVE[k])
        ship_thrust_sound.play()
    if k == simplegui.KEY_MAP["space"]:
        a_missle = my_ship.shoot()

def up_key(k):
    if k in KEY_ROT:
        my_ship.remove_angle_vel()
    if k in KEY_MOVE:
        my_ship.stop()
        ship_thrust_sound.rewind()

#random float generator in a given range   
def rand_float(low, high):
    range_width = high - low
    return (random.random() * range_width + low)

#generate explosion sprite
def create_explosion(other, ship = False):
    pos = other.get_pos()
    image = ship_explosion_image if ship else explosion_image
    info = explosion_info
    sound = explosion_sound
    return Sprite(pos, [0,0], 0, 0,image,info,sound)

#store the orientation of the ship for regeneration
def get_orientation(ship):
    global ship_orientation
    ship_orientation['ang'] = ship.get_angle()
    ship_orientation['pos'] = ship.get_pos()

#check for collision in set of rocks
def group_collide(group_set, other_object, ship = False):
    global ship_crash
    for sprite in list(group_set):
        if sprite.collide(other_object):
            if ship:
                explosion_group.add(create_explosion(my_ship,True))
                explosion_group.add(create_explosion(sprite))
                get_orientation(my_ship)
                ship_crash = True
            else:
                explosion_group.add(create_explosion(sprite))
            group_set.remove(sprite)
            return True
    return False

#check for collision between set of missiles and set of rocks
def group_group_collide(set_rocks, set_missiles):
    score = 0
    for missile in list(set_missiles):
        result = group_collide(set_rocks,missile)
        if result:
            score += 1
            set_missiles.remove(missile)
        else:
            pass
    return score

#draw and update all rocks in set
def process_sprite_group(canvas, group_sprite):
    for sprite in set(group_sprite):
        result = sprite.update()
        if result:
            group_sprite.remove(sprite)
        sprite.draw(canvas)

# timer handler that spawns a rock 
def rock_spawner():
    global rock_group
    if len(rock_group) < 12 and started:
        ship_pos = my_ship.get_pos()
        scale = rand_float(0.3,1.15)
        ang = rand_float(-6.28, 6.29)
        vel = [0,0]
        pos = [0,0]
        multiplier = score//6 if score > 50 else score//3
        ang_vel = rand_float(-0.1,0.1)
        for i in (0,1):
            vel[i] = rand_float(-0.5,0.6)*multiplier
            x = WIDTH if i==0 else HEIGHT
            pos[i] = random.randrange(0,x)
            while ( dist(pos,ship_pos) < 2*my_ship.get_radius()):
                pos[i] = random.randrange(0,x)
        rock_group.add(Sprite(pos, vel, ang, ang_vel, asteroid_image, asteroid_info))
        #a_rock.scale(scale)
    else:
        pass
    
def reset_ship():
    global my_ship, ship_crash, countdown
    my_ship = Ship(ship_orientation['pos'], [0, 0], 0, ship_image, ship_info)
    my_ship.set_angle(ship_orientation['ang'])
    ship_crash = False
    countdown = 60
    
# reset function
def reset():
    global lives, score, started, rock_group
    if lives < 1:
        started = False
        lives = 3
        score = 0
        rock_group = set()
        explosion_group = set()
        ship_orientation['pos'] = [WIDTH/2, HEIGHT/2]
        ship_orientation['ang'] = 0

# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship, empty set of rocks, missiles, explosions NOTE: More Globals
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set()
missile_group = set()
explosion_group = set()
ship_explosion_set = set()

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(down_key)
frame.set_keyup_handler(up_key)
frame.set_mouseclick_handler(click)
timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
init()
