import random
import map
import player


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
m.create('data.json')
m.score()
print (m)


while (m.energyAvalible() == True):
    while (m.energyAvalible() == True):
        m.walk()
    print(m)
    m.thirtyMinutes()
print(m)
print (m.movements)
print('Energy Used %d' % (m.energyUsed))
for player in players:
    print('%s' % (player))
for i in m.nodeList:
    if (i.hit == 0):
        print ('Failure: %d' % i.number)
print('Success')
m.optimizeChamps()
