class Player(object):
    def __init__(self, number, champ1, champ2, champ3):
        self.number = number
        self.location = 0
        self.champs = [champ1, champ2, champ3]
        self.energy = 3
        self.pathList = None
        self.win = 0
        self.lose = 0
        self.draw = 0
        self.stuck = False
        self.actualFights = []

    def __str__(self):
        return 'Player %d at Node %d with champs %s Energy: %d Stuck: %s\n Path: %s\n' % (self.number, self.pathList[self.location], self.champs, self.energy, self.stuck, self.pathList)
