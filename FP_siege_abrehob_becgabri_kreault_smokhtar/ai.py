from getch import getch
from constants import *
import time, random
import select
import sys
import multiprocessing
from multiprocessing import Pipe
import threading
import time
from random import randint
random.seed()
from operator import itemgetter

################################################################################
# Toggle Student AI / Story Mode                                               #
################################################################################
USE_AI = True                                                                 #
STORY_MODE = False                                                             #
################################################################################

ACTION_INFO = {}
ACTION_INFO["first_turn_of_combat"] = True
# function decides if it is possible to KO an enemy with one of the weapons
# in your inventory. If you can, it returns its position in the backpack
# or if it is in the main hand (16) or offhand (15). It returns 10 if false

def weakest_weapon_to_ko(options):
    # create a list to order out of the dictionary (DOES NOT INCLUDE SHIELDS)
    key_for_weapon = "10"
    unordered_weapons = []
    for weapon in options["inventory"]["backpack_weapons"].items():
        if weapon[1]["type"] != "SHIELD":
            weapon_information = [weapon[0], weapon[1]["strength"], weapon[1]["type"]]
            unordered_weapons.append(weapon_information)
    if options["inventory"]["main_hand"] != None:
        main_hand_info = ["16", options["inventory"]["main_hand"]["strength"],
                             options["inventory"]["main_hand"]["type"]]
        unordered_weapons.append(main_hand_info)
    if options["inventory"]["off_hand"] != None and \
       options["inventory"]["off_hand"]["type"] != "SHIELD":
        off_hand_info = ["15", options["inventory"]["off_hand"]["strength"],
                            options["inventory"]["off_hand"]["type"]]
        unordered_weapons.append(off_hand_info)
    # put weapons in order of strength: greatest to least
    ordered_weapons = sorted(unordered_weapons, key=itemgetter(1), reverse=True)
    # check for the weakest option that will ko your enemy
    for weapon in ordered_weapons:
        if weapon[1] * (options["player"]["next_attack"] / 3.0) >= options["enemy"]["health"]:
            # if it will ko the enemy, return button needed to swap
            # !!!WARNING value 0 corresponds to the weapon already being in your main hand and
            # 1 corresponds to it being in your off hand!!!
            key_for_weapon = weapon[0]
    # if there is no option that works, return an out of range number (10)
    return key_for_weapon


'''
Requires: Nothing
Modifies: Nothing
Effects: Determines the maximum strength that we can achieve from our weapons
'''
def max_weapon_strength(options):
    # When I use the word "sword", it could also mean "club" or "claw"

    max_strength = 0

    # Used to check dual-wielding strengths
    sword_strengths = []

    # Finds all dual-wielding combinations
    sword_combinations_strengths = []
    max_combination_strength = 0
    # Checks the main hand weapon strength
    if options["inventory"]["main_hand"] == None:
        max_strength = 1
    else:
        max_strength = options["inventory"]["main_hand"]["strength"]
        # If it's not a bow, it must be a sword
        if options["inventory"]["main_hand"]["type"] != "BOW":
            sword_strengths.append(options["inventory"]["main_hand"]["strength"])

    # Checks the off hand weapon strength
    if (options["inventory"]["off_hand"] != None and
        options["inventory"]["off_hand"]["type"] != "SHIELD"):
        if options["inventory"]["off_hand"]["strength"] > max_strength:
            max_strength = options["inventory"]["off_hand"]["strength"]
        # (The off-hand weapon cannot be a bow)
        sword_strengths.append(options["inventory"]["off_hand"]["strength"])

    # For every weapon in the backpack, check if it is the strongest
    # (or it is a sword that could be used in the strongest sword combination)
    for weapon in options["inventory"]["backpack_weapons"].items():
        # weapon[0] refers to the key of each weapon, weapon[1] refers to its attributes
        curr_weapon = weapon[1]
        if curr_weapon["type"] != "SHIELD":
            if curr_weapon["strength"] > max_strength:
                max_strength = curr_weapon["strength"]
            if curr_weapon["type"] != "BOW":
                sword_strengths.append(curr_weapon["strength"])

    # If we can dual-wield
    if len(sword_strengths) > 1:
        # Create an array of all the sword combination strengths
        for i in range(len(sword_strengths)):
            for j in range(len(sword_strengths)):
                if i != j:
                    sword_combinations_strengths.append(sword_strengths[i] + 0.5 * sword_strengths[j])
        # Find the max sword combination strength
        for i in sword_combinations_strengths:
            if i > max_combination_strength:
                max_combination_strength = i
        # If dual-wielding deals more damage than our strongest bow
        if max_combination_strength > max_strength:
            # The "+ 0.25" is used in the weapon swapping function to signify
            # that we should be looking for 2 weapons when we decide to attack
            return max_combination_strength + 0.25
        # If our strongest bow deals more damage than dual-wielding
        else:
            return max_strength
    # If we can't dual-wield
    else:
        return max_strength



