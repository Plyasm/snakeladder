##################################################IMPORTS AND GLOBAL VARIABLES#######################################
import random
game_board = 0
players = []
debug = False
###################################################VALIDATION###################################################
def validate_menu(choice):
    if choice.isdigit() and (int(choice) > 0 and int(choice) < 5):
        return True
    return False

def validate_number(choice):
    if choice.isdigit():
        return True
    return False

def validate_game_option(choice):
    if choice.isdigit() and (int(choice) > 0 and int(choice) < 4):
        return True
    return False

def validate_player_name(choice):
    global players
    for player in players:
        if str(player) == choice:
            return False
    return True

def validate_choice(validate_func, question, error_msg):
    done = False
    while not done:
        choice = input(question)
        done = validate_func(choice)
        if not done:
            print(error_msg)
    return choice

############################################CLASSES###########################################
class Place:
    def __init__(self, name):
        self.name = name
        self.next_place = None
        self.prev_place = None
        self.special = 0
    def set_next(self, next_place):
        self.next_place = next_place
    def get_next(self):
        return self.next_place
    def set_prev(self, prev_place):
        self.prev_place = prev_place
    def get_prev(self):
        return self.prev_place
    def __str__(self):
        return self.name

class Snake_Ladder(Place):
    def __init__(self, name, move_step):
        Place.__init__(self, name)
        self.move_step = move_step
    def get_move_step(self):
        return self.move_step
    def __str__(self):
        if self.move_step != None:
            return self.name + "(" +str(self.move_step)+ ")"
        else:
            return self.name

class Player():
    def __init__(self, name):
        self.name = name
        self.place = None

    def row_dice(self):
        return random.randint(1, 6)

    def set_place(self, place):
        self.place = place

    def get_place(self):
        return self.place

    def __str__(self):
        return self.name# + "@" + str(self.place)

########################################################FUNCTIONS####################################################
def Connect(place1, place2):#connect two places next to each other
    place1.set_next(place2)
    place2.set_prev(place1)

def display_board():#board display
    global game_board
    global players
    cur = game_board
    while cur != None:#go through all spaces
        on_space = []
        on = ''
        for player in players:#find player occupied spaces
            if player.get_place() == str(cur):
                on_space.append(str(player))
        spaces = 11 - len(str(cur))#formatting of gui
        if len(on_space) != 0:
            for person in on_space:
                on += person + " "
            print(str(cur) + spaces * " " + on[:-1])#printing spacename together with players on it
        else:
            print(str(cur))
        cur = cur.get_next()

def get_place(player):#return player occupied space
    global game_board
    cur = game_board
    while cur != None:
        if player.get_place() == str(cur):
            return cur
        cur = cur.get_next()

def create_game():#make game board
    global game_board
    #getting numbers
    snake_num = int(validate_choice(validate_number, "Enter the number of Snakes in game: ", "Error, please enter a number."))
    ladder_num = int(validate_choice(validate_number, "Enter the number of Ladder in game: ", "Error, please enter a number."))
    normal_num = int(validate_choice(validate_number, "Enter the number of Normal spaces in game: ", "Error, please enter a number."))
    #generate placements
    placement = []
    for i in range(snake_num):
        placement.append("S")
    for i in range(ladder_num):
        placement.append("L")
    for i in range(normal_num):
        placement.append("N")
    random.shuffle(placement)
    #generate movements for ladders and snakes
    movement = len(placement) * [0]
    if debug:
        print(placement)
    for i in range(len(placement)):
        if placement[i] == "S":
            movement[i] = random.randint(1, i + 1)
        elif placement[i] == "L":
            movement[i] = random.randint(1, len(placement) - i)
        else:
            movement[i] = 0
    #generating actual places
    game_board = Snake_Ladder("Start", None)
    places = []
    if debug:
        print(movement)
    for i in range(len(placement)):
        if placement[i] == "S":
            place = Snake_Ladder("S" + str(i + 1), str(movement[i]))
            places.append(place)
        elif placement[i] == "L":
            place = Snake_Ladder("L" + str(i + 1), str(movement[i]))
            places.append(place)
        else:
            place = Snake_Ladder("N" + str(i + 1), None)
            places.append(place)
    end = Snake_Ladder("Finish", None)
    #linking together in board
    prev = game_board
    counter = 0
    while counter <= len(placement) - 1:
        cur = places[counter]
        Connect(prev, cur)
        counter += 1
        prev = cur
    cur = end
    Connect(prev, cur)#connect end to the last place
    if debug:
        display_board()

def add_player():#add players to database
    global players
    name = validate_choice(validate_player_name, "Please enter the name of the new player: ", "Error, player name is repeating.")
    new_player = Player(name)
    players.append(new_player)

def start_game():#starting actual game
    global game_board
    global players
    #conditions to start
    if game_board == 0:
        print("There is no game board generated yet!")
        return None
    elif len(players) == 0:
        print("There are no players!")
        return None
    #set ups
    random.shuffle(players)
    for player in players:
        player.set_place(str(game_board))
    if debug:
        display_board()
    win = False
    player_list = players
    #actually turn based system starting
    while not win:
        for player in player_list:
            display_board()
            print(str(player) + "'s turn. 1: Roll dice 2: Skip turn 3: Quit")#options
            choice = int(validate_choice(validate_game_option, "Please choose a move: ", "Error, please choose a number between 1 and 3."))
            if choice == 1:#roll dice & move
                move = random.randint(1, 6)
                print(str(player) + " rolls a " + str(move) + ".")
                counter = move
                cur = get_place(player)
                while counter != 0 and cur != None:
                    cur = cur.get_next()
                    if str(cur) == "Finish":#if roll enough to win
                        win = True
                        print(str(player) + " wins!")
                        break
                    counter -= 1
                if win:
                    break
                else:
                    player.set_place(str(cur))#move to the space
                    if get_place(player).get_move_step() != None:#if it's ladder or snake move accordingly
                        if "S" in str(get_place(player)):#snake movement
                            counter = int(get_place(player).get_move_step())
                            cur = get_place(player)
                            while counter != 0:#useless code can remove, snake tile cant send you to finish
                                cur = cur.get_prev()
                                if str(cur) == "Finish":
                                    win = True
                                    print(str(player) + " wins!")
                                    break
                                counter -= 1
                            player.set_place(str(cur))
                        else:#ladder movement
                            counter = int(get_place(player).get_move_step())
                            cur = get_place(player)
                            while counter != 0:
                                cur = cur.get_next()
                                if str(cur) == "Finish":
                                    win = True
                                    print(str(player) + " wins!")
                                    break
                                counter -= 1
                            player.set_place(str(cur))
                if win:
                    break
            elif choice == 2:#skipping turn
                print(str(player) + " skipped a turn.")
                pass
            else:
                player_list.remove(player)#quit game
                print(str(player) + " left the game.")
                if len(player_list) == 0:#no players left
                    print("No players left in the game!")
                    win = True
                    break

#############################################################UI#########################################################

def display_main_menu():
    print("1) Create Game")
    print("2) Add a player")
    print("3) Start")
    print("4) Quit")

def menu():
    global game_board
    done = False
    while not done:
        display_main_menu()
        menu_choice = int(validate_choice(validate_menu, "Please choose an option: ", "Error, please choose a number between 1 to 4."))
        if menu_choice == 1:
            create_game()
        elif menu_choice == 2:
            add_player()
        elif menu_choice == 3:
            start_game()
        else:
            print("Ending game program....")
            done = True
menu()
