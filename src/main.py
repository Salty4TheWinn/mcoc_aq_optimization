import random
import map
import player


players = []
for i in range(1,11):
    players.append(player.Player(i, 'Cosmic', 'Tech', 'Mystic'))

m = map.Map(players)
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