def combat_action(options):
    global ACTION_INFO

    # Update isLeave to determine if AI will fight or flee
    # When isLeave is true, return 'e'
    def is_leave():
        #if enemy will drop weapon
        if options["future"]["will_drop"] == True:
            if options["inventory"]["candles"] > 0 and options["future"]["escapes"][0] == True:
                # When health < 50 and no potions always escape
                if options["player"]["health"] < 50 and options["inventory"]["potions"] == 0:
                    return True
                #When enemy is has a health between 20-60
                if options["enemy"]["health"] >= 20 and (options["enemy"]["name"] == "Skeleton" or options["enemy"]["name"] == "Big Skeleton"
                                               or options["enemy"]["name"] == "Mud Troll"):
                    #Checks if health is too low to fight in situation
                    if options["inventory"]["potions"] == 0 and options["player"]["health"] < 100:
                        if max_weapon_strength(options) >= 20:
                            return False
                        else:
                            return True
            #Checks if AI should escape enemies with health from 60-100
                elif (options["enemy"]["name"] == "Three-Headed Wolf"
                      or options["enemy"]["name"] == "Evil Steve-n-Dorf" or options["enemy"]["name"] == "Ancient Dragon"):
                    if options["inventory"]["potions"] == 0:
                        return True
                    # Accounts if health and potions combined are too low
                    elif options["inventory"]["potions"] == 1 and options["player"]["health"] < 50:
                        return True
                    # If AI doesn't have strong enough weapons
                    elif max_weapon_strength(options) <= 7:
                        return True
                    else:
                        return False
            else:
                return False
        else:
            if options["inventory"]["candles"] > 0:
                if options["enemy"]["health"] >= 60 and options["future"]["escapes"][0] == True:
                    return True
                elif options["enemy"]["health"] >= 20 and options["player"]["health"] < 100 and \
                    options["future"]["escapes"][0] == True:
                    return True
            else:
                return False

    # Decide: will we stay or leave on the first turn of combat?
    if is_leave() and ACTION_INFO["first_turn_of_combat"]:
        return 'e'


    # function that returns true if you can deal more or equal damage to the enemy than they can to you
    # disadvantage describes what strength you need with your weapon in order for this to be true

    def can_deal_more_damage():
        if options["enemy"]["name"] == "Cave Goblin":
            # determining your disadvantage
            if options["inventory"]["main_hand"]["name"] == "Autograder":
                disadvantage = -1
            elif options["inventory"]["main_hand"]["name"] == "Plain Sword":
                disadvantage = 0
            elif options["inventory"]["main_hand"]["name"] == "Rusty Dagger":
                disadvantage = 1
            else:
                disadvantage = 2
            # comparing your strength to your enemies
            if options["player"]["next_attack"] >= options["enemy"]["next_attack"] + disadvantage:
                return True
            else:
                return False

        elif options["enemy"]["name"] == "Big Goblin":
            # determining disadvantage based on your attack vs. theirs
            if options["inventory"]["main_hand"]["name"] == "Autograder":
                if options["enemy"]["next_attack"] == 5:
                    disadvantage = -1
                # when enemy attack is not very strong
                else:
                    disadvantage = 0
            elif options["inventory"]["main_hand"]["name"] == "Plain Sword":
                disadvantage = 1
            elif options["inventory"]["main_hand"]["name"] == "Rusty Dagger":
                disadvantage = 2
            else:
                disadvantage = 2
            # comparing you and your enemy
            if options["player"]["next_attack"] >= options["enemy"]["next_attack"] + disadvantage:
                return True
            else:
                return False

        elif options["enemy"]["name"] == "Skeleton":
            # determining disadvantage
            if options["inventory"]["main_hand"]["name"] == "Autograder":
                disadvantage = 1
            elif options["inventory"]["main_hand"]["name"] == "Plain Sword":
                disadvantage = 2
            elif options["inventory"]["main_hand"]["name"] == "Rusty Dagger":
                disadvantage = 2
            else:
                disadvantage = 2
            # comparing you and your enemy
            if options["player"]["next_attack"] >= options["enemy"]["next_attack"] + disadvantage:
                return True
            else:
                return False
        # enemy is Steve-n-Dorf
        else:
            # never attack when enemy is above average
            if options["enemy"]["next_attack"] < 2:
                # determine disadvantage
                if options["inventory"]["main_hand"]["name"] == "Smelly Dagger" or \
                   options["inventory"]["main_hand"]["name"] == "Rusty Dagger":
                    # attack based on disadvantage
                    if options["player"]["next_attack"] >= options["enemy"]["next_attack"] + 2:
                        return True
                    else:
                        return False
                # you have a plain sword is your else scenario here (not considering gauntlet mode)
                else:
                    # remember, this is under the heading that enemy attack must be less than average
                    # so viable hits will be 5 and 4 for weak and 5,4, and 3 for very weak
                    if options["player"]["next_attack"] >= options["enemy"]["next_attack"] + 2:
                        return True
                    else:
                        return False
    #When to use fireball
    if options["inventory"]["fireballs"] > 0:
        # Checks if weapons aren't as good as fireball
        if options["enemy"]["health"] <= 25 and options["enemy"]["health"] >= 20 and max_weapon_strength(options) < 7:
            return 'f'
        # Throws fireball whenever next attack on Steve-n-Dorf is average or less
        elif options["enemy"]["name"] == "Evil Steve-n-Dorf" and options["future"]["player_attacks"] < 3:
            return 'f'
        elif ((options["enemy"]["name"] == "Three-Headed Wolf" or options["enemy"]["name"] == "Ancient Dragon" or
               options["enemy"]["name"] == "Evil Steve-n-Dorf") and options["steps_left"] < 500):
            if (max_weapon_strength(options) < 25 or options["future"]["player_attacks"] < 3) and options["enemy"]["health"] >= 25:
                return 'f'
        elif max_weapon_strength(options) <= 2 and options["enemy"]["health"] >= 20:
            return 'f'

    # If we have a bow and the enemy doesn't on the first turn of combat,
    # shoot the enemy
    if ACTION_INFO["first_turn_of_combat"]:
        ACTION_INFO["first_turn_of_combat"] = False
        if (options["inventory"]["main_hand"] != None and
            options["inventory"]["main_hand"]["type"] == "BOW"):
            return 'x'



    # Checks if AI needs to take potion or escape
    # Health needs to be one more than the max amount of damage enemy can deal
    # This is where 17, 25, 27, 39 and 47 come from
    if options["player"]["health"] < 17 and (options["enemy"]["name"] == "Cave Rat" or options["enemy"]["name"] == "Cave Goblin"
        or options["enemy"]["name"] == "Big Goblin"):
        if options["inventory"]["potions"] > 0:
            return 'i'
        elif options["inventory"]["candles"] > 0 and options["future"]["escapes"][0]== True:
            return 'e'
    elif options["player"]["health"] < 25 and (options["enemy"]["name"] == "Skeleton" or options["enemy"]["name"] == "Big Skeleton"
                                               or options["enemy"]["name"] == "Mud Troll"):
        if options["inventory"]["potions"] > 0:
            return 'i'
        elif options["inventory"]["candles"] > 0 and options["future"]["escapes"][0] == True:
            return 'e'
    elif options["player"]["health"] < 39 and (options["enemy"]["name"] == "Three-Headed Wolf" or options["enemy"]["name"] == "Evil Steve-n-Dorf"):
        if options["inventory"]["potions"] > 0:
            return 'i'
        elif options["inventory"]["candles"] > 0 and options["future"]["escapes"][0] == True:
            return 'e'
    elif options["enemy"]["name"] == "Ancient Dragon":
        if ((options["player"]["health"] < 47 and options["enemy"]["item"]["type"] == "CLAWS")
            or (options["player"]["health"] < 27 and options["enemy"]["item"]["type"] == "SHIELD")):
            if options["inventory"]["potions"] > 0:
                return 'i'
            elif options["inventory"]["candles"] > 0 and options["future"]["escapes"][0] == True:
                return 'e'


    # The following blocks of code deal with escaping in the middle of a battle due
    # to the loss of our good weapons

    # If we have fairly crappy weapons and the enemy could beat the crap out of us
    # (because it has a lot of health), escape
    if options["inventory"]["candles"] > 0 and max_weapon_strength(options) < 7 and \
       options["future"]["escapes"][0] == True and ((options["enemy"]["health"] >= 60 and
       options["future"]["will_drop"] == True) or (options["enemy"]["health"] >= 40 and
       options["future"]["will_drop"] == False)):
        return 'e'

    # If we have really crappy weapons and the enemy could kind of beat the crap out
    # of us (because it has a decent amount of health), blast it with a fireball, and
    # if we can't do that, escape
    if max_weapon_strength(options) < 5 and options["enemy"]["health"] >= 30:
        if options["inventory"]["fireballs"] != 0:
            return 'f'
        elif options["future"]["escapes"][0] == True and options["inventory"]["candles"] > 0:
            return 'e'


    # Other situations to use a fireball
    if options["inventory"]["fireballs"] > 0:
        # Checks if weapons aren't as good as fireball
        if options["enemy"]["health"] <= 25 and options["enemy"]["health"] >= 20 and max_weapon_strength(options) < 7:
            return 'f'
        # Throw a fireball whenever we have bad weapons and the enemy has a lot of health
        # and our next attack is not very good
        elif (options["future"]["player_attacks"][0] < 3 and
             options["enemy"]["health"] >= 80 and
             max_weapon_strength(options) <= 12) or \
             (options["future"]["player_attacks"][0] < 3 and
             options["enemy"]["health"] >= 50 and
             max_weapon_strength(options) <= 7) or \
             (options["future"]["player_attacks"][0] < 4 and
             options["enemy"]["health"] >= 25 and
             max_weapon_strength(options) <= 20 and
             options["inventory"]["potions"] == 0):
            return 'f'

    # if you decide to fight
    if not (is_leave() and ACTION_INFO["first_turn_of_combat"]):
        # killing the enemy with one weapon
        # get the value that gets you the key of the weakest weapon that will let you KO
        potential_weapon_to_one_hit = weakest_weapon_to_ko(options)
        '''
        # look for the strength of the item that matches that key
        for weapon in options["inventory"]["backpack_weapons"].items():
            if weapon[0] == potential_weapon_to_one_hit:
                weakest_strength_to_ko = weapon["strength"]
        '''
        # if that thing is something in your backpack
        if '2' <= potential_weapon_to_one_hit and potential_weapon_to_one_hit <= '7':
            ACTION_INFO['source_hand'] = potential_weapon_to_one_hit
            ACTION_INFO['target_hand'] = 'main_hand'
            return '1'
        # if it's in your main hand, keep it in your main hand
        elif potential_weapon_to_one_hit == '16':
            return 'x'
        # WARNING not accounting for weapon being in off hand, that is ignored and cannot be dealt with
        else:
            # See if we have a shield in our backpack
            shield_in_backpack = False
            for weapon in options["inventory"]["backpack_weapons"].items():
                if weapon[1]["type"] == "SHIELD":
                    shield_in_backpack = True

            # CHECK AND SEE IF PLAYER NEXT ATTACK IS LESS THAN OR EQUAL TO THEIR ATTACK
            if options["player"]["next_attack"] <= options["enemy"]["next_attack"]:
                if ((options["inventory"]["off_hand"] == None or
                    options["inventory"]["off_hand"]["type"] != "SHIELD") and
                    shield_in_backpack):
                    strongest_shield_index = -1
                    strongest_shield_strength_val = 0
                    for weapon in options['inventory']["backpack_weapons"].items():
                        if weapon[1]["type"] == "SHIELD" and weapon[1]["strength"] > strongest_shield_strength_val:
                            strongest_shield_strength_val = weapon[1]["strength"]
                            strongest_shield_index = weapon[0]
                    ACTION_INFO['source_hand'] = strongest_shield_index
                    ACTION_INFO['target_hand'] = 'off_hand'
                    return '2'
                if options["inventory"]["off_hand"] != None and \
                    options["inventory"]["off_hand"]["type"] == "SHIELD" and \
                    options["future"]["blocks"][0] == True:
                    return 'c'

            # this code is when austin returns to me a .25 for highest damage possible
            # call austin's function and decode it: multiply by 4 mod 4 if rem is 1 or 3:
            # CALLING AUSTIN's FUNCTION
            highest_strength_weapon = max_weapon_strength(options)
            decode = (highest_strength_weapon * 4) % 4
            if decode == 1 or decode == 3:
                unordered_weapons = []
                # puts all weapons for dual wield into a nested list
                for weapon in options["inventory"]["backpack_weapons"].items():
                    if weapon[1]["type"] != "SHIELD" and weapon[1]["type"] != 'BOW':
                        weapon_information = [weapon[0], weapon[1]["strength"], weapon[1]["type"]]
                        unordered_weapons.append(weapon_information)
                if options["inventory"]["main_hand"] != None and \
                    options["inventory"]["main_hand"]["type"] != "BOW":
                    main_hand_info = ["16", options["inventory"]["main_hand"]["strength"],
                            options["inventory"]["main_hand"]["type"]]
                    unordered_weapons.append(main_hand_info)
                if options["inventory"]["off_hand"] != None and \
                    options["inventory"]["off_hand"]["type"] != "SHIELD":
                    off_hand_info = ["15", options["inventory"]["off_hand"]["strength"],
                        options["inventory"]["off_hand"]["type"]]
                    unordered_weapons.append(off_hand_info)
            # put weapons in order of strength: greatest to least
                ordered_weapons = sorted(unordered_weapons, key=itemgetter(1), reverse=True)
                strength_max = ordered_weapons[0][1]
                second_strength_max = ordered_weapons[1][1]

                # If possible, find the strongest weapon we have and put it into our main hand
                if options["inventory"]["main_hand"] == None or \
                   options["inventory"]["main_hand"]["strength"] != strength_max:
                    # If the strongest weapon is not in our off hand, find it and put
                    # it into our main hand
                    if ordered_weapons[0][0] != "15":
                        ACTION_INFO['source_hand'] = ordered_weapons[0][0]
                        ACTION_INFO['target_hand'] = 'main_hand'
                        return '1'
                    # If the second-strongest weapon is not already in our main hand,
                    # find it and put it into our main hand
                    elif options["inventory"]["main_hand"] == None or \
                         options["inventory"]["main_hand"]["strength"] != second_strength_max:
                        ACTION_INFO['source_hand'] = ordered_weapons[1][0]
                        ACTION_INFO['target_hand'] = 'main_hand'
                        return '1'
                    # If our two strongest weapons are in our main hand and off hand, but in
                    # the wrong order, don't worry about it and just attack
                    else:
                        return 'x'

                # If possible, find the second-strongest weapon we have and put it into our off hand
                if options["inventory"]["off_hand"] == None or \
                   options["inventory"]["off_hand"]["strength"] != second_strength_max:
                    # If the second-strongest weapon is not in our main hand, find it and put
                    # into our off hand
                    if ordered_weapons[1][0] != "16":
                        ACTION_INFO['source_hand'] = ordered_weapons[1][0]
                        ACTION_INFO['target_hand'] = 'off_hand'
                        return '2'
                    # If the second-strongest weapon is in our main hand (which could only
                    # happen if they second-strongest and the strongest are of the same
                    # strength), find the 'strongest' weapon and put it into our off hand
                    else:
                        ACTION_INFO['source_hand'] = ordered_weapons[0][0]
                        ACTION_INFO['target_hand'] = 'off_hand'
                        return '2'

            # If we plan to attack with only one weapon
            elif options["inventory"]["main_hand"] == None or \
                 options["inventory"]["main_hand"]["strength"] != highest_strength_weapon:
                highest_weapon_index = 20
                for weapon in options["inventory"]["backpack_weapons"].items():
                    if weapon[1]["type"] != "SHIELD" and \
                       weapon[1]["strength"] == highest_strength_weapon:
                        highest_weapon_index = weapon[0]
                if '2' <= highest_weapon_index and highest_weapon_index <= '7':
                    ACTION_INFO['source_hand'] = highest_weapon_index
                    ACTION_INFO['target_hand'] = 'main_hand'
                    return '1'
                # otherwise it is in your main hand or your off hand and you're good to go no more switching

            # If we have everything we need, ATTACK!!!!
            return 'x'


