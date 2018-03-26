# From MOZAIC repo
# Doesn't work?

import json, sys, math

# This bot will always attack the closest planet it can attack.
# It will not attack if it already has an expedition going.
def main():
    player = sys.argv[1]

    game_state = json.load(sys.stdin)
    if len([exp for exp in game_state["expeditions"] if exp["owner"] == player]) != 0:
        do_empty_move()
        return

    own_planets = [planet["planet"] for planet in game_state["planets"]
                    if planet["planet"]["owner"] == player]
    other_planets = [planet["planet"] for planet in game_state["planets"]
                    if planet["planet"]["owner"] != player]

    (closest_own_planet, closest_other_planet) = find_closest_planet(own_planets, other_planets)
    if closest_own_planet is None or closest_other_planet is  None:
        do_empty_move()
        return
    do_move(closest_own_planet, closest_other_planet)

def find_closest_planet(own_planets, other_planets):
    closest_distance = float("inf")
    closest_own_planet = None
    closest_other_planet = None
    for own_planet in own_planets:
        for other_planet in other_planets:
            distance = calculate_distance_between_planets(own_planet, other_planet)
            if distance < closest_distance \
            and own_planet["ship_count"] > other_planet["ship_count"]:
                closest_distance = distance
                closest_own_planet = own_planet
                closest_other_planet = other_planet
    return (closest_own_planet, closest_other_planet)

def calculate_distance_between_planets(first_planet, second_planet):
    return math.sqrt((second_planet["x"] - first_planet["x"])**2
            + (second_planet["y"] - first_planet["y"])**2)

def get_number_of_ships_to_send(own_planet, other_planet):
    number_of_ships = own_planet["ship_count"] - other_planet["ship_count"]
    number_of_ships += int((own_planet["ship_count"] - number_of_ships)/2) + 1
    return number_of_ships

def do_move(own_planet, other_planet):
    move = {}
    move["origin"] = own_planet["name"]
    move["destination"] = other_planet["name"]
    move["ship_count"] = get_number_of_ships_to_send(own_planet, other_planet)
    command = {}
    command["moves"] = [move]
    print(json.dumps(data))

def do_empty_move():
    print(json.dumps({"moves":{}}))

if __name__ == "__main__":
    main()
