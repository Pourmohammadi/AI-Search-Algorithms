from base_agent import BaseAgent
from game_data import GameData
from pyswip import Prolog

counter = 0
is_alight_visited = False
find_in_goals = False
inital = True
prolog = Prolog()
last_move = ''

class Agent(BaseAgent):
    def do_move(self, game_data: GameData):
        global last_move
        global is_alight_visited
        global find_in_goals
        global inital
        x_cordinate = game_data.agent_pos[0]
        y_cordinate = game_data.agent_pos[1]

        if inital:
            s = 'dark' + '(' + str(x_cordinate) + '/' + str(y_cordinate) + ')'
            prolog.assertz(s)
            s = 'safe' + '(' + str(x_cordinate) + '/' + str(y_cordinate) + ')'
            prolog.assertz(s)
            prolog.assertz('(safe(X/Y) :- dark(X/Z), Z =:= Y-1)')
            prolog.assertz('(safe(X/Y) :- dark(X/Z), Z =:= Y+1)')
            prolog.assertz('(safe(X/Y) :- dark(Z/Y), Z =:= X-1)')
            prolog.assertz('(safe(X/Y) :- dark(Z/Y), Z =:= X+1)')

        inital = False

        s = 'visited' + '(' + str(x_cordinate) + '/' + str(y_cordinate) + ')'
        prolog.assertz(s)

        if len(game_data.look_around()) == 0:
            s = 'dark' + '(' + str(x_cordinate) + '/' + str(y_cordinate) + ')'
            prolog.assertz(s)
        elif len(set(game_data.look_around())) == 1 and 'a' in set(game_data.look_around()):
            s = 'alight' + '(' + str(x_cordinate) + '/' + str(y_cordinate) + ')'
            prolog.assertz(s)
            if not is_alight_visited:
                prolog.assertz('(safe(X/Y) :- alight(X/Z), Z =:= Y-1)')
                prolog.assertz('(safe(X/Y) :- alight(X/Z), Z =:= Y+1)')
                prolog.assertz('(safe(X/Y) :- alight(Z/Y), Z =:= X-1)')
                prolog.assertz('(safe(X/Y) :- alight(Z/Y), Z =:= X+1)')
                prolog.assertz('(goal(X/Y) :- alight(X/Z), Z =:= Y-1)')
                prolog.assertz('(goal(X/Y) :- alight(X/Z), Z =:= Y+1)')
                prolog.assertz('(goal(X/Y) :- alight(Z/Y), Z =:= X-1)')
                prolog.assertz('(goal(X/Y) :- alight(Z/Y), Z =:= X+1)')
                is_alight_visited = True
                find_in_goals = True
        else:
            s = 'light' + '(' + str(x_cordinate) + '/' + str(y_cordinate) + ')'
            prolog.assertz(s)

        search_for_goals = find_in_goals
        find_in_unvisited = True
        moved = False
        move = ''
        while(not moved):
            if search_for_goals:
                s = 'goal' + '(' + str(x_cordinate) + '/' + str(y_cordinate) + ')'
                c = bool(list(prolog.query(s)))
                if c:
                    if last_move == 'E': move = "W"
                    elif last_move == 'W': move = "E"
                    elif last_move == 'N': move = "S"
                    else: move = "N"
                    break
            if x_cordinate+1 in range(game_data.grid_width) and not moved:
                s = 'safe' + '(' + str(x_cordinate+1) + '/' + str(y_cordinate) + ')'
                a = bool(list(prolog.query(s)))
                s = 'visited' + '(' + str(x_cordinate+1) + '/' + str(y_cordinate) + ')'
                b = bool(list(prolog.query(s)))
                if search_for_goals:
                    s = 'goal' + '(' + str(x_cordinate+1) + '/' + str(y_cordinate) + ')'
                    c = bool(list(prolog.query(s)))
                    if c and not b:
                        move = "E"
                        moved = True
                elif a and find_in_unvisited:
                    if not b:
                        move = "E"
                        moved = True
                elif a:
                    move = "E"
                    moved = True
            if y_cordinate+1 in range(game_data.grid_height) and not moved:
                s = 'safe' + '(' + str(x_cordinate) + '/' + str(y_cordinate+1) + ')'
                a = bool(list(prolog.query(s)))
                s = 'visited' + '(' + str(x_cordinate) + '/' + str(y_cordinate+1) + ')'
                b = bool(list(prolog.query(s)))
                if search_for_goals:
                    s = 'goal' + '(' + str(x_cordinate) + '/' + str(y_cordinate+1) + ')'
                    c = bool(list(prolog.query(s)))
                    if c and not b:
                        move = "N"
                        moved = True
                elif a and find_in_unvisited:
                    if not b:
                        move = "N"
                        moved = True
                elif a:
                    move = "N"
                    moved = True
            if x_cordinate-1 in range(game_data.grid_width) and not moved:
                s = 'safe' + '(' + str(x_cordinate-1) + '/' + str(y_cordinate) + ')'
                a = bool(list(prolog.query(s)))
                s = 'visited' + '(' + str(x_cordinate-1) + '/' + str(y_cordinate) + ')'
                b = bool(list(prolog.query(s)))
                if search_for_goals:
                    s = 'goal' + '(' + str(x_cordinate-1) + '/' + str(y_cordinate) + ')'
                    c = bool(list(prolog.query(s)))
                    if c and not b:
                        move = "W"
                        moved = True
                elif a and find_in_unvisited:
                    if not b:
                        move = "W"
                        moved = True
                elif a:
                    move = "W"
                    moved = True
            if y_cordinate-1 in range(game_data.grid_height) and not moved:
                s = 'safe' + '(' + str(x_cordinate) + '/' + str(y_cordinate-1) + ')'
                a = bool(list(prolog.query(s)))
                s = 'visited' + '(' + str(x_cordinate) + '/' + str(y_cordinate-1) + ')'
                b = bool(list(prolog.query(s)))
                if search_for_goals:
                    s = 'goal' + '(' + str(x_cordinate) + '/' + str(y_cordinate-1) + ')'
                    c = bool(list(prolog.query(s)))
                    if c and not b:
                        move = "S"
                        moved = True
                if a and find_in_unvisited:
                    if not b:
                        move = "S"
                        moved = True
                elif a:
                    move = "S"
                    moved = True

            if not search_for_goals:
                find_in_unvisited = False
                    
            search_for_goals = False
        last_move = move
        return move


if __name__ == "__main__":
    agent = Agent()
    agent.play()
