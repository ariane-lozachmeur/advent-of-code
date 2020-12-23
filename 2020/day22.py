from copy import deepcopy
import json

def distribute_cards(lines):
    current_player = 1
    players = {}
    for l in lines:
        if l == '\n':
            pass
        elif l.startswith('Player'):
            current_player = l.replace('Player ','')[0]
            players[current_player] = []
        else:
            card = int(l.strip('\n'))
            players[current_player].append(card)
    return players

def play_round_q1(players):
    c1 = players['1'].pop(0)
    c2 = players['2'].pop(0)
    if c1 > c2:
        players['1'].append(c1)
        players['1'].append(c2)
    elif c2 > c1:
        players['2'].append(c2)
        players['2'].append(c1)
    return players

def seen_this_before(players, prev_configs):
    for config in prev_configs:
        if players['1'] == config['1'] and players['2'] == config['2']:
            return True
    return False

def play_game_q2(players):
    print('Starting game with ')
    print(players)
    prev_configs = []
    seen_this = False
    n = 0
    while len(players['1'])>0 and len(players['2'])>0 and not seen_this:
        n += 1
        c = {}
        c['1'] = players['1'].pop(0)
        c['2'] = players['2'].pop(0)
        if len(players['1']) >= c['1'] and len(players['2']) >= c['2']:
            print('Starting new game')
            winner = play_game_q2({'1':players['1'][:c['1']], '2':players['2'][:c['2']]})

        elif c['2'] > c['1']:
            winner = '2'
        elif c['1'] > c['2']:
            winner = '1'

        players[winner].append(c[winner])
        players[winner].append(c['2' if winner=='1' else '1'])
        seen_this = seen_this_before(players, prev_configs)
        prev_configs.append(deepcopy(players))
    
    if len(players['1'])==0:
        print('Player 2 wins with score {}'.format(caluculate_score(players['2'])))
        return '2'
    elif len(players['2'])==0:
        print('Player 1 wins with score {}'.format(caluculate_score(players['1'])))
        return '1'
    elif seen_this:
        print('Infinite game')
        print('Player 1 wins with score {}'.format(caluculate_score(players['1'])))
        return '1'


def caluculate_score(player):
    score = 0
    for i in range(len(player)):
        score += (i+1) * player[-(i+1)]
    return score

if __name__=="__main__":
    with open('inputs/day22.txt', 'r') as handle:
        lines = handle.readlines()
        
    players = distribute_cards(lines)
    # players = {'1':[43, 19], '2':[2, 29, 14]}

    play_game_q2(players)



