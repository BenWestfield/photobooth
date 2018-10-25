import os
import time
import pygame 
from pygame.locals import QUIT,KEYDOWN,K_ESCAPE,K_RETURN
import config 

#########################
### Configuration #######
#########################


#initialise pygame
pygame.init()
pygame.display.set_mode((config.monitor_w,config.monitor_h))
screen = pygame.display.get_surface()
pygame.display.set_caption('Photo Booth Pics')
pygame.mouse.set_visible(False) #hide the mouse cursor
pygame.display.toggle_fullscreen


real_path = os.path.dirname(os.path.realpath(__file__)) + "/media/"
print(os.path.dirname(os.path.realpath(__file__))+"/media/")

def clear_screen():
    screen.fill ((0,0,0))
    pygame.display.flip() 



#update the displayed image
def update_display():
    print("update the display")
    clock = pygame.time.Clock()
    pygame.time.set_timer(pygame.USEREVENT,1000)
    font = pygame.font.SysFont('Consolas',50)
    counter = config.count_down
    
    while counter >= 1:
        for e in pygame.event.get():
            if e.type == pygame.USEREVENT:
                counter -= 1
            if e.type == pygame.QUIT: break
        else :
            text = str(counter) if counter > 0 else 'SMILE!'
            screen.fill((0,0,0)) 
            screen.blit(font.render(text,True, (207,181,59)),(config.monitor_w / 2,config.monitor_h /2))
            pygame.display.flip()
            time.sleep(1)
    print("exit the timer loop")
    pygame.time.set_timer(pygame.USEREVENT,0)
    clear_screen()

# clean up running programs when main programme exits
def cleanup ():
    print('Ended abruptly')
    pygame.quit()



#CR : urgh, tidy the return type of this function

#set variables to properly display the image on screen at right ratio
def set_dimensions(img_w, img_h):
    #This does not work when booting in terminal. If I get time,
    # lets look into why.

    #CR move these to a class that is passed around
    transform_x = config.monitor_w #how wide to scale the jpg when replaying
    transform_y = config.monitor_h #how high to scale the jpg when replaying
    offset_x = 0 #how far off to left corner to display photos
    offset_y = 0 # how far off to left corner to diplay photos

    #based on output screen resolution, calculate how to display
    ratio_h = (config.monitor_w * img_h) / img_w

    if (ratio_h < config.monitor_h):
        #Make widescreen with black bars
        transform_y = ratio
        transform_x =  config.monitor_w
        offset_y = (config.monitor_h - ratio_h ) / 2
        offset_x = 0
    elif (ratio_h > config.monitor_h):
        #Use vertical black bars
        transform_x = (config.monitor_h * img_w) / img_h
        transform_y = config.monitor_h
        offset_x = (config.monitor_w - transform_x) /2
        offset_y = 0
    else:
        #No need for black bars
        transform_x = config.monitor_w
        transform_y = config.monitor_h
        offset_y = offset_x = 0
    return transform_x,transform_y,offset_x,offset_y

#show one of the png media files
def show_image(image_path):
    #clear the screen
    screen.fill((0,0,0))

    #load the image
    img = pygame.image.load(image_path)
    img = img.convert()

    #set pixel dimensions based on the image
    transform_x,transform_y,offset_x,offset_y = set_dimensions(img.get_width(), img.get_height())

    # rescale the image to fit the current display
    img = pygame.transform.scale(img, (transform_x, transform_y))
    screen.blit(img,(offset_x,offset_y))
    pygame.display.flip()

#define the photo taking function for when input it pressed
def start_photobooth():
    input(pygame.event.get()) #press escape to exit pygame. Then press ctrl-c to exit python

    ################################## Begin Step 1 ##########################################
    print ("Get Ready")
    show_image(real_path + "instructions.png") 

    time.sleep(config.prep_delay)

    update_display()
    clear_screen


    print ("Taking picutres")

    show_image(real_path + "processing.png")
    time.sleep(config.prep_delay)
    print ("Done")

#Handle keyboard inputs
def input(events):
    for event in events: # Hit ESC to quit
        if (event.type == QUIT or
                (event.type == KEYDOWN and event.key == K_ESCAPE)):
            pygame.quit()
        elif event.type == KEYDOWN and event.key == K_RETURN:
            start_photobooth()

####################
### Main Program ###
####################

print ("Photo booth app running ... ")


while True:
    show_image(real_path + "intro.png")
    input(pygame.event.get()) # press escape to exit pygame. Then press ctrl-c to exit
    #time.sleep(config.debounce) #debounce

