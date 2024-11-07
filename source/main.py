import random
def nachalo():
    print("                                 WUMPUS")
    print("               CREATIVE COMPUTING  MORRISTOWN, NEW JERSEY")
    print()
    print()
    print()
    response = input("INSTRUCTIONS (Y-N)? ").strip().upper()
    if response == "Y":
        print_instructions()

def print_instructions():
    print("WELCOME TO 'HUNT THE WUMPUS'")
    print("  THE WUMPUS LIVES IN A CAVE OF 20 ROOMS. EACH ROOM")
    print("HAS 3 TUNNELS LEADING TO OTHER ROOMS. (LOOK AT A")
    print("DODECAHEDRON TO SEE HOW THIS WORKS-IF YOU DON'T KNOW")
    print("WHAT A DODECAHEDRON IS, ASK SOMEONE)")
    print()
    print("     HAZARDS:")
    print(" BOTTOMLESS PITS - TWO ROOMS HAVE BOTTOMLESS PITS IN THEM")
    print("     IF YOU GO THERE, YOU FALL INTO THE PIT (& LOSE!)")
    print(" SUPER BATS - TWO OTHER ROOMS HAVE SUPER BATS. IF YOU")
    print("     GO THERE, A BAT GRABS YOU AND TAKES YOU TO SOME OTHER")
    print("     ROOM AT RANDOM. (WHICH MAY BE TROUBLESOME)")
    print()
    print("     WUMPUS:")
    print(" THE WUMPUS IS NOT BOTHERED BY HAZARDS (HE HAS SUCKER")
    print(" FEET AND IS TOO BIG FOR A BAT TO LIFT).  USUALLY")
    print(" HE IS ASLEEP.  TWO THINGS WAKE HIM UP: YOU SHOOTING AN")
    print("ARROW OR YOU ENTERING HIS ROOM.")
    print("     IF THE WUMPUS WAKES HE MOVES (P=.75) ONE ROOM")
    print(" OR STAYS STILL (P=.25).  AFTER THAT, IF HE IS WHERE YOU")
    print(" ARE, HE EATS YOU UP AND YOU LOSE!")
    print()
    print("     YOU:")
    print(" EACH TURN YOU MAY MOVE OR SHOOT A CROOKED ARROW")
    print("   MOVING:  YOU CAN MOVE ONE ROOM (THRU ONE TUNNEL)")
    print("   ARROWS:  YOU HAVE 5 ARROWS.  YOU LOSE WHEN YOU RUN OUT")
    print("   EACH ARROW CAN GO FROM 1 TO 5 ROOMS. YOU AIM BY TELLING")
    print("   THE COMPUTER THE ROOM#S YOU WANT THE ARROW TO GO TO.")
    print("   IF THE ARROW CAN'T GO THAT WAY (IF NO TUNNEL) IT MOVES")
    print("   AT RANDOM TO THE NEXT ROOM.")
    print("     IF THE ARROW HITS THE WUMPUS, YOU WIN.")
    print("     IF THE ARROW HITS YOU, YOU LOSE.")
    print()
    print("    WARNINGS:")
    print("     WHEN YOU ARE ONE ROOM AWAY FROM A WUMPUS OR HAZARD,")
    print("     THE COMPUTER SAYS:")
    print(" WUMPUS:  'I SMELL A WUMPUS'")
    print(" BAT   :  'BATS NEARBY'")
    print(" PIT   :  'I FEEL A DRAFT'")
    print()

def setup_cave():
    return {
        1: [2, 5, 8],
        2: [1, 3, 10],
        3: [2, 4, 12],
        4: [3, 5, 14],
        5: [1, 4, 6],
        6: [5, 7, 15],
        7: [6, 8, 17],
        8: [1, 7, 9],
        9: [8, 10, 18],
        10: [2, 9, 11],
        11: [10, 12, 19],
        12: [3, 11, 13],
        13: [12, 14, 20],
        14: [4, 13, 15],
        15: [6, 14, 16],
        16: [15, 17, 20],
        17: [7, 16, 18],
        18: [9, 17, 19],
        19: [11, 18, 20],
        20: [13, 16, 19]
    }