def movement_action(options):
    global ACTION_INFO
    ACTION_INFO["first_turn_of_combat"] = True

    # If we have extra repels, use them all at the end of the game
    # (use them when we are about to run out of steps or run out of health)
    if ((options["invuln_steps"] == 0 or options["invuln_steps"] == 1) and
        (options["steps_left"] <= options["inventory"]["repels"] * 10 or
        (options["inventory"]["repels"] != 0 and
        options["inventory"]["potions"] == 0))):
        return 'r'

    # If in the next 8 moves the map danger stays above "Safe", the map danger
    # doesn't decrease by a lot or it's not safe to hide when we should,
    # and we're past floor 3, use a repel
    if options["inventory"]["repels"] != 0 and options["invuln_steps"] == 0 and \
       options["level"] >= 4:
        use_repel = True
        initial_map_danger = options["map_danger"]
        for i in range(8):
            if options["future"]["map_danger"][i] < 4 or \
               (options["future"]["map_danger"][i] < initial_map_danger - 3 and
               options["future"]["hide_danger"][i] < 2):
                use_repel = False
        if use_repel:
            return 'r'


    # If there is at least 1 potion in inventory and health is less than 26,
    # use a potion
    if options["inventory"]["potions"] != 0 and \
       options["player"]["health"] <= 25:
        return 'i'


    def to_percentage(danger):
        return danger * 0.03 + 0.03

    # Abbreviations: mEP = "map encounter percentage" and
    #                hEP = "hide encounter percentage"
    mEP = to_percentage(options["map_danger"])
    hEP = to_percentage(options["hide_danger"])
    mEP1 = to_percentage(options["future"]["map_danger"][1])
    hEP1 = to_percentage(options["future"]["hide_danger"][1])
    mEP2 = to_percentage(options["future"]["map_danger"][2])
    hEP2 = to_percentage(options["future"]["hide_danger"][2])
    mEP3 = to_percentage(options["future"]["map_danger"][3])


    # Our AI runs out of moves over half the time, so we commented out the hiding code
    # below so that we could make it even further.  Although it makes it so we don't go
    # as far when we die, it's much more entertaining to go 50 floors than 45.

    # if options["invuln_steps"] == 0:
        # Hide if less likely to get into an encounter by hiding this turn and moving
        # the next than moving this turn
        # if hEP + (1 - hEP) * mEP1 < mEP:
        #    return 'h'
        # Hide if less likely to get into an encounter by hiding this turn and next then
        # moving on the following turn
        # elif hEP + (1 - hEP) * hEP1 + (1 - hEP) * (1 - hEP1) * mEP2 < mEP:
        #     return 'h'
        # Hide if less likely to get into an encounter by hiding 3 turns in a row
        # and then moving
        # elif hEP + (1 - hEP) * hEP1 + (1 - hEP) * (1 - hEP1) * hEP2 + \
        #     (1 - hEP) * (1 - hEP1) * (1 - hEP2) * mEP3 < mEP:
        #     return 'h'
    # If hiding 4 times in a row was actually beneficial, we still wouldn't do it
    # because it takes too many moves

    return 'x'


