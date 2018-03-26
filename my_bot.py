# BVH

import json
import sys

def main():
    for line in sys.stdin:
        state = json.loads(line)
        planets = [p for p in state['planets']]
        my_planets = [p for p in state['planets'] if p['owner'] == 1]
        other_planets = [p for p in state['planets'] if p['owner'] != 1]
        expeds = [e for e in state['expeditions']]
        my_expeds = [e for e in state['expeditions'] if e['owner'] == 1]
        other_expeds = [e for e in state['expeditions'] if e['owner'] != 1]

        if not my_planets or not other_planets:
            move(None)
        else:

            # Find my planet with most future ships
            # TODO save planets that might get lost
            origin = max(my_planets, key=lambda p: future_count(p, 1, expeds))
            
            # 1) Find nearest nobody planet that won't be mine
            # dest = min([p for p in other_planets if not future_count(p, 1, expeds)], key=lambda p: dist_sq(p, origin))
            dest = min([p for p in other_planets], key=lambda p: dist_sq(p, origin))
            dest_count = origin['ship_count'] - 1
            if dest is None:
                # 2) Find enemy planet with least future ships
                dest = min([p for p in other_planets if p['owner'] == 2], key=lambda p: future_count(p, 2, expeds))


            if dest is not None:
                # TODO fire once I have enough ships
                move({
                    'origin': origin['name'],
                    'destination': dest['name'],
                    'ship_count': dest_count
                })

def move(command):
    record = { 'moves': [command] }
    print(json.dumps(record))
    sys.stdout.flush()

def dist_sq(p1, p2):
    '''Returns the squared distance between two planets.'''
    return (p1['x'] - p2['x']) ** 2 + (p1['y'] - p2['y']) ** 2

def future_count(planet, by_owner, expeds):
    '''Returns the expected ship count by an owner on a planet, or zero if it won't be theirs.'''
    init_count = planet['ship_count']
    sim_count = 0
    sim_owner = planet['owner']
    result = 0

    # Sort relevant expeds by collision time (earliest first)
    inc_all = [e for e in expeds if e['destination'] == planet['name']]
    inc_all.sort(key=lambda e: e['turns_remaining'])

    if not by_owner:
        total_ships = sum([e['ship_count'] for e in inc_all])
        result = init_count - total_ships

    else:
        # Simulate every fight and adjust expected/future ship count
        for e in inc_all:
            # Handle every ship separately
            for i in range(0, e['ship_count']):
                if sim_owner:
                    # Planet is owned
                    if sim_owner == e['owner']:
                        # Owner receives bonus
                        sim_count += 1
                    else:
                        # Owner gets attacked
                        sim_count -= 1
                        if sim_count == 0:
                            # Planet is nobody again
                            sim_owner = 0
                        
                else:
                    # Planet is nobody
                    if sim_count:
                        # Nobody ship neutralized
                        sim_count -= 1
                    else:
                        # New owner arrives
                        sim_count = 1
                        sim_owner = e['owner']

        if sim_owner == by_owner:
            result = sim_count
        else:
            result = -sim_count
    
    return result


if __name__ == '__main__':
    main()
