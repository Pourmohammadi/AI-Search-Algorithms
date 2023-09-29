# Reza Pourmohammadi
# 983613010

from base_agent import BaseAgent
from game_data import GameData

is_Astar_done = False
shortest_path = []
counter = 0
max_turns = 0
class Agent(BaseAgent):
    def do_move(self, game_data: GameData):

        global is_Astar_done
        global shortest_path
        global counter
        global max_turns
        max_turns = game_data.remaining_turns
        
        if not is_Astar_done:
            mat = []
            for i in range(game_data.grid_width):
                mat.append([])
            for i in range(game_data.grid_width):
                for j in range(game_data.grid_height):
                    mat[game_data.grid_width-1-i].append(game_data.matrix[j][i])

            graph = {}
            for i in range(game_data.grid_width):
                for j in range(game_data.grid_height):
                    graph.setdefault((i,j), [])
            for i in range(game_data.grid_width):
                for j in range(game_data.grid_height):
                    if i > 0:
                        graph[(i,j)].append((i-1,j))
                    if i < game_data.grid_width-1:
                        graph[(i,j)].append((i+1,j))
                    if j > 0:
                        graph[(i,j)].append((i,j-1))
                    if j < game_data.grid_height-1:
                        graph[(i,j)].append((i,j+1))
            
            goals = []
            for i in range(game_data.grid_width):
                for j in range(game_data.grid_height):
                    if mat[i][j] == game_data._GameData__melody[0]:
                        goals.append((i,j))

            huristic = []
            for i in range(game_data.grid_width):
                huristic.append([])
            for i in range(game_data.grid_width):
                for j in range(game_data.grid_height):
                    if mat[i][j] == game_data._GameData__melody[0]:
                        huristic[i].append(0)
                    elif mat[i][j] == '.':
                        min = game_data.grid_height + game_data.grid_width
                        for goal in goals:
                            h = abs(goal[0]-i) + abs(goal[1]-j)
                            if min > h:
                                min = h
                        huristic[i].append(min)
                    else:   
                        huristic[i].append(game_data.grid_height + game_data.grid_width)
                        
            agent_correct_pos = ((game_data.grid_width-1)-game_data.agent_pos[1],game_data.agent_pos[0])
            flag = True

            open_list = set([agent_correct_pos])
            closed_list = set([])
            g = {}
            g[agent_correct_pos] = 0
            parents = {}
            parents[agent_correct_pos] = agent_correct_pos

            while flag and len(open_list) > 0:
                best = None
                for node in open_list:
                    if best == None:
                        best = node
                    elif (g[node] + huristic[node[0]][node[1]]) < (g[best] + huristic[best[0]][best[1]]):
                        best = node
                
                if mat[best[0]][best[1]] == game_data._GameData__melody[0]:
                    while parents[best] != best:
                        shortest_path.append(best)
                        best = parents[best]
                    shortest_path.append(agent_correct_pos)
                    shortest_path.reverse()
                    flag = False
                
                if flag:
                    for neighbor in graph[best]:
                        if neighbor not in open_list and neighbor not in closed_list:
                            open_list.add(neighbor)
                            parents[neighbor] = best
                            g[neighbor] = g[best] + 1
                        else:
                            if g[neighbor] > g[best] + 1:
                                g[neighbor] = g[best] + 1
                                parents[neighbor] = best
                                if neighbor in closed_list:
                                    closed_list.remove(neighbor)
                                    open_list.add(neighbor)
                    open_list.remove(best)
                    closed_list.add(best)
            is_Astar_done = True
        
        move = ""
        if counter < len(shortest_path)-1 and max_turns:
            if shortest_path[counter][0]-shortest_path[counter+1][0] == 1:
                move = "N"
            elif shortest_path[counter][0]-shortest_path[counter+1][0] == -1:
                move = "S"
            elif shortest_path[counter][1]-shortest_path[counter+1][1] == 1:
                move = "W"
            elif shortest_path[counter][1]-shortest_path[counter+1][1] == -1:
                move = "E"
            counter += 1
            max_turns -= 1

        return move
        
if __name__ == "__main__":
    agent = Agent()
    agent.play()