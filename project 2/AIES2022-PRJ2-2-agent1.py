import random
from base_agent import BaseAgent
from game_data import GameData
import numpy as np
from time import sleep


def cost_matrix_printer(cost_matrix,x,y):
    print(f"we are here {x,y}")
    print('cost matrix : ')
    for key,value in cost_matrix.items():
        print(f"{key} : {value}")

goal_melody = []
phase = 0
queue = []
path = []
cost_matrix = {}

counter = 0


class Agent(BaseAgent):

    def do_move(self, game_data: GameData):


        global goal_melody
        global phase
        global counter 
        global cost_matrix

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
            #calculate the cost based on current note
            current_note = goal_melody.pop(0)
            print(f"Cost of note : {current_note}")
            # find the corrdinates of all the current_note
            note_corrs = []
            for i in range(game_data.grid_height):
                for j in range(game_data.grid_width):
                    cost_matrix[(i,j)] = 0 # reset the cost 
                    if game_data.matrix[i][j]==current_note:
                        note_corrs.append((i,j))
            
            # calculate the cost for each cell using BFS
            queue = []
            for note in note_corrs:
                i,j = note
                queue.append((i,j,0)) # x,y,cost

            # loop until all the cells cost revealed
            while len(queue):
                x,y,cost = queue.pop(0)

                # east
                if 0<=x<game_data.grid_height-1:
                    cost_plus = 0
                    flag = True
                    if (game_data.matrix[x+1][y] == current_note):
                        flag = False
                    elif (game_data.matrix[x+1][y] == '.'):
                        cost_plus = 1
                    else :
                        cost_plus = 999

                    if cost_matrix[(x+1,y)] == 0 or (cost_matrix[(x+1,y)] > cost + cost_plus and cost_matrix[(x+1,y)] < 100):
                        if flag :
                            cost_matrix[(x+1,y)] = cost + cost_plus 
                            print('East')
                            queue.append((x+1,y,cost + cost_plus))

                # west
                if 0<x<game_data.grid_height:
                    cost_plus = 0
                    flag = True
                    if (game_data.matrix[x-1][y] == current_note):
                        flag = False
                    elif (game_data.matrix[x-1][y] == '.'):
                        cost_plus = 1
                    else :
                        cost_plus = 999

                    if cost_matrix[(x-1,y)] == 0 or (cost_matrix[(x-1,y)] > cost + cost_plus and cost_matrix[(x-1,y)] < 100):
                        if flag :
                            cost_matrix[(x-1,y)] = cost + cost_plus 
                            print('West')
                            queue.append((x-1,y,cost + cost_plus))

                # North
                if 0<=y<game_data.grid_width-1:
                    cost_plus = 0
                    flag = True
                    if (game_data.matrix[x][y+1] == current_note):
                        flag = False
                    elif (game_data.matrix[x][y+1] == '.'):
                        cost_plus = 1
                    else :
                        cost_plus = 999

                    if cost_matrix[(x,y+1)] == 0 or (cost_matrix[(x,y+1)] > cost + cost_plus and cost_matrix[(x,y+1)] < 100):
                        if flag :
                            cost_matrix[(x,y+1)] = cost + cost_plus 
                            print('North')
                            queue.append((x,y+1,cost + cost_plus))

                # South
                if 0<y<game_data.grid_width:
                    cost_plus = 0
                    flag = True
                    if (game_data.matrix[x][y-1] == current_note):
                        flag = False
                    elif (game_data.matrix[x][y-1] == '.'):
                        cost_plus = 1
                    else :
                        cost_plus = 999

                    if cost_matrix[(x,y-1)] == 0 or (cost_matrix[(x,y-1)] > cost + cost_plus and cost_matrix[(x,y-1)] < 100):
                        if flag : 
                            cost_matrix[(x,y-1)] = cost + cost_plus 
                            print('South')
                            queue.append((x,y-1,cost + cost_plus)) 

                print('-'*20)
                # cost_matrix_printer(cost_matrix,x,y)
                # input()
            phase = 2
            # sleep(3)          
                
        if phase == 2:
            # Hill climbing
            x,y = game_data.agent_pos
            # if we reach the note

            sleep(1)            
            min_cost = 999
            direction = ""
            # East neighbore 
            if (x+1,y) in cost_matrix:
                if min_cost > cost_matrix[(x+1,y)]:
                    min_cost = cost_matrix[(x+1,y)]
                    direction = 'E'

            # West neighbore 
            if (x-1,y) in cost_matrix:
                if min_cost > cost_matrix[(x-1,y)]:
                    min_cost = cost_matrix[(x-1,y)]
                    direction = 'W'

            # North neighbore 
            if (x,y+1) in cost_matrix:
                if min_cost > cost_matrix[(x,y+1)]:
                    min_cost = cost_matrix[(x,y+1)]
                    direction = 'N'

            # South neighbore 
            if (x,y-1) in cost_matrix:
                if min_cost > cost_matrix[(x,y-1)]:
                    min_cost = cost_matrix[(x,y-1)]
                    direction = 'S'
            if min_cost == 0:
                phase = 1
                print("we reached note")
        
        return direction



if __name__ == "__main__":
    
    agent = Agent()
    
    agent.play()
