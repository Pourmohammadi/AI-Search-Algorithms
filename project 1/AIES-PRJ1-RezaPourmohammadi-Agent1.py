from base_agent import BaseAgent
from game_data import GameData

is_bfs_done = False
shortest_path = []
counter = 0
max_turns = 0
class Agent(BaseAgent):
    def do_move(self, game_data: GameData):

        global is_bfs_done
        global shortest_path
        global counter
        global max_turns
        max_turns = game_data.remaining_turns

        if not is_bfs_done:
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
            
            agent_correct_pos = ((game_data.grid_width-1)-game_data.agent_pos[1],game_data.agent_pos[0])
            flag = True
            
            path_list  = [[agent_correct_pos]]
            path_index = 0
            previous_nodes = {agent_correct_pos}
            if mat[agent_correct_pos[0]][agent_correct_pos[1]] == game_data._GameData__melody[0]:
                shortest_path = path_list[path_index][:]
            else:
                while (path_index < len(path_list)) and flag:
                    current_path = path_list[path_index]
                    last_node = current_path[-1]
                    next_nodes = graph[last_node]
                    for node in next_nodes:
                        if game_data._GameData__melody[0] == mat[node[0]][node[1]]:
                            current_path.append(node)
                            shortest_path = current_path[:]
                            flag = False
                    if flag:
                        for next_node in next_nodes:
                            if not next_node in previous_nodes and (mat[next_node[0]][next_node[1]] == '.' or  mat[next_node[0]][next_node[1]] == game_data._GameData__melody[0]):
                                new_path = current_path[:]
                                new_path.append(next_node)
                                path_list.append(new_path)
                                previous_nodes.add(next_node)
                    path_index += 1
            is_bfs_done = True

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