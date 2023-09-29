POSSIBLE_NOTES = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]


class GameData:
    def __init__(self, agent_pos: tuple, matrix: list, max_turns: int):
        self.__matrix        = matrix
        self.grid_width      = len(self.__matrix)
        self.grid_height     = len(self.__matrix[0])
        self.agent_pos       = agent_pos
        self.remaining_turns = max_turns

    def look_around(self):
        heard_notes_set = set()
        for i, i_item in enumerate(self.__matrix):
            for j, j_item in enumerate(i_item):
                if abs(self.agent_pos[0] - i) + abs(self.agent_pos[1] - j) == 1:
                    if j_item in POSSIBLE_NOTES:
                        heard_notes_set.add(j_item)
        return sorted(list(heard_notes_set))

    def get_current_value(self):
        return self.__matrix[self.agent_pos[0]][self.agent_pos[1]]
