'''
- - - What would I want the Island to look like
- - - Set up a bare bones location-with an entry exit point


'''
from game import location
import game.config as config
import game.display as display
import time
import random
from datetime import datetime

###########################################
               # Classes
###########################################
class Island (location.Location):

    def __init__ (self, x, y, w):
        super().__init__(x, y, w)
        self.name = "island"
        self.symbol = 'I'
        self.visitable = True
        self.locations = {}
        self.locations["beach"] = BeachWithShip(self)
        self.locations["sub"] = Subarea(self)

        self.starting_location = self.locations["beach"]

    def enter (self, ship):
        display.announce ("arrived at an island", pause=False)

class BeachWithShip (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "southBeach"
        self.verbs['south'] = self


    def enter (self):
        display.announce ("You arrive at the beach of a seemingly peaceful island.\n" +
                  "Your ship is at anchor in a small bay to the south.\n" +
                  "The calm blow of the wind rustles the ancient-looking tress adorned with vibrant foliage.\n" +
                  "Up ahead, you can see a a shrine sitting atop a hill.")

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"):
            display.announce ("You return to your ship.")
            self.main_location.end_visit()
        if (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["sub"]

class coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __add__(self, other):
        return coordinate(self.x + other.x, self.y + other.y)



class Subarea (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "southBeach"
        self.verbs['south'] = self
        self.played_times = 0


    def enter (self):
        display.announce ("In Subarea")
        self.reactiongame()

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"):
            display.announce ("You return to your ship.")
            self.main_location.end_visit()

    def reactiongame(self):
        self.played_times += 1
        if self.played_times <= 3:
            command_list = ['w', 'a', 's', 'd']
            x_times = 0
            points = 0
            display.announce('Dodge 8 out of 10 incoming spike balls by pressing coressponding keys in time')
            time.sleep(1)
            while x_times < 10:
                rand_spot = random.randint(0, 3)
                #   Seconds part
                startime = time.time()
                reaction = display.get_text_input(f'Press {command_list[rand_spot]} ')
                #   Seconds part
                endtime = time.time()
                delta = endtime - startime
                if (reaction == command_list[rand_spot]) and delta <= 1.5:
                    points += 1
                else:
                    display.announce('You got hit')
                    piratelist = config.the_player.get_pirates()
                    random.shuffle(piratelist)
                    num = random.randint(1,len(piratelist) + 1)
                    targets = (piratelist[:num])
                    for hit in targets:
                        display.announce(f'{hit.get_name()} got hit for 15 Hp')
                        deader = hit.inflict_damage(15, 'smashed by a spike ball')
                        #If a pirate is killed by the damage, inflict_damge returns them.
                        # Otherwise, it returns None
                        if not (deader is None):
                            display.announce(f"{deader.get_name()} is killed!")
                            config.the_player.cleanup_pirates() #Makes sure the game ends if all pirates are dead
                        
                x_times += 1
            if points >= 8:
                pass
                #Give Speed and Accuracy points for completion 
        else:
            display.announce(f'You have maximized the limit of which you can enter the sub-area')
                             

            #Define getting hit. Should maybe take some health down?(Completed?) 
            #Figure out a prize for winning 
            #Island Theme?  
            #if returned the 4th time, subarea doesn't work(Completed?)
    def matchingpuzzle(self):
        set_board = [
            [" ", " ", " ", " "],
            [" ", " ", " ", " "],
            [" ", " ", " ", " "],
            [" ", " ", " ", " "]
        ]
        playerXO = random.choice([1, 2])
        
        x = random.choice(range(4))
        y = random.choice(range(4))
        set_board[y][x] = 'X'
        X_Coord = coordinate(x,y)
        while set_board[y][x] != " " or ((X_Coord.y == y) and (abs(x - X_Coord.x) == 1)): #note:guaranteed the first trip through the loop
            x = random.choice(range(4))
            y = random.choice(range(4))
        #once we're past the loop, x,y is a good spot
        set_board[y][x] = 'O'
        O_Coord = coordinate(x,y)
        #Get input
        # w a s d
        input_meanings = {}
        input_meanings['w'] = coordinate(0,-1)
        input_meanings['s'] = coordinate(0,1)
        input_meanings['a'] = coordinate(-1,0)
        input_meanings['d'] = coordinate(1,0)
        line = ["─"]*len(set_board)
        print("┌"+"┬".join(line)+"┐")
        line = "├"+"┼".join(line)+"┤"
        for row in set_board:
            print("│"+"│".join(row)+"│")
            print(line)
        #etc

        #Make either X or O move
        if playerXO == 1:
            playerXO = 'X'
            player = X_Coord
            alt = O_Coord
            altXO = 'O'
        else:
            playerXO = 'O'
            player = O_Coord
            alt = X_Coord
            altXO = 'X'
        display.announce(f"Control the '{playerXO}' using 'w a s d' to line up with the '{altXO}' side by side.")
        
        while not ((player.y == alt.y) and (abs(player.x - alt.x == 1))):
            user_input = input()
            if user_input in input_meanings:
                move = input_meanings[user_input]
                set_board[player.y][player.x] = " "       #player.x & player.y? for both X and O 
                player = player + move
                set_board[player.y][player.x] = playerXO
                line = ["─"]*len(set_board)
                print("┌"+"┬".join(line)+"┐")
                line = "├"+"┼".join(line)+"┤"
                for row in set_board:
                    print("│"+"│".join(row)+"│")
                    print(line)
            else:
                display.announce("Use 'w a s d' to move.")

        #if (X_Coord.y == O_Coord.y) and (abs(X_Coord.x - O_Coord.x == 1)):
#Reward with Treasure or Stat upgrade


#############################################
