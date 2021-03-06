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
        return 'Node %d  \tPath Length %d\tImportance %d\tBranches %d\tPlayers %s \n' % (self.number, self.pathCounter, self.importance, self.branches, self.hit)

    def resetImportance(self):
        self.importance = 0
        self.pathCounter = 0


    alreadyCounted = []

    def calculatePathLength(self, map):
        global alreadyCounted
        self.pathCounter = 1
        if (len(self.futureNodes) > 0):
            self.branches = len(self.futureNodes)-1
        else:
            self.branches = 0
        for fnId in self.futureNodes:
            if (fnId in alreadyCounted):
                # print('Already found %d' % fnId)
                # self.branches -= 1
                a = 1
            else:
                fn = list(filter(lambda fn: fn.number == fnId, map.nodeList))[0]
                if (fn == None):
                    print('Bad Data', fnId)
                else:
                    alreadyCounted.append(fnId)
                    fn.calculatePathLength(map)
                    self.pathCounter += fn.pathCounter
                    self.branches += fn.branches
                    # print('Added %d to list %d' % (fnId, self.pathCounter))


    def calculateImportance(self, map):
        global alreadyCounted
        #importance = path length + linked nodes + hits/branches
        if (self.importance != 0):
            return
        elif( self.combatClass == 'GGobaBoss'):
            self.importance = 100
        else:
            self.branches = 0
            alreadyCounted = []
            # print('Calculating Path Length of %d' % self.number)
            self.calculatePathLength( map)
            # print(alreadyCounted);
            self.pathCounter = len(alreadyCounted)
            # print(self.pathCounter)


            self.importance = 20.0 * self.pathCounter / len(map.nodeList)
            # temp = 10.0 * self.pathCounter / len(map.nodeList)


            if (len(self.linkedTo) > 0):
                self.importance += 10
            if (self.hit < self.branches):
                self.importance = self.importance + (10.0*(self.branches - self.hit+1))
            if (self.boostedBy > 0):
                self.importance -= 10

            # self.importance += self.branches * 10

            for fnId in self.futureNodes:
                fn = list(filter(lambda fn: fn.number == fnId, map.nodeList))[0]
                if (fn == None):
                    print('Bad Data Check your map file: ', fnId)
                else:
                    fn.calculateImportance(map)
                    # self.importance += (fn.importance * 0.5)
            # print("Path Link is %d: %d %.2f %.2f" % (self.number, self.pathCounter, temp,  len(map.nodeList)))




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
