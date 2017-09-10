from constants import ITEM_DURABILITIES
enemy_freqs = [0.08, 0.10, 0.10, 0.12, 0.12, 0.15, 0.15, 0.18]

enemies = [
    {
        "name": "Cave Rat",
        "image": "RAT",
        "health": {
            "min": 1,
            "max": 3,
        },
        "EXP": 1,
        "items": [
            {"name": "Cave Rat", "type": "iRAT", "strength": 2, 'durability': ITEM_DURABILITIES['Knife']},
            {"name": "Cave Rat", "type": "iRAT", "strength": 3, 'durability': ITEM_DURABILITIES['Flimsy Shield']},
        ]
    },
    {
        "name": "Cave Goblin",
        "image": "GOBLIN",
        "health": {
            "min": 5,
            "max": 8,
        },
        "EXP": 4,
        "items": [
            {"name": "Cave Goblin", "type": "iGOBLIN", "strength": 5, 'durability': ITEM_DURABILITIES['Smelly Dagger']},
            {"name": "Cave Goblin", "type": "iGOBLIN", "strength": 4, 'durability': ITEM_DURABILITIES['Slimy Bow']},
            {"name": "Cave Goblin", "type": "iGOBLIN", "strength": 5, 'durability': ITEM_DURABILITIES['Moldy Shield']},
        ]
    },
    {
        "name": "Big Goblin",
        "image": "GOBLIN",
        "health": {
            "min": 8,
            "max": 10,
        },
           "EXP": 6,
        "items": [
            {"name": "Big Goblin", "type": "iGOBLIN", "strength": 6, 'durability': ITEM_DURABILITIES['Rusty Dagger']},
            {"name": "Big Goblin", "type": "iGOBLIN", "strength": 5, 'durability': ITEM_DURABILITIES['Grimy Bow']},
            {"name": "Big Goblin", "type": "iGOBLIN", "strength": 6, 'durability': ITEM_DURABILITIES['Old Shield']},
        ]
    },
    {
        "name": "Skeleton",
        "image": "SKELETON",
        "health": {
            "min": 20,
            "max": 30,
        },
        "EXP": 13,
        "items": [
            {"name": "Skeleton", "type": "iSKELETON", "strength": 7, 'durability': ITEM_DURABILITIES['Plain Sword']},
            {"name": "Skeleton", "type": "iSKELETON", "strength": 6, 'durability': ITEM_DURABILITIES['Plain Bow']},
            {"name": "Skeleton", "type": "iSKELETON", "strength": 7, 'durability': ITEM_DURABILITIES['Buckler']},
        ]
    },
    {
        "name": "Big Skeleton",
        "image": "SKELETON",
        "health": {
            "min": 30,
            "max": 45,
        },
        "EXP": 20,
        "items": [
            {"name": "Big Skeleton", "type": "iSKELETON", "strength": 8, 'durability': ITEM_DURABILITIES['Good Sword']},
            {"name": "Big Skeleton", "type": "iSKELETON", "strength": 7, 'durability': ITEM_DURABILITIES['Strong Bow']},
            {"name": "Big Skeleton", "type": "iSKELETON", "strength": 8, 'durability': ITEM_DURABILITIES['Big Shield']},
        ]
    },
    {
        "name": "Mud Troll",
        "image": "TROLL",
        "health": {
            "min": 50,
            "max": 60,
        },
        "EXP": 30,
        "items": [
            {"name": "Mud Troll", "type": "iTROLL", "strength": 9, 'durability': ITEM_DURABILITIES['Club of Whacking']},
            {"name": "Mud Troll", "type": "iTROLL", "strength": 8, 'durability': ITEM_DURABILITIES['Powerful Bow']},
            {"name": "Mud Troll", "type": "iTROLL", "strength": 9, 'durability': ITEM_DURABILITIES['Brawny Shield']},
        ]
    },
    {
        "name": "Three-Headed Wolf",
        "image": "DOG",
        "health": {
            "min": 60,
            "max": 100,
        },
        "EXP": 50,
        "items": [
            {"name": "Three-Headed Wolf", "type": "iWOLF", "strength": 14, 'durability': ITEM_DURABILITIES['Wolf Claws']},
        ]
    },
    {
        "name": "Ancient Dragon",
        "image": "DRAGON",
        "health": {
            "min": 80,
            "max": 100,
        },
        "EXP": 64,
        "items": [
            {"name": "Ancient Dragon", "type": "iDRAGON", "strength": 18, 'durability': ITEM_DURABILITIES['Dragon Claws']},
            {"name": "Ancient Dragon", "type": "iDRAGON", "strength": 10, 'durability': ITEM_DURABILITIES['Dragonhide Shield']},
        ]
    },
]


STEVENDORF_STATS = {
        "name": "Evil Steve-n-Dorf",
        "image": "STEVENDORF",
        "health": {
            "min": 130,
            "max": 130,
        },
        "EXP": 100,
        "items": [
            {"name": "Evil Steve-n-Dorf", "type": "SWORD", "strength": 15, 'durability': ITEM_DURABILITIES['Autograder']},
        ]
    }
