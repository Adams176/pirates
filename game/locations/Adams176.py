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




class Subarea (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "southBeach"
        self.verbs['south'] = self


    def enter (self):
        display.announce ("In Subarea")
        self.reactiongame()

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"):
            display.announce ("You return to your ship.")
            self.main_location.end_visit()

    def reactiongame(self):
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

            #Define getting hit. Should maybe take some health down? 
            #Figure out a prize for winning 
            #Island Theme?
            #if returned the 4th time, subarea doesn't work
    def matchingpuzzle(self):
        pass
        '''
        set_board = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
        player = random_randint(1, 2)
        spot = random_randint(1, 9)
        if spot == range(1, 3):
            if player == 1:
                set_board[spot - 1][spot - 1] = X
            if player == 2:
                set_board[spot - 1][spot - 1] = O


#############################################
'''