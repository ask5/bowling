from player import Player
from rules_lib import *
import re
from pprint import pprint


class Bowling(object):

    def __init__(self):
        print()
        print("Bowling Score Calculator")
        print()

        self.frames = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.players = []

    #
    # Setup collects players information
    #
    def setup(self):
        print("SETUP")
        # get number of players from user
        while True:
            try:
                num_players = int(input("Number of players: "))
            except ValueError:
                print("invalid entry")
                continue
            else:
                break

        # input names for each player
        for i in range(0, num_players):
            name = input("Player {} name: ".format(str(i + 1)))
            p = Player()
            p.name = name
            self.players.append(p)

        print("SETUP COMPLETE")
        print()
        print("Program will prompt user to enter every player's pin scores for all 10 frames. Valid inputs: 0 to 10, X, /")
        print("Scores will be displayed at the end of each frame.")
        print()
        input("Press ENTER to begin...")
        print()

    #
    # Main method that runs the game
    #
    def play(self):
        for frame in self.frames:
            print()
            print("Frame {}".format(str(frame)))
            print("---------------------------------------------------------")
            for player in self.players:

                result = dict()
                result['strike'] = False
                result['spare'] = False

                # get the first roll
                result['roll_1'] = self.get_fresh_pins("{}'s turn #1: ".format(player.name))

                # if it is not the 10th frame then player gets 2 chances, depending upon if the first roll is strike or not
                if frame < 10:
                    if strike(result['roll_1']):
                        result['strike'] = True
                        result['roll_2'] = ''
                    else:
                        remainder = 10 if frame == 10 else 10 - int(result['roll_1'])
                        result['roll_2'] = self.get_spare_pins("{}'s turn #2: ".format(player.name), remainder)
                        if spare(result['roll_1'], result['roll_2']):
                            result['spare'] = True
                    result['roll_3'] = ''
                else:
                    # for 10th frame, if roll 1 is strike then get fresh pins else get spare pins
                    if strike(result['roll_1']):
                        result['strike'] = True
                        result['roll_2'] = self.get_fresh_pins("{}'s turn #1: ".format(player.name))
                    else:
                        remainder = 10 if frame == 10 else 10 - int(result['roll_1'])
                        result['roll_2'] = self.get_spare_pins("{}'s turn #2: ".format(player.name), remainder)

                    # if its 10th frame, then you'll need the thrid roll if you play strike on the first roll
                    # or spare on the first 2 rolls
                    if strike(result['roll_1']) or result['roll_2'] == "/":
                        result['roll_3'] = self.get_fresh_pins("{}'s turn #3: ".format(player.name))
                    else:
                        result['roll_3'] = ''

                player.set_result(frame=frame, result=result)

                player.calculate_score()

            self.print_scoreboard()

    def reset(self):
        for player in self.players:
            player.results.clear()
            player.scores.clear()

    #
    #  Helper methods
    #

    def get_fresh_pins(self, msg):
        pins = 'undefined'
        while not pins or not re.match("^([Xx0-9]|10)$", pins):
            if pins != 'undefined':
                print("Error! Valid inputs: 0 to 10, X, x")
            pins = input(msg)
        else:
            return pins

    def get_spare_pins(self, msg, remainder=10):
        pins = 'undefined'
        regex = "^([\/0-9]|10)$" if remainder == 10 else "^([\/0-"+ str(remainder) +"])$"
        while not pins or not re.match(regex, pins):
            if pins != 'undefined':
                print("Error! Valid inputs: 0 to {}, /".format(str(remainder)))
            pins = input(msg)
        else:
            return pins

    def print_scoreboard(self):
        print()
        print("Scoreboard")

        # print heading
        print("----------------------------------------------------------------------------")
        heading = self.fixed_width("Frames") + "|"
        for frame in self.frames:
            heading = heading + self.fixed_width(str(frame), 5) + "|"
        print(heading)
        print("----------------------------------------------------------------------------")

        # print results
        for player in self.players:
            results = ''
            for frame, res in player.results.items():
                results = results + self.fixed_width(res['roll_1'] + " " + res['roll_2'] + " " + res['roll_3'], 5) + "|"

            print(self.fixed_width(player.name) + "|" + results)

            scores = ''
            for frame, s in player.scores.items():
                scores = scores + self.fixed_width(str(s['frame_score']), 5) + "|"

            print(self.fixed_width("Frame Scores") + "|" + scores)

            totals = ''
            for frame, s in player.scores.items():
                totals = totals + self.fixed_width(str(s['running_total']), 5) + "|"

            print(self.fixed_width("Running Total") + "|" + totals)
            print("----------------------------------------------------------------------------")

        print()
    #
    # helper function for printing scoreboard
    #
    def fixed_width(self, text, length=15):
        if len(text) >= length:
            return text[:length]
        else:
            return text + ' ' * (length - len(text))