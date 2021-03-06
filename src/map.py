import player
import node
import json
from pprint import pprint



class Map(object):
    def __init__(self, players):
        self.nodeList = []
        self.players = players
        self.clock = 0
        self.openNodes = 0
        self.movements = 0
        self.energyUsed = 0
        self.bossNode = 0
        self.nextPath = 1
        self.pathList  = []
        self.stuckPlayers = []
        self.pathChoice = [0, 1, 2, 3, 4, 5, 6, 7, 0, 1]
        # self.pathChoice = [1, 0, 5, 7, 3, 2, 4, 6, 0, 6]
        # self.pathChoice = [5, 4, 3, 2, 1, 6, 7, 0, 4, 4]
        self.done = False


    def __str__(self):
        temp = 'Map 5 Time %d \n' % (self.clock)
        nodeIter = iter(self.nodeList)
        # for i in nodeIter:
        #     temp += i.__str__()
        for j in self.players:
            temp += j.__str__()
        # for k in self.pathList:
        #     temp += 'Paths: %s\n' % (k)
        return temp

    def printPlayers(self):
        temp = ""
        for j in self.players:
            temp += j.__str__()
        return temp

    def score(self):
        for node in self.nodeList:
            node.resetImportance()
        rootNode = self.nodeList[0]
        rootNode.calculateImportance(self)

    def energyAvalible(self):
        for player in self.players:
            if (player.energy > 0 and player.location < len(player.pathList)-1 and player.stuck == False):
                current = list(filter(lambda fn: fn.number == player.location, self.nodeList))[0]
                if (current.boostedBy == 0):
                    return True
        return False

    def thirtyMinutes(self):
        self.clock  = self.clock + 60
        for player in self.players:
            if (player.energy < 5):
                player.energy = player.energy + 1


    def setPaths(self):
        for player in self.players:
            if (player.pathList == None):
                player.pathList = self.pathList[self.pathChoice[self.nextPath-1]]
                self.nextPath += 1
                if (self.nextPath > len(self.pathChoice)):
                    self.nextPath = 1

    def checkDone(self):
        self.done = True
        for player in self.players:
            if (player.pathList[player.location] != self.bossNode):
                self.done = False


    def walk(self):
        for player in self.players:
            while(player.energy > 0 and player.location < len(player.pathList)-1 and player.stuck != True):
                current = list(filter(lambda fn: fn.number == player.pathList[player.location], self.nodeList))[0]
                if (current.boostedBy > 0):
                    # print('Cannot Attack a boosted node %s' %(current))
                    player.stuck = True
                    self.stuckPlayers.append(player)
                else:
                    # print('Player %d Moving to Node %d\n' % (player.number, player.pathList[player.location+1]))
                    player.location += 1
                    moveNode = list(filter(lambda fn: fn.number == player.pathList[player.location], self.nodeList))[0]
                    if (moveNode.hit == 0):
                        player.energy = player.energy - 1
                        self.energyUsed = self.energyUsed + 1
                        self.openNodes = self.openNodes - 1
                        player.actualFights.append(moveNode.number)
                        # print(moveNode.linkedTo)
                        for bnId in moveNode.linkedTo:
                            bn = list(filter(lambda fn: fn.number == bnId, self.nodeList))[0]
                            bn.boostedBy = bn.boostedBy - 1
                            temp = []
                            for stuckPlayer in self.stuckPlayers:
                                if (stuckPlayer.pathList[stuckPlayer.location] == bnId):
                                    # print('Found Stuck Player %d at %d' % (stuckPlayer.number, stuckPlayer.pathList[stuckPlayer.location]))
                                    stuckPlayer.stuck = False
                                else:
                                    temp.append(stuckPlayer)
                            self.stuckPlayers = temp
                            # print('Removing Boost on %d boost now set to %d\n' % (bnId, bn.boostedBy))
                        moveNode.linkedTo = []
                    self.movements = self.movements + 1
                    moveNode.hit = moveNode.hit + 1
        self.checkDone()


    # def walk(self):
    #     for player in self.players:
    #         while(player.energy > 0 and player.location != self.bossNode):
    #             current = list(filter(lambda fn: fn.number == player.location, self.nodeList))[0]
    #
    #             if (current.boostedBy > 0):
    #                 print('Cannot Attack a bossted node %d' %(player.location))
    #             elif (len(current.futureNodes) == 1):
    #                 mostImportantIndex = current.futureNodes[0]
    #                 player.location = mostImportantIndex
    #                 moveNode = list(filter(lambda fn: fn.number == mostImportantIndex, self.nodeList))[0]
    #
    #                 if (moveNode.hit == 0):
    #                     player.energy = player.energy - 1
    #                     self.energyUsed = self.energyUsed + 1
    #                     self.openNodes = self.openNodes - 1
    #                     # print(moveNode.linkedTo)
    #                     for bnId in moveNode.linkedTo:
    #                         bn = list(filter(lambda fn: fn.number == bnId, self.nodeList))[0]
    #                         bn.boostedBy = bn.boostedBy - 1
    #                         # print('Removing Boost on %d boost now set to %d\n' % (bnId, bn.boostedBy))
    #                     moveNode.linkedTo = []
    #                 self.movements = self.movements + 1
    #                 moveNode.hit = moveNode.hit + 1
    #                 self.score()
    #                 player.path.append(mostImportantIndex)
    #             else:
    #                 current.fight(player)
    #                 mostImportant = -10000000
    #                 mostImportantIndex  = -1
    #                 for move in current.futureNodes:
    #                     moveNode = list(filter(lambda fn: fn.number == move, self.nodeList))[0]
    #
    #                     if (moveNode.importance > mostImportant):
    #                         mostImportant = moveNode.importance
    #                         mostImportantIndex = move
    #                 if (mostImportantIndex >= 0):
    #                     player.location = mostImportantIndex
    #                     moveNode = list(filter(lambda fn: fn.number == mostImportantIndex, self.nodeList))[0]
    #
    #                     if (moveNode.hit == 0):
    #                         player.energy = player.energy - 1
    #                         self.energyUsed = self.energyUsed + 1
    #                         self.openNodes = self.openNodes - 1
    #                         # print(moveNode.linkedTo)
    #                         for bnId in moveNode.linkedTo:
    #                             bn = list(filter(lambda fn: fn.number == bnId, self.nodeList))[0]
    #                             bn.boostedBy = bn.boostedBy - 1
    #                             # print('Removing Boost on %d boost now set to %d\n' % (bnId, bn.boostedBy))
    #                         moveNode.linkedTo = []
    #                     self.movements = self.movements + 1
    #                     moveNode.hit = moveNode.hit + 1
    #                     self.score()
    #                     player.path.append(mostImportantIndex)
    # ##                    print(self)
    #                     # print(self.printPlayers())



    def create(self, file):
        remove = 0
        with open(file) as data_file:
            data = json.load(data_file)
            for datum in data:
                self.nodeList.append(node.Node(datum['number'], datum['combatClass'], datum['futureNodes'], datum['linkedTo'], datum['boostedBy'], datum['inputs']))
                if (datum['combatClass'] == 'Boss'):
                    self.bossNode = datum['number']
                    remove += 1
                elif (datum['combatClass'] == 'Root'):
                    remove += 1
        self.openNodes = len(self.nodeList) - 1 # remove root and boss


    def loadPaths(self, file):
        with open(file) as data_file:
            data = json.load(data_file)
            for datum in data:
                self.pathList.append(datum['nodes'])


    def optimizeChamps(self):
        for player in self.players:
            tech = 0
            cosmic = 0
            mystic = 0
            science = 0
            skill = 0
            mutant = 0
            for nodeId in player.actualFights:
                current = list(filter(lambda fn: fn.number == nodeId, self.nodeList))[0]
                if (current.combatClass == 'Mutant'):
                    tech += 1
                elif (current.combatClass == 'Tech'):
                    cosmic += 1
                elif (current.combatClass == 'Cosmic'):
                    mystic += 1
                elif (current.combatClass == 'Mystic'):
                    science += 1
                elif (current.combatClass == 'Science'):
                    skill += 1
                elif (current.combatClass == 'Skill'):
                    mutant += 1
            first  = -1
            firstName = ''
            second = -1
            secondName = ''
            third = -1
            thirdName = ''
            if (tech > first):
                firstName = 'Tech'
                first = tech
            if (cosmic > first):
                firstName = 'Cosmic'
                first = cosmic
            if (mystic > first):
                firstName = 'Mystic'
                first = mystic
            if (science > first):
                firstName = 'Science'
                first = science
            if (skill > first):
                firstName = 'Skill'
                first = skill
            if (mutant > first):
                firstName = 'Mutant'
                first = mutant

            if (tech > second and firstName != 'Tech'):
                secondName = 'Tech'
                second = tech
            if (cosmic > second and firstName != 'Cosmic' ):
                secondName = 'Cosmic'
                second = cosmic
            if (mystic > second and firstName != 'Mystic'):
                secondName = 'Mystic'
                second = mystic
            if (science > second and firstName != 'Science'):
                secondName = 'Science'
                second = science
            if (skill > second and firstName != 'Skill'):
                secondName = 'Skill'
                second = skill
            if (mutant > second and firstName != 'Mutant'):
                secondName = 'Mutant'
                second = mutant

            if (tech > third and firstName != 'Tech' and secondName != 'Tech'):
                thirdName = 'Tech'
                third = tech
            if (cosmic > third and firstName != 'Cosmic' and secondName != 'Cosmic' ):
                thirdName = 'Cosmic'
                third = cosmic
            if (mystic > third and firstName != 'Mystic' and secondName != 'Mystic'):
                thirdName = 'Mystic'
                third = mystic
            if (science > third and firstName != 'Science' and secondName != 'Science'):
                thirdName = 'Science'
                third = science
            if (skill > third and firstName != 'Skill' and secondName != 'Skill' ):
                thirdName = 'Skill'
                third = skill
            if (mutant > third and firstName != 'Mutant' and secondName != 'Mutant'):
                thirdName = 'Mutant'
                third = mutant

            if (second < 1):
                secondName = 'Anything'
            if (third < 1):
                thirdName = 'Anything'

            print('Player %d needs %s, %s, %s' % (player.number, firstName, secondName, thirdName))
