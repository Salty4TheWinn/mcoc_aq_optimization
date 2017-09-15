import player

class Node(object):
    def __init__(self, number, combatClass, futureNodes,  linkedTo = [],  boostedBy = 0, inputs = 1):
        self.number = number
        self.combatClass = combatClass
        self.hit = 0
        if (number == 0):
            self.hit = 10
        self.futureNodes = futureNodes
        self.linkedTo = linkedTo
        self.boostedBy = boostedBy
        self.importance = 0
        self.difficulty = 0
        self.pathCounter = 0
        self.branches = 0
        self.linkedCounter = 0
        self.inputs = inputs
        self.totalFuturePaths = []

    def __str__(self):
        return 'Node %d  \tImportance %d\tBranches %d\tPlayers %s \n' % (self.number, self.importance, self.branches, self.hit)

    def resetImportance(self):
        self.importance = 0
        self.pathCounter = 0

    def calculateImportance(self, map):
        #importance = path length + linked nodes + hits/branches
        if (self.importance != 0):
            return
        elif( self.combatClass == 'GGobaBoss'):
            self.importance = 100
        else:

            if (self.hit == 0):
                self.pathCounter = 1/self.inputs
            else:
                self.pathCounter = 0

            self.branches = len(self.futureNodes)
            self.branches = self.branches - self.inputs + 1
            print('branches %d %d' % (self.number, self.branches))
            # if (self.branches == 0):
            #     self.branches = 1



            for fnId in self.futureNodes:
                fn = list(filter(lambda fn: fn.number == fnId, map.nodeList))[0]
                if (fn == None):
                    print('WTF: ', fnId)
                else:
                    fn.calculateImportance(map)
                    self.pathCounter = self.pathCounter + (fn.pathCounter)
                    if (fn.branches > 1):
                        self.branches = self.branches + ( (fn.branches-1))
                    if (fn.inputs > 1):
                        self.branches -= fn.inputs - 1
                    self.linkedCounter = len(self.linkedTo) + (fn.linkedCounter)
            #path length
            print('Inital %d: %d' % (self.pathCounter, map.openNodes))
            if (self.pathCounter > 0):
                self.importance = (self.pathCounter / map.openNodes) * 33.0
            #branches
            # self.importance = self.importance + 25 - ((self.hit/self.branches)*25)
            #linked nodes
            print('Path Counter %d: %d %d %d' % (self.number, self.importance, self.pathCounter, map.openNodes))
            # self.importance = self.importance + (self.linkedCounter * 25/5)
            # print('Linked Counter %d: %d' % (self.number, self.importance))
            if (self.hit < self.branches):
                self.importance = self.importance + 33 - ((self.hit/self.branches)*33)
            print('Hit vs Brances %d: %d' % (self.number, self.importance))
            if (self.boostedBy > 0):
                self.importance = self.importance -33
            print('Boosted %d: %d' % (self.number, self.importance))
            if (len(self.linkedTo) > 0):
                self.importance = self.importance +33
            print('Linked %d: %d' % (self.number, self.importance))
            if( self.combatClass == 'Root' ):
                self.importance = 0
            print('Node %d Path Counter %d Importance %d Branches %d' % (self.number, self.pathCounter, self.importance, self.branches))
    def actualFight(self, weakClass, strongClass, player):
        if (strongClass in player.champs):
            player.win = player.win + 1
        elif (weakClass not in player.champs):
            player.lose = player.lose + 1
        else:
            player.draw = player.draw + 1
    def fight(self, player):
        if (self.combatClass == 'Empty' or self.combatClass == 'Root'):
            return
        elif (self.combatClass == 'Cosmic'):
            self.actualFight('Tech', 'Mystic', player)
        elif (self.combatClass == 'Tech'):
            self.actualFight('Mutant', 'Cosmic', player)
        elif (self.combatClass == 'Mutant'):
            self.actualFight('Skill', 'Tech', player)
        elif (self.combatClass == 'Skill'):
            self.actualFight('Science', 'Mutant', player)
        elif (self.combatClass == 'Science'):
            self.actualFight('Mystic', 'Skill', player)
        elif (self.combatClass == 'Mystic'):
            self.actualFight('Cosmic', 'Science', player)
