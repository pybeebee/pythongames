"""
April 19, 2014
Kaili Liu
"""
# template for "Stopwatch: The Game"
import simplegui
import time


# define global variables
tenths_seconds = 0
ones_seconds = 0
tens_seconds = 0
minutes = 0
successes = 0L
attempts = 0L
display = 0
elapsed_time = 0


# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):    
    tenths = t%10
    seconds = t/10L % 60
    minutes = t/600L
    return '%(min)01d:%(sec)02d.%(ten)1d' % { "min":minutes, "sec":seconds, "ten":tenths}
    
    
# define event handlers for buttons; "Start", "Stop", "Reset"


def start_button_handler():
    global elapsed_time
    timer.start()
    
    

def stop_button_handler():
    global elapsed_time, successes, attempts

    timer.stop()
    attempts += 1
    if elapsed_time % 10 == 0:
        successes += 1


def reset_button_handler():
    global elapsed_time, attempts, successes, minutes, tens_seconds, ones_seconds, tenths_seconds
    timer.stop()
    attempts = 0
    successes = 0
    elapsed_time = 0
    
    
    
# define event handler for timer with 0.1 sec interval
def timer_handler():
    global elapsed_time
    elapsed_time = int(elapsed_time)
    elapsed_time += 1
  


# define draw handler
def draw_handler(canvas):
    global start_time, elapsed_time, display, successes, attempts

    display = str(successes) + "/" + str(attempts)
    canvas.draw_text(format(elapsed_time), (75, 60), 24, "White")
#    canvas.draw_text(elapsed_time, (75, 80), 20, "White")
    canvas.draw_text(display, (170, 30), 20, "Silver")
    
# create frame
frame = simplegui.create_frame("Stopwatch", 200, 150)
frame.set_draw_handler(draw_handler)

# register event handlers
timer = simplegui.create_timer(100, timer_handler)   
start_button = frame.add_button("Start", start_button_handler)
stop_button = frame.add_button("Stop", stop_button_handler)
reset_button = frame.add_button("Reset", reset_button_handler)

# start frame
frame.start()



