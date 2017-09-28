import random
import map
import player




def singleRun(pathPlan, verbose=False):
    players = []
    players.append(player.Player(1, 'Cosmic', 'Tech', 'Science'))
    players.append(player.Player(2, 'Cosmic', 'Tech', 'Mystic'))
    players.append(player.Player(3, 'Cosmic', 'Tech', 'Mystic'))
    players.append(player.Player(4, 'Cosmic', 'Tech', 'Mystic'))
    players.append(player.Player(5, 'Cosmic', 'Tech', 'Mystic'))
    players.append(player.Player(6, 'Cosmic', 'Tech', 'Mystic'))
    players.append(player.Player(7, 'Cosmic', 'Tech', 'Mystic'))
    players.append(player.Player(8, 'Cosmic', 'Tech', 'Mystic'))
    players.append(player.Player(9, 'Cosmic', 'Tech', 'Mystic'))
    players.append(player.Player(10, 'Cosmic', 'Tech', 'Mystic'))

    m = map.Map(players)
    m.pathChoice = pathPlan
    m.create('section1.json')
    m.loadPaths('paths.json')
    m.setPaths()
    m.score()

    while ( m.done == False and m.energyAvalible() == True):
        while (m.energyAvalible() == True):
             m.walk()
             if (verbose):
                 print(m)
        # print(m)
        if (m.done == False):
            m.thirtyMinutes()
    success = True
    for i in m.nodeList:
        if (i.hit == 0):
            # print ('Failure: %d' % i.number)
            success = False
        # if (i.number == m.bossNode and i.boostedBy == 0):
        #     print('Boss Dead')
    if (success):
        if (verbose):
            print('======================== Done ===================')
            print('Time %d' % m.clock)
            print('Energy Used %d' % (m.energyUsed))
            print('Path Plan %s'%(pathPlan))
        temp = {
        'time': m.clock,
        'energy': m.energyUsed,
        'pathPlan': pathPlan
        }
        return temp
    else:
        return None
    # m.optimizeChamps()

results = []
best = None
for i in range(0, 1000):
    pathPlan = []
    for j in range(0, 10):
        pathPlan.append(random.randint(0, 7))
    temp = singleRun(pathPlan)
    if (temp != None):
        results.append(temp)
        if (best == None or temp["time"] < best["time"]):
            best = temp
print(results)
print(best)

# singleRun(best["pathPlan"], True)
singleRun([7, 0, 7, 6, 3, 2, 1, 0, 4, 5], True)
