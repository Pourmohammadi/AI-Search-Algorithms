import random
from base_agent import BaseAgent
from game_data import GameData
import numpy as np
from time import sleep


def direction_matrix_printer(cost_matrix,x,y):
    print(f"we are here {x,y}")
    print('direction matrix : ')
    for key,value in cost_matrix.items():
        print(f"{key} : {value}")

goal_melody = []
phase = 0
queue = []
path = []
direction_matrix = {}


class Agent(BaseAgent):

    def do_move(self, game_data: GameData):


        global goal_melody
        global phase
        global direction_matrix
        global path

        if phase == 0:
            goal_melody = game_data._GameData__melody
            all_notes = set()
            # find all the notes in matrix:
            for i in range(game_data.grid_height):
                for j in range(game_data.grid_width):
                    if game_data.matrix[i][j] not in all_notes:
                        all_notes.add(game_data.matrix[i][j])
            all_notes.remove('.')
            print('all notes',all_notes)

            exist_melody = []
            for note in goal_melody:
                if note in all_notes:
                    exist_melody.append(note)

            # find the closest melody to our goal melody
            if len(exist_melody)<len(goal_melody):
                iterations = len(goal_melody) - len(exist_melody)
                for i in range(iterations):
                    t1 = exist_melody.copy()
                    t2 = exist_melody.copy()
                    t1.append('a')
                    for note in all_notes:
                        t2.append(note)
                        before = game_data.h(t1)
                        after = game_data.h(t2)
                        if after < before:
                            t1 = t2.copy()
                        t2.pop()

                    exist_melody = t1

            print('eixst melody', exist_melody)
            goal_melody = exist_melody.copy()
            # sleep(2)
            phase = 1

        if phase == 1:
            current_note = goal_melody.pop(0)
            sleep(1)
            # calculate the cost for each cell using BFS
            queue = []
            x,y = game_data.agent_pos
            queue.append((x,y))
            visited = set()
            visited.add((x,y))
            while len(queue):
                x,y = queue.pop(0)

                if game_data.matrix[x][y] == current_note:
                    print("found current note: ", current_note)
                    # start doing backtrack
                    if (x,y) not in direction_matrix:
                        path.append('nomove')
                        phase = 2
                        break

                    i,j,direction = direction_matrix[(x,y)]
                    while (i,j) in direction_matrix:
                        path.append(direction)
                        i,j,direction = direction_matrix[i,j]
                    path.append(direction)
                    print("this is the path: ", path)
                    phase = 2
                    # clear directions
                    direction_matrix.clear()
                    break

                # east
                if 0<=x<game_data.grid_height-1 and (x+1,y) not in visited:
                   if  game_data.matrix[x+1][y] == '.' or game_data.matrix[x+1][y] == current_note:

                        print("East")
                        direction_matrix[(x+1,y)] = (x,y,"E")
                        visited.add((x+1,y))
                        queue.append((x+1,y))             


                # west
                if 0<x<game_data.grid_height and (x-1,y) not in visited:
                   if  game_data.matrix[x-1][y] == '.' or game_data.matrix[x-1][y] == current_note:

                        print("West")
                        direction_matrix[(x-1,y)] = (x,y,"W")
                        visited.add((x-1,y))
                        queue.append((x-1,y))             

                # north
                if 0<=y<game_data.grid_width-1 and (x,y+1) not in visited:
                   if  game_data.matrix[x][y+1] == '.' or game_data.matrix[x][y+1] == current_note:

                        print("North")
                        direction_matrix[(x,y+1)] = (x,y,"N")
                        visited.add((x,y+1))
                        queue.append((x,y+1))             

                # south
                if 0<y<game_data.grid_width and (x,y-1) not in visited:
                   if  game_data.matrix[x][y-1] == '.' or game_data.matrix[x][y-1] == current_note:

                        print("South")
                        direction_matrix[(x,y-1)] = (x,y,"S")
                        visited.add((x,y-1))
                        queue.append((x,y-1))             

                # direction_matrix_printer(direction_matrix,x,y)
                print('*'*20)

        if phase == 2:
            if len(path) == 1:
                phase = 1
            # sleep(4)
            return path.pop()

if __name__ == "__main__":
    
    agent = Agent()
    
    agent.play()