def item_action(options):
    global ACTION_INFO # Necessary for reading and writing the global ACTION_INFO dictionary

    numShields = 0;
    numBows = 0;
    numSCC = 0;
    weakShieldDur = 100;
    weakShieldIndex = -1;
    weakBowStr = 100;
    weakBowIndex = -1;
    weakSCCStr = 100;
    weakSCCIndex = -1;

    # OH SHIELD 
    if (options["inventory"]["off_hand"] != None and
        options["inventory"]["off_hand"]["type"] == "SHIELD"):
        numShields += 1
        if (options["inventory"]["off_hand"]["durability"] < weakShieldDur):
            weakShieldDur = options["inventory"]["off_hand"]["durability"]
            weakShieldIndex = 2
    # MH SWWORD
    if (options["inventory"]["main_hand"] != None and
        options["inventory"]["main_hand"]["type"] == "SWORD"):
        numSCC += 1
        if (options["inventory"]["main_hand"]["strength"] < weakSCCStr):
            weakSCCStr = options["inventory"]["main_hand"]["strength"]
            weakSCCIndex = 1
    # OH SWORD
    if (options["inventory"]["off_hand"] != None and
        options["inventory"]["off_hand"]["type"] == "SWORD"):
        numSCC += 1
        if (options["inventory"]["off_hand"]["strength"] < weakSCCStr):
            weakSCCStr = options["inventory"]["off_hand"]["strength"]
            weakSCCIndex = 2
    # MH CLAWS
    if (options["inventory"]["main_hand"] != None and
        options["inventory"]["main_hand"]["type"] == "CLAWS"):
        numSCC += 1
        if (options["inventory"]["main_hand"]["strength"] < weakSCCStr):
            weakSCCStr = options["inventory"]["main_hand"]["strength"]
            weakSCCIndex = 1
    # OH CLAWS
    if (options["inventory"]["off_hand"] != None and
        options["inventory"]["off_hand"]["type"] == "CLAWS"):
        numSCC += 1
        if (options["inventory"]["off_hand"]["strength"] < weakSCCStr):
            weakSCCStr = options["inventory"]["off_hand"]["strength"]
            weakSCCIndex = 2
    # MH CLUB
    if (options["inventory"]["main_hand"] != None and
        options["inventory"]["main_hand"]["type"] == "CLUB"):
        numSCC += 1
        if (options["inventory"]["main_hand"]["strength"] < weakSCCStr):
            weakSCCStr = options["inventory"]["main_hand"]["strength"]
            weakSCCIndex = 1
    # OH CLUB
    if (options["inventory"]["off_hand"] != None and
        options["inventory"]["off_hand"]["type"] == "CLUB"):
        numSCC += 1
        if (options["inventory"]["off_hand"]["strength"] < weakSCCStr):
            weakSCCStr = options["inventory"]["off_hand"]["strength"]
            weakSCCIndex = 2
    # BOW
    if (options["inventory"]["main_hand"] != None and
        options["inventory"]["main_hand"]["type"] == "BOW"):
        numBows += 1
        if (options["inventory"]["main_hand"]["strength"] < weakBowStr):
            weakBowStr = options["inventory"]["main_hand"]["strength"]
            weakBowIndex = 1

    # Traverse the entire list of items
    for x in options['inventory']['backpack_weapons'].items():
        if x[1]['type'] == "SHIELD":
            numShields += 1
            if (x[1]["strength"] < weakShieldDur):
                weakShieldDur = x[1]["durability"]
                weakShieldIndex = x[0]
        elif x[1]['type'] == "SWORD" or x[1]['type'] == "CLAWS" or x[1]['type'] == "CLUB":
            numSCC += 1
            if (x[1]["strength"] < weakSCCStr):
                weakSCCStr = x[1]["strength"]
                weakSCCIndex = x[0]
        elif x[1]['type'] == "BOW":
            numBows += 1
            if (x[1]["strength"] < weakBowStr):
                weakBowStr = x[1]["strength"]
                weakBowIndex = x[0]


    ############################################################################         
    # Empty Space in Inventory
    ############################################################################
    if options["inventory"]["backpack_has_space"] == True:
        # SHIELD DROPPED
        if options["enemy"]["item"]["type"] == "SHIELD":
            if (numShields < 1):
                return '8'
            else:
                # OH SHIELD
                if (weakShieldDur <= options["enemy"]["item"]["durability"]):
                    return str(weakShieldIndex)
                #should never get here
                return '9'
        # SWORD DROPPED OR CLAWS DROPPED OR CLUB DROPPED
        elif (options["enemy"]["item"]["type"] == "SWORD" or 
            options["enemy"]["item"]["type"] == "CLAWS" or
            options["enemy"]["item"]["type"] == "CLUB"):
           if (numSCC < 4):
                return '8'
           else:
                if (weakSCCStr <= options["enemy"]["item"]["strength"]):
                    return str(weakSCCIndex)
                #should never get here
                return '9'
        # BOW DROPPED
        elif options["enemy"]["item"]["type"] == "BOW":
            if (numBows < 1):
                return '8'
            else:
                if (weakBowStr <= options["enemy"]["item"]["strength"]):
                    return str(weakBowIndex)
                #should never get here
                return '9'   
        # should never get (for random new item type)
        else: 
            return '9'

    ############################################################################
    # No Empty Space in Inventory
    ############################################################################
    elif options["inventory"]["backpack_has_space"] == False:
        # SHIELD DROPPED
        if options["enemy"]["item"]["type"] == "SHIELD":
            if (numShields < 1):
                return '9'
            else:
                # OH SHIELD
                if (weakShieldDur <= options["enemy"]["item"]["durability"]):
                    return str(weakShieldIndex)
                #should never get here
                return '9'
        # SWORD DROPPED OR CLAWS DROPPED OR CLUB DROPPED
        elif (options["enemy"]["item"]["type"] == "SWORD" or 
            options["enemy"]["item"]["type"] == "CLAWS" or
            options["enemy"]["item"]["type"] == "CLUB"):
           if (numSCC < 4):
                return '9'
           else:
                if (weakSCCStr <= options["enemy"]["item"]["strength"]):
                    return str(weakSCCIndex)
                #should never get here
                return '9'
        # BOW DROPPED
        elif options["enemy"]["item"]["type"] == "BOW":
            if (numBows < 1):
                return '9'
            else:
                if (weakBowStr <= options["enemy"]["item"]["strength"]):
                    return str(weakBowIndex)
                #should never get here
                return '9'   
        # should never get (for random new item type)
        else: 
            return '9'
    # should never get (for random new item type)
    return '9'


