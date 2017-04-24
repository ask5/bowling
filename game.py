#
# Main entry point of the program
#
from bowling import Bowling

bowling = Bowling()

# setup players
bowling.setup()

# start the game
play = "y"
while play.lower() == "y":
    bowling.play()
    play = input("Game Over! Replay? [y/n]")
    bowling.reset()