def setup_game():
    locations = {
        "player": 1,
        "wumpus": 7,
        "pits": [3, 15],
        "bats": [10, 18]
    }
    return locations, 5  # 5 arrows

def print_location(locations, cave):
    print(f"YOU ARE IN ROOM  {locations['player']}")
    print("TUNNELS LEAD TO ", '   '.join(map(str, cave[locations['player']])))
    print()

def hazard_warning(locations, cave):
    player_room = locations['player']
    hazards = {"wumpus": "I SMELL A WUMPUS!", "pits": "I FEEL A DRAFT", "bats": "BATS NEARBY!"}
    for hazard, warning in hazards.items():
        if hazard == "pits" or hazard == "bats":
            rooms = locations[hazard]
        else:
            rooms = [locations[hazard]]
        for room in rooms:
            if room in cave[player_room]:
                print(warning)

def move_player(locations, cave):
    while True:
        try:
            new_room = int(input("WHERE TO? "))
            if new_room in cave[locations['player']]:
                locations['player'] = new_room
                break
            else:
                print("NOT POSSIBLE -")
        except ValueError:
            print("PLEASE ENTER A VALID ROOM NUMBER")

def move_wumpus(locations, cave):
    if random.random() < 0.75:
        locations['wumpus'] = random.choice(cave[locations['wumpus']])

def check_hazards(locations):
    if locations['player'] == locations['wumpus']:
        print("... OOPS! BUMPED A WUMPUS!")
        move_wumpus(locations, cave)
        if locations['player'] == locations['wumpus']:
            print("TSK TSK TSK - WUMPUS GOT YOU!")
            return -1
    elif locations['player'] in locations['pits']:
        print("YYYYIIIIEEEE . . . FELL IN PIT")
        return -1
    elif locations['player'] in locations['bats']:
        print("ZAP--SUPER BAT SNATCH! ELSEWHEREVILLE FOR YOU!")
        locations['player'] = random.randint(1, 20)
        return check_hazards(locations)
    return 0

def shoot_arrow(locations, cave, arrows):
    if arrows <= 0:
        print("NO ARROWS LEFT!")
        return 0, arrows
    try:
        num_rooms = int(input("NO. OF ROOMS (1-5): "))
        if num_rooms < 1 or num_rooms > 5:
            raise ValueError
    except ValueError:
        print("INVALID INPUT, TRY AGAIN.")
        return shoot_arrow(locations, cave, arrows)

    path = []
    for _ in range(num_rooms):
        try:
            room = int(input("ROOM #: "))
            path.append(room)
        except ValueError:
            print("INVALID INPUT, TRY AGAIN.")
            return shoot_arrow(locations, cave, arrows)

    current_room = locations['player']
    for room in path:
        if room in cave[current_room]:
            current_room = room
        else:
            current_room = random.choice(cave[current_room])
        if current_room == locations['wumpus']:
            print("AHA! YOU GOT THE WUMPUS!")
            return 1, arrows - 1
        elif current_room == locations['player']:
            print("OUCH! ARROW GOT YOU!")
            return -1, arrows - 1

    print("MISSED")
    move_wumpus(locations, cave)
    return 0, arrows - 1

def main():
    cave = setup_cave()
    locations, arrows = setup_game()

    print("HUNT THE WUMPUS")
    print()
    while True:
        hazard_warning(locations, cave)
        print_location(locations, cave)
        action = input("SHOOT OR MOVE (S-M)? ").strip().upper()
        if action == "S":
            result, arrows = shoot_arrow(locations, cave, arrows)
        elif action == "M":
            move_player(locations, cave)
            result = check_hazards(locations)
        else:
            print("INVALID OPTION. PLEASE ENTER 'S' OR 'M'.")
            continue

        if result == -1:
            print("HA HA HA - YOU LOSE!")
            break
        elif result == 1:
            print("HEE HEE HEE - THE WUMPUS'LL GETCHA NEXT TIME!!")
            break

        if arrows == 0:
            print("YOU'VE RUN OUT OF ARROWS. YOU LOSE!")
            break

if __name__ == "__main__":
    nachalo()
    main()
