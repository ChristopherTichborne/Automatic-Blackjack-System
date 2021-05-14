
# Description: Functions for setting up a basic blackjack strategy table 


import numpy as np
import cv2

#functions
royalty = ["King" , "Queen", "Jack"]
def strat_table_setup():
    strat_table = []
    #duplicate_table = []
    #ace_table = []
    
    append_letter(strat_table, 10, "Stand")
    append_letter(strat_table, 5, "Stand")
    append_letter(strat_table, 5, "Hit")
    append_letter(strat_table, 5, "Stand")
    append_letter(strat_table, 5, "Hit")
    append_letter(strat_table, 5, "Stand")
    append_letter(strat_table, 5, "Hit")
    append_letter(strat_table, 5, "Stand")
    append_letter(strat_table, 5, "Hit")
    append_letter(strat_table, 2, "Hit")
    append_letter(strat_table, 3, "Stand")
    append_letter(strat_table, 5, "Hit")
    append_letter(strat_table, 9, "Double Down")
    append_letter(strat_table, 1, "Hit")
    append_letter(strat_table, 8, "Double Down")
    append_letter(strat_table, 3, "Hit")
    append_letter(strat_table, 4, "Double Down")
    append_letter(strat_table, 15, "Hit")
    return strat_table
def ace_table_setup():
    ace_table = []
    
    append_letter(ace_table, 11, "Stand")
    append_letter(ace_table, 4, "Double Down")
    append_letter(ace_table, 2, "Stand")
    append_letter(ace_table, 4, "Hit")
    append_letter(ace_table, 4, "Double Down")
    append_letter(ace_table, 7, "Hit")
    append_letter(ace_table, 3, "Double Down")
    append_letter(ace_table, 7, "Hit")
    append_letter(ace_table, 3, "Double Down")
    append_letter(ace_table, 8, "Hit")
    append_letter(ace_table, 2, "Double Down")
    append_letter(ace_table, 8, "Hit")
    append_letter(ace_table, 2, "Double Down")
    append_letter(ace_table, 5, "Hit")
                  
    
    
    
def append_letter(strat_table, amount, letter):
    for i in range(amount):
        strat_table.append(letter)    

#dealers card is what dealer is showing, my hand is the sum of cards in my hand both need to be int and ace = 11
def find_action(dealers_card, my_hand, strat_table):
    if(my_hand > 21):
        action = "Bust"    
    elif(my_hand >= 17):
        #first row
        action = strat_table[dealers_card - 2]
    elif(my_hand == 16):
        #second row
        action = strat_table[dealers_card - 2 + (10 * 1)]
    elif(my_hand == 15):
        #third row
        action = strat_table[dealers_card - 2 + (10 * 2)]
    elif(my_hand == 14):
        action = strat_table[dealers_card - 2 + (10 * 3)]
    elif(my_hand == 13):
        action = strat_table[dealers_card - 2 + (10 * 4)]
    elif(my_hand == 12):
        action = strat_table[dealers_card - 2 + (10 * 5)]
    elif(my_hand == 11):
        action = strat_table[dealers_card - 2 + (10 * 6)]
    elif(my_hand == 10):
        action = strat_table[dealers_card - 2 + (10 * 7)]
    elif(my_hand == 9):
        action = strat_table[dealers_card - 2 + (10 * 8)]
    elif(my_hand >= 5 and my_hand <= 8):
        action = strat_table[dealers_card - 2 + (10 * 9)]
    
    return action
#cards_showing needs to be made up of ints or strings that are 1 || 2 ||  3 ect

def find_my_hand(cards_showing):
    total = 0
    for i in range(len(cards_showing)):
        if(cards_showing[i].best_rank_match in royalty):
            cards_showing[i].best_rank_match = 10
        if(cards_showing[i].best_rank_match == "Ace"):
            cards_showing[i].best_rank_match = 11

    
    for i in range(len(cards_showing)):
        total += int(cards_showing[i].best_rank_match)
    return total
    
    