def swap_select_weapon(options):
    global ACTION_INFO # Necessary for reading and writing the global ACTION_INFO dictionary

    return str(ACTION_INFO['source_hand'])

#####################################################################################
# Game Driver for your AI. Don't modify this section.                               #
#####################################################################################
def _check_loop():                                                                  #
    raw_input()                                                                     #
    USE_AI = False                                                                  #
                                                                                    #
class User(object):                                                                 #
    def __init__(self):                                                             #
        self.input_check = None                                                     #
        self.set_ai(USE_AI)                                                         #
                                                                                    #
    def select(self, options):                                                      #
        if options['situation'] == 'COMBAT': return combat_action(options)          #
        elif options['situation'] == 'ITEM': return item_action(options)            #
        elif options['situation'] == 'MOVE': return movement_action(options)        #
        elif options['situation'] == 'SWAP': return swap_select_weapon(options)     #
        else: raise Exception("Bad move option: {0}".format(options['situation']))  #
                                                                                    #
    def set_ai(self, setting):                                                      #
        global USE_AI                                                               #
        if setting:                                                                 #
            # launch subprocess to handle input                                     #
            USE_AI = True                                                           #
            self.input_check = threading.Thread(target=_check_loop)                 #
            self.input_check.daemon = True                                          #
            self.input_check.start()                                                #
        else:                                                                       #
            # end the subprocess                                                    #
            if self.input_check and self.input_check.is_alive():                    #
                self.input_check.join(GAME_SPEED)                                   #
            USE_AI = False                                                          #
                                                                                    #
                                                                                    #
    def __move__(self, options):                                                    # 
        if not USE_AI:                                                              #
            usr = getch()                                                           #
            if ord(usr) == 13:                                                      #
                self.set_ai(True)                                                   #
                return self.select(options).lower()                                 #
            return usr.lower()                                                      #
                                                                                    #
        time.sleep(GAME_SPEED)                                                      #
        if self.input_check and not self.input_check.is_alive():                    #
            self.set_ai(False)                                                      #
            return getch().lower()                                                  #
        return self.select(options).lower()                                         #
                                                                                    #
                                                                                    #
#####################################################################################
