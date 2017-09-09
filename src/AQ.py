import random


class Node(object):
    def __init__(self, number, combatClass, futureNodes,  linkedTo = [],  boostedBy = 0):
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
        
    def __str__(self):
        return 'Node %d\tImportance %d\tBranches %d\tPlayers %s \n' % (self.number, self.importance, self.branches, self.hit)

    def resetImportance(self):
        self.importance = 0
        self.pathCounter = 0

    def calculateImportance(self, map):
        #importance = path length + linked nodes + hits/branches 
        if(self.number == 34):
            self.importance = 100
        else:
            if (self.hit == 0):
                self.pathCounter = 1
            else:
                self.pathCounter = 0
            self.branches = len(self.futureNodes)
            
            for fnId in self.futureNodes:
                fn = list(filter(lambda fn: fn.number == fnId, map.nodeList))[0]
                if (fn == None):
                    print('WTF: ', fnId)
                else:
                    fn.calculateImportance(map)
                    self.pathCounter = self.pathCounter + fn.pathCounter
                    if (fn.branches > 1):
                        self.branches = self.branches + (fn.branches-1)
                    self.linkedCounter = len(self.linkedTo) + (fn.linkedCounter)
            #path length
            if (self.pathCounter > 0):
                self.importance = (self.pathCounter / map.openNodes) * 33.0
            #branches
            self.importance = self.importance + 33 - ((self.hit/self.branches)*33)
            #linked nodes
            self.importance = self.importance + (self.linkedCounter * 33/5)
            if (self.boostedBy > 0):
                self.importance = self.importance -100
            if (len(self.linkedTo) > 0):
                self.importance = self.importance +100

    ##        print('Node %d Path Counter %d Importance %d' % (self.number, self.pathCounter, self.importance))

        
class Player(object):
    def __init__(self, number, champ1, champ2, champ3):
        self.number = number
        self.location = 0
        self.champs = [champ1, champ2, champ3]
        self.energy = 3
        self.path = [0]

    def __str__(self):
        return 'Player %d at Node %d with champs %s Energy: %d\n Path: %s\n' % (self.number, self.location, self.champs, self.energy, self.path)

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
                    mostImportant = -10000000
                    mostImportantIndex  = -1
                    for move in current.futureNodes:
                        moveNode = list(filter(lambda fn: fn.number == move, self.nodeList))[0]

    ##                    if (player.number == 9):
    ##                        print('Node: %d Importance %d\n' % (moveNode.number, moveNode.importance))
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
        self.nodeList.append(Node(0, 'Root', [100]))
        self.nodeList.append(Node(100, 'Empty', [1, 2, 101]))
        self.nodeList.append(Node(101, 'Empty', [6, 12, 7]))
        self.nodeList.append(Node(1, 'Cosmic', [102]))
        self.nodeList.append(Node(102, 'Empty', [5, 10]))
        
        self.nodeList.append(Node(2, 'Mystic', [110]))
        self.nodeList.append(Node(110, 'Empty', [111]))
        self.nodeList.append(Node(111, 'Empty', [19, 3]))

        self.nodeList.append(Node(3, 'Science', [4]))
        self.nodeList.append(Node(4, 'Mutant', [8], [], 1))
        self.nodeList.append(Node(5, 'Cosmic', [9], [10, 15]))
        self.nodeList.append(Node(6, 'Tech', [11], [], 1))
        self.nodeList.append(Node(7, 'Science', [13], [], 1))
        self.nodeList.append(Node(8, 'Mutant', [14], [], 1))
        self.nodeList.append(Node(9, 'Cosmic', [103]))
        self.nodeList.append(Node(103, 'Empty', [104]))
        self.nodeList.append(Node(104, 'Empty', [31]))

        self.nodeList.append(Node(10, 'Mystic', [15], [], 1))
        self.nodeList.append(Node(11, 'Tech', [16], [17]))
        self.nodeList.append(Node(12, 'Skill', [17], [6, 7]))
        self.nodeList.append(Node(13, 'Science', [18]))
        self.nodeList.append(Node(14, 'Mutant', [25], [24, 30]))
        self.nodeList.append(Node(15, 'Mystic', [32], [31, 33], 1))
        self.nodeList.append(Node(16, 'Tech', [21]))
        self.nodeList.append(Node(17, 'Skill', [22], [], 1))
        self.nodeList.append(Node(18, 'Science', [23]))
        self.nodeList.append(Node(19, 'Science', [20, 24]))
        self.nodeList.append(Node(20, 'Mystic', [8], [4, 8]))
        self.nodeList.append(Node(21, 'Tech', [26], [], 1))
        self.nodeList.append(Node(22, 'Skill', [27], [21, 23]))
        self.nodeList.append(Node(23, 'Science', [28], [], 1))
        self.nodeList.append(Node(24, 'Tech', [30], [35, 36],  1))
        self.nodeList.append(Node(25, 'Mutant', [36]))
        self.nodeList.append(Node(26, 'Mystic',[106], [34]))
        self.nodeList.append(Node(27, 'Science', [107], [34]))
        self.nodeList.append(Node(28, 'Cosmic',[109], [34]))
        self.nodeList.append(Node(29, 'Tech',[108], [34]))
        self.nodeList.append(Node(108, 'Empty', [109]))
        self.nodeList.append(Node(109, 'Empty', [107]))

        self.nodeList.append(Node(30, 'Mutant', [29], [], 1))
        self.nodeList.append(Node(31, 'Cosmic', [33], [32], 1))
        self.nodeList.append(Node(32, 'Mystic', [106], [34], 1))
        self.nodeList.append(Node(106, 'Empty', [107]))
        self.nodeList.append(Node(107, 'Empty', [34]))

        self.nodeList.append(Node(33, 'Cosmic', [105], [], 1))
        self.nodeList.append(Node(105, 'Empty', [37]))
        self.nodeList.append(Node(34, 'Boss', [], [], 7))
        self.nodeList.append(Node(35, 'Tech', [108], [34], 1))
        self.nodeList.append(Node(36, 'Mutant', [35], [], 1))
        self.nodeList.append(Node(37, 'Cosmic', [32], [34]))

        self.openNodes = len(self.nodeList)


        
players = []
for i in range(1,11):
    players.append(Player(i, 'Cosmic', 'Tech', 'Mystic'))

m = Map(players)
m.create()
m.score()
print (m)


while (m.energyAvalible() == True):
    while (m.energyAvalible() == True):
        m.walk()
    print(m)
    m.thirtyMinutes()

print (m.movements)
print('Energy Used %d' % (m.energyUsed))
for i in m.nodeList:
    if (i.hit == 0):
        print ('Failure')
print('Success')

