
class Player(object):
    def __init__(self):
        self.name = None
        self.results = dict()
        self.rolls = []
        self.scores = dict()

    #
    #   set pins scores for a frame.
    #
    def set_result(self, frame, result):
        self.results[frame] = result

    def calculate_score(self):
        running_total = 0
        for frame, result in self.results.items():
            frame_score = 0

            # this is brutal but works, needs to be simplified
            currentIndex = result['index']
            if result['strike'] or result['spare']:
                if len(self.rolls) - 1 >= currentIndex + 2:
                    frame_score = self.rolls[currentIndex] + self.rolls[currentIndex + 1] + self.rolls[currentIndex + 2]
            else:
                frame_score = self.rolls[currentIndex] + self.rolls[currentIndex + 1]
                if frame == 10 and len(self.rolls) - 1 >= currentIndex + 2:
                    frame_score = frame_score + self.rolls[currentIndex + 2]

            running_total = running_total + frame_score

            self.scores[frame] = {
                "frame_score": frame_score,
                "running_total": running_total
            }


