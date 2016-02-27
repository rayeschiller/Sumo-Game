from visual import *
import math 
import time
import random
import threading 
import csaudio
from csaudio import *
import wave

wave.big_endian = 0 
# Sumo wrestling balls
# Rina Schiller, John Wetmore, Sarah Arbeli

scene.width=500
scene.height=500
scene.title='Sumo'

def make_alien():
    """ makes an alien! -- in the process, this shows how to
        group many objects into a single coordinate system ("frame")
        and treat that as a single object
        Docs here:  http://vpython.org/contents/docs/frame.html
    """
    alien = frame( pos=(4,1.2,0), radius = .7 )  # makes a new "frame" == a container
    # with a local coordinate system that can have any number of parts...
    # here are the "parts":
    sphere( frame=alien, radius=1, color=color.green )
    sphere( frame=alien, radius=0.3, pos=(.7,.5,.2), color=color.white )
    sphere( frame=alien, radius=0.3, pos=(.2,.5,.7), color=color.white )
    sphere( frame=alien, radius=0.3, pos=(.5,.5,.5), color=color.white )
    cylinder( frame=alien, pos=(0,.9,-.2), axis=(.02,.2,-.02),  # the hat!
              radius=.7, color=color.magenta)
    return alien   # always use the _frame_, not any of its parts...

def make_ball():
    ball = frame( pos=(-4,1.2,0), radius = .7)  # makes a new "frame" == a container
    # with a local coordinate system that can have any number of parts...
    # here are the "parts":
    sphere( frame=ball, radius=1, color=color.cyan)
    sphere( frame=ball, radius=0.3, pos=(.7,.5,.2), color=color.white )
    sphere( frame=ball, radius=0.3, pos=(.2,.5,.7), color=color.white )
    sphere( frame=ball, radius=0.3, pos=(.5,.5,.5), color=color.white )
    cylinder( frame=ball, pos=(0,.9,-.2), axis=(.02,.2,-.02),  # the hat!
              radius=.7, color=color.orange)
    return ball   # always use the _frame_, not any of its parts...

def rand_color(min=0, max=1):
    """ Generate a random 3 item tuple between a
        minimum and maximum level.
        Good for randome colors values.
    """
    r = (max-min) * random.random() + min
    b = (max-min) * random.random() + min
    g = (max-min) * random.random() + min
    return [r,g,b]

def play_smoothly( filename ): 
    """ a test function that plays filename
        You'll need the filename in this folder!

        To play smoothly, it creates a separate thread
        and runs the sound in that other thread...
    """
    t = threading.Thread( target=play, args=(filename,) )
    t.start()

