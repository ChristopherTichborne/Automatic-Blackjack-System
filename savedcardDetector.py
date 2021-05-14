############## Python-OpenCV Playing Card Detector ###############
#
# Description: Python script to detect and identify playing cards
# from a PiCamera video feed.
#

# Import necessary packages
import cv2
import numpy as np
import time
import os
import Cards
import VideoStream
import Basic_Strategy


### ---- INITIALIZATION ---- ###
# Define constants and initialize variables

## Camera settings
IM_WIDTH = 1920
IM_HEIGHT = 1080 
FRAME_RATE = 20

## Initialize calculated frame rate because it's calculated AFTER the first time it's displayed
frame_rate_calc = 1
freq = cv2.getTickFrequency()

## Define font to use
font = cv2.FONT_HERSHEY_SIMPLEX

# Initialize camera object and video feed from the camera. The video stream is set up
# as a seperate thread that constantly grabs frames from the camera feed. 
# See VideoStream.py for VideoStream class definition
## IF USING USB CAMERA INSTEAD OF PICAMERA,
## CHANGE THE THIRD ARGUMENT FROM 1 TO 2 IN THE FOLLOWING LINE:
videostream = VideoStream.VideoStream((IM_WIDTH,IM_HEIGHT),FRAME_RATE,2,1).start()
time.sleep(2) # Give the camera time to warm up
#image = cv2.imread('3Cardsv3.jpg',-1)
#]image = cv2.resize(image,(1280, 720))
num_cards_wrong = []
frames=0
# Load the train rank and suit images
path = os.path.dirname(os.path.abspath(__file__))
train_ranks = Cards.load_ranks( path + '/Card_Imgs/')
train_suits = Cards.load_suits( path + '/Card_Imgs/')
strat_table = Basic_Strategy.strat_table_setup()


### ---- MAIN LOOP ---- ###
# The main loop repeatedly grabs frames from the video stream
# and processes them to find and identify playing cards.

cam_quit = 0 # Loop control variable
dealers_card = [0]


# Begin capturing frames
while cam_quit == 0:

    # Grab frame from video stream
    image = videostream.read()
    
    # Start timer (for calculating frame rate)
    t1 = cv2.getTickCount()

    
    # Pre-process camera image (gray, blur, and threshold it)
    pre_proc = Cards.preprocess_image(image)
    # Find and sort the contours of all cards in the image (query cards)
    cnts_sort, cnt_is_card = Cards.find_cards(pre_proc)
    my_card = []
    
    # If there are no contours, do nothing
    if len(cnts_sort) != 0:
    
        # Initialize a new "cards" list to assign the card objects.
        # k indexes the newly made array of cards.
        cards = []
        k = 0
    
        # For each contour detected:
        for i in range(len(cnts_sort)):
            if (cnt_is_card[i] == 1):
    
                # Create a card object from the contour and append it to the list of cards.
                # preprocess_card function takes the card contour and contour and
                # determines the cards properties (corner points, etc). It generates a
                # flattened 200x300 image of the card, and isolates the card's
                # suit and rank from the image.
                cards.append(Cards.preprocess_card(cnts_sort[i],image))
    
                # Find the best rank and suit match for the card.
                cards[k].best_rank_match,cards[k].best_suit_match,cards[k].rank_diff,cards[k].suit_diff,cards[k].is_Ace = Cards.match_card(cards[k],train_ranks,train_suits)
                if(cards[k].best_rank_match != '-'):
                    #print(str(cards[k].best_rank_match) + " " + str(cards[k].center[1]) + " " + str(int(720/2)))
                    if(cards[k].center[1] > 360):
                        my_card.append(cards[k])
                    else:
                        dealers_card[0] = cards[k]
                # Draw center point and match result on the image.
                image = Cards.draw_results(image, cards[k])
                k = k + 1
    
        # Draw card contours on image (have to do contours all at once or
        # they do not show up properly for some reason)
        if (len(cards) != 0):
            temp_cnts = []
            for i in range(len(cards)):
                temp_cnts.append(cards[i].contour)
            cv2.drawContours(image,temp_cnts, -1, (255,0,0), 2)
        temp = 0
        for i in cards:
            if(i.best_rank_match == "-"):
                temp+=1
        num_cards_wrong.append(temp)        
    

        
    # Draw framerate in the corner of the image. Framerate is calculated at the end of the main loop,
    # so the first time this runs, framerate will be shown as 0.
    cv2.putText(image,"FPS: "+str(int(frame_rate_calc)),(10,26),font,0.7,(255,0,255),2,cv2.LINE_AA)
    
    if (len(my_card) > 1 and dealers_card[0] != 0):
        my_hand = Basic_Strategy.find_my_hand(my_card)
        dealers_hand = Basic_Strategy.find_my_hand(dealers_card)
        action = Basic_Strategy.find_action(dealers_hand, my_hand, strat_table)
        cv2.putText(image,"YOUR HAND TOTAL="+str(my_hand),(40,int(IM_HEIGHT-200)),font,0.7,(255,0,255),2,cv2.LINE_AA)
        cv2.putText(image,"DEALERS HAND = " + str(dealers_hand),(40,100),font,0.7,(255,0,255),2,cv2.LINE_AA)
        cv2.putText(image,"ACTION="+str(action),(int(IM_WIDTH/2),int(IM_HEIGHT/2)),font,0.7,(255,0,255),2,cv2.LINE_AA)
    
    
     
    # Finally, display the image with the identified cards!
    cv2.imshow("Card Detector", image)
    
    t2 = cv2.getTickCount()
    time1 = (t2-t1)/freq
    frame_rate_calc = 1/time1
    
    

    # Poll the keyboard. If 'q' is pressed, exit the main loop.
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        cam_quit = 1    
    #cv2.waitKey(0)
    

        

# Close all windows and close the PiCamera video stream.
cv2.destroyAllWindows()
sum_temp = 0
for i in num_cards_wrong:
    sum_temp += i
print("average unidentified " + str(7/(sum_temp * len(num_cards_wrong))))
videostream.stop()
