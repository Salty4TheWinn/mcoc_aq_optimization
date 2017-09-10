import player
import node

class Map(object):
    def __init__(self, players):
        self.nodeList = []
        self.players = players
        self.clock = 0
        self.openNodes = 0
        self.movements = 0
        self.energyUsed = 0


    def __str__(self):
        temp = 'Map 5 Time %d \n' % (self.clock)
        nodeIter = iter(self.nodeList)
        for i in nodeIter:
            temp += i.__str__()
        for j in self.players:
            temp += j.__str__()
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
            if (player.energy > 0 and player.location != 34):
                current = list(filter(lambda fn: fn.number == player.location, self.nodeList))[0]
                if (current.boostedBy == 0):
                    return True
        return False

    def thirtyMinutes(self):
        self.clock  = self.clock + 60
        for player in self.players:
            if (player.energy < 5):
                player.energy = player.energy + 1

    def walk(self):
        for player in self.players:
            if(player.energy > 0 and player.location != 34):
                current = list(filter(lambda fn: fn.number == player.location, self.nodeList))[0]

                if (current.boostedBy > 0):
                    print('Cannot Attack a bossted node %d' %(player.location))
                else:
                    current.fight(player)
                    mostImportant = -10000000
                    mostImportantIndex  = -1
                    for move in current.futureNodes:
                        moveNode = list(filter(lambda fn: fn.number == move, self.nodeList))[0]

                        if (moveNode.importance > mostImportant):
                            mostImportant = moveNode.importance
                            mostImportantIndex = move
                    if (mostImportant == -10000000):
                            print ('WTF No node selected')
                    else:
                        player.location = mostImportantIndex
                        moveNode = list(filter(lambda fn: fn.number == mostImportantIndex, self.nodeList))[0]

                        if (moveNode.hit == 0):
                            player.energy = player.energy - 1
                            self.energyUsed = self.energyUsed + 1
                            self.openNodes = self.openNodes - 1
                            print(moveNode.linkedTo)
                            for bnId in moveNode.linkedTo:
                                bn = list(filter(lambda fn: fn.number == bnId, self.nodeList))[0]
                                bn.boostedBy = bn.boostedBy - 1
                                print('Removing Boost on %d boost now set to %d\n' % (bnId, bn.boostedBy))
                            moveNode.linkedTo = []
                        self.movements = self.movements + 1
                        moveNode.hit = moveNode.hit + 1
                        self.score()
                        player.path.append(mostImportantIndex)
    ##                    print(self)
                        print(self.printPlayers())



    def create(self):
        self.nodeList.append(node.Node(0, 'Root', [100]))
        self.nodeList.append(node.Node(100, 'Empty', [1, 2, 101]))
        self.nodeList.append(node.Node(101, 'Empty', [6, 12, 7]))
        self.nodeList.append(node.Node(1, 'Cosmic', [102]))
        self.nodeList.append(node.Node(102, 'Empty', [5, 10]))

        self.nodeList.append(node.Node(2, 'Mystic', [110]))
        self.nodeList.append(node.Node(110, 'Empty', [111]))
        self.nodeList.append(node.Node(111, 'Empty', [19, 3]))

        self.nodeList.append(node.Node(3, 'Science', [4]))
        self.nodeList.append(node.Node(4, 'Mutant', [8], [], 1))
        self.nodeList.append(node.Node(5, 'Cosmic', [9], [10, 15]))
        self.nodeList.append(node.Node(6, 'Tech', [11], [], 1))
        self.nodeList.append(node.Node(7, 'Science', [13], [], 1))
        self.nodeList.append(node.Node(8, 'Mutant', [14], [], 1))
        self.nodeList.append(node.Node(9, 'Cosmic', [103]))
        self.nodeList.append(node.Node(103, 'Empty', [104]))
        self.nodeList.append(node.Node(104, 'Empty', [31]))

        self.nodeList.append(node.Node(10, 'Mystic', [15], [], 1))
        self.nodeList.append(node.Node(11, 'Tech', [16], [17]))
        self.nodeList.append(node.Node(12, 'Skill', [17], [6, 7]))
        self.nodeList.append(node.Node(13, 'Science', [18]))
        self.nodeList.append(node.Node(14, 'Mutant', [25], [24, 30]))
        self.nodeList.append(node.Node(15, 'Mystic', [32], [31, 33], 1))
        self.nodeList.append(node.Node(16, 'Tech', [21]))
        self.nodeList.append(node.Node(17, 'Skill', [22], [], 1))
        self.nodeList.append(node.Node(18, 'Science', [23]))
        self.nodeList.append(node.Node(19, 'Science', [20, 24]))
        self.nodeList.append(node.Node(20, 'Mystic', [8], [4, 8]))
        self.nodeList.append(node.Node(21, 'Tech', [26], [], 1))
        self.nodeList.append(node.Node(22, 'Skill', [27], [21, 23]))
        self.nodeList.append(node.Node(23, 'Science', [28], [], 1))
        self.nodeList.append(node.Node(24, 'Tech', [30], [35, 36],  1))
        self.nodeList.append(node.Node(25, 'Mutant', [36]))
        self.nodeList.append(node.Node(26, 'Mystic',[106], [34]))
        self.nodeList.append(node.Node(27, 'Science', [107], [34]))
        self.nodeList.append(node.Node(28, 'Cosmic',[109], [34]))
        self.nodeList.append(node.Node(29, 'Tech',[108], [34]))
        self.nodeList.append(node.Node(108, 'Empty', [109]))
        self.nodeList.append(node.Node(109, 'Empty', [107]))

        self.nodeList.append(node.Node(30, 'Mutant', [29], [], 1))
        self.nodeList.append(node.Node(31, 'Cosmic', [33], [32], 1))
        self.nodeList.append(node.Node(32, 'Mystic', [106], [34], 1))
        self.nodeList.append(node.Node(106, 'Empty', [107]))
        self.nodeList.append(node.Node(107, 'Empty', [34]))

        self.nodeList.append(node.Node(33, 'Cosmic', [105], [], 1))
        self.nodeList.append(node.Node(105, 'Empty', [37]))
        self.nodeList.append(node.Node(34, 'Boss', [], [], 7))
        self.nodeList.append(node.Node(35, 'Tech', [108], [34], 1))
        self.nodeList.append(node.Node(36, 'Mutant', [35], [], 1))
        self.nodeList.append(node.Node(37, 'Cosmic', [32], [34]))

        self.openNodes = len(self.nodeList)
    def optimizeChamps(self):
        for player in self.players:
            tech = 0
            cosmic = 0
            mystic = 0
            science = 0
            skill = 0
            mutant = 0
            for nodeId in player.path:
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
            print('Player %d needs Tech %d Cosmic %d Mystic %d Science %d Skill %d Mutant %d' % (player.number, tech, cosmic, mystic, science, skill, mutant))