def main():
    print 'Welcome to Sumo Ball Wrestling!'
    
    
    print 'Player 1: Use arrow keys to move'
    print 'Player 2: Use ASDW keys to move'
    print 'To restart the game, press Shift + R'

    print 'Click 1 to have a circle arena'
    print 'Click 2 to have a square arena'
    print 'Click 3 to have a triangle arena'
    
    choice = input("choose wisely: ")
    if choice == 1:
        floor = cylinder(length=.3, height=.1, width=6, radius=20, color=(.3,.4,.5), axis=(0,1,0))
    elif choice == 2:
        floor = box(length=30, height=.3, width = 30, radius=15, color=(.3,.4,.5), axis=(0,0,1))
    elif choice == 3:
        floor = pyramid(length=25, height=.4, width=25, radius=15, color=(.3,.4,.5), axis=(0,0,1))
    else:
        floor = cylinder(length=.3, height=.3, width=6, radius=20, color=(.3,.4,.5), axis=(0,1,0))
    
    #user messages
    L = label(pos=(0,12,0), box = False, text='Game Over')
    G = label(pos=(0,10,0), box = False, text='Green Alien Wins!')
    B = label(pos=(0,10,0), box = False, text='Blue Alien Wins!') 
    L.visible = False
    G.visible = False
    B.visible = False
    
    #create ball and alien
    ball = make_ball()
    alien = make_alien()
   
    while mag(ball.pos) < floor.radius and mag(alien.pos) < floor.radius:    
                
        ball.vel = vector(0,0,0)   # this is the "game piece" w/ zero starting vel.
        alien.vel = vector(0,0,0)  # no velocity (yet!)

        R = ball.radius + alien.radius 
        game_over = False

        # We set some variables to control the display and the event loop
        RATE = 30             # number of loops per second to run, if possible!
        dt = 1.0/(1.0*RATE)   # the amount of time per loop (again, if possible)
        autocenter = True     # do you want vPython to keep the scene centered?
        rate(RATE)
        scene.range = 25
        scene.forward = vector( 0,-1,-3 )

        while True:
            # +++++ start of all position updates: once per loop +++++ 
            ball.pos = ball.pos + ball.vel*dt           # PHYSICS!
            alien.pos = alien.pos + alien.vel*dt
            # +++++ end of all once-per-loop position updates +++++

            # ===== handling user events: keypresses and mouse =====
            rate(RATE)
            # here, we see if the user has pressed any keys
            if scene.kb.keys:   # any keypress to be handled?
                s = scene.kb.getkey()
                # print "You pressed the key", s  

                # Key presses to give the alien velocity (in the x-z plane)
                dx = 3.5; dz = 3.5   # easily-changeable values
                if s == 'left': alien.vel += vector(-dx,0,0)
                if s == 'right': alien.vel += vector(dx,0,0)
                if s == 'up': alien.vel += vector(0,0,-dz)
                if s == 'down': alien.vel += vector(0,0,dz)

                # Key presses to give the ball velocity (in the x-z plane)
                dx = 3.5; dz = 3.5   # easily-changeable values
                if s == 'a': ball.vel += vector(-dx,0,0)
                if s == 'd': ball.vel += vector(dx,0,0)
                if s == 'w': ball.vel += vector(0,0,-dz)
                if s == 's': ball.vel += vector(0,0,dz)

                # space to stop everything
                if s == ' ':  # space to stop things
                    ball.vel = vector(0,0,0)
                    alien.vel = vector(0,0,0)

                # capital R to reset things
                if s == 'R':
                    L.visible = False
                    B.visible = False
                    G.visible = False
                    ball.vel = vector(0,0,0)
                    ball.pos = vector(-4,1.2,0)
                    alien.vel = vector(0,0,0)
                    alien.pos = vector(4,1.2,0)
                    floor.radius = 20
                    floor.color = (.3,.4,.5)
                    game_over = False

                if s in 'Qq':  # Quit!
                    print "Quitting..."
                    break  # breaks out of the main loop

            #detect collision
            if mag(alien.pos-ball.pos) <= R:

                #if collision, ball moves depending on which ball hits first
                if mag(ball.vel)>mag(alien.vel): 
                    alien.vel = vector(ball.vel.x,0,ball.vel.z)
                    ball.vel = .5 * -ball.vel
                    play_smoothly( 'boom.wav' )
                else:
                    ball.vel = vector(alien.vel.x,0,alien.vel.z)
                    alien.vel = .5 * -alien.vel
                    play_smoothly( 'boom.wav' )
                #floor gets smaller
                floor.radius -= 1
                #floor changes to random color with new collision
                clr = rand_color()
                floor.color = clr
                
            #if ball leaves the radius of the arena, print winner message
            if mag(ball.pos) > floor.radius:
                L.visible = True
                G.visible = True 
                ball.vel = vector(ball.vel.x,-15,0)
                alien.vel = vector(0,0,0)
                if game_over == False:
                    play_smoothly( 'endboom.wav' )
                    play_smoothly( 'yay.mp3' )
                game_over = True
                
                
            elif mag(alien.pos) > floor.radius:
                L.visible = True
                B.visible = True
                
                ball.vel = vector(0,0,0)
                alien.vel = vector(alien.vel.x,-15,0)
                
                if game_over == False:
                    play_smoothly( 'endboom.wav' )
                    play_smoothly( 'yay.mp3' )
                game_over = True




                

# This should be the FINAL thing in the file...
if __name__ == "__main__":   # did we just RUN this file?
    main()                   # if so, we call main()

