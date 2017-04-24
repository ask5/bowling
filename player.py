
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

            if frame < 10:
                if result['strike']:
                    frame_score = frame_score + 10
                    if frame + 1 in self.results:
                        if frame + 1 < 10:
                            if self.results[frame + 1]['strike']:
                                frame_score = frame_score + 10
                                if frame + 2 in self.results:
                                    if self.results[frame + 2]['strike']:
                                        frame_score = frame_score + 10
                                    else:
                                        frame_score = frame_score + int(self.results[frame + 2]['roll_1'])
                            elif self.results[frame + 1]['spare']:
                                frame_score = frame_score + 10
                            else:
                                frame_score = frame_score + int(self.results[frame + 1]['roll_1']) \
                                              + int(self.results[frame + 1]['roll_2'])
                        else:
                            roll_1 = 10 if self.results[frame + 1]['roll_1'].lower() == 'x' else int(self.results[frame + 1]['roll_1'])
                            if self.results[frame + 1]['roll_2'].lower() == 'x':
                                roll_2 = 10
                            elif self.results[frame + 1]['roll_2'] == "/":
                                roll_2 = 10 - int(self.results[frame + 1]['roll_1'])
                            else:
                                roll_2 = int(self.results[frame + 1]['roll_2'])

                            frame_score = frame_score + roll_1 + roll_2

                elif result['spare']:
                    if frame + 1 in self.results:
                        if self.results[frame + 1]['strike']:
                            frame_score = 20
                        else:
                            frame_score = 10 + int(self.results[frame + 1]['roll_1'])
                else:
                    frame_score = frame_score + int(result['roll_1']) + int(result['roll_2'])
            else:
                roll_1 = 10 if result['roll_1'].lower() == 'x' else int(result['roll_1'])
                if result['roll_2'].lower() == 'x':
                    roll_2 = 10
                elif result['roll_2'] == "/":
                    roll_2 = 10 - int(result['roll_1'])
                else:
                    roll_2 = int(result['roll_2'])

                try:
                    roll_3 = 10 if result['roll_3'].lower() == 'x' else int(result['roll_3'])
                except:
                    roll_3 = 0

                frame_score = roll_1 + roll_2 + roll_3

            running_total = running_total + frame_score

            self.scores[frame] = {
                "frame_score": frame_score,
                "running_total": running_total
            }


