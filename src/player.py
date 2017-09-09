class Player(object):
    def __init__(self, number, champ1, champ2, champ3):
        self.number = number
        self.location = 0
        self.champs = [champ1, champ2, champ3]
        self.energy = 3
        self.path = [0]

    def __str__(self):
        return 'Player %d at Node %d with champs %s Energy: %d\n Path: %s\n' % (self.number, self.location, self.champs, self.energy, self.path)
