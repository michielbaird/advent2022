import sys
from collections import deque

BASE_CUBE = {
    0: {0: (5, 2), 1: (3, 0), 2: (2, 0), 3: (1, 0)},
    1: {0: (0, 3), 1: (2, 3), 2: (4, 3), 3: (5, 3)},
    2: {0: (0, 2), 1: (3, 3), 2: (4, 0), 3: (1, 1)},
    3: {0: (0, 1), 1: (5, 1), 2: (4, 1), 3: (2, 1)},
    4: {0: (2, 2), 1: (3, 2), 2: (5, 0), 3: (1, 2)},
    5: {0: (4, 2), 1: (3, 1), 2: (0, 0), 3: (1, 3)},
}
FACE_DELTAS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


class Face:
    def __init__(self, length):
        self.rotation = 0
        self.length = length
        self.face_id = 0
        self.filled = False
        self.min_row = 0
        self.max_row = 0
        self.min_col = 0
        self.max_col = 0
        self.sides = [[] for _ in range(4)]
    def set_face(self,
        rotation,
        face_id,
        row,
        col,
        length
    ):
        self.rotation = rotation  
        self.min_row = row
        self.max_row = row + length - 1
        self.min_col = col
        self.max_col = col + length - 1
        self.face_id = face_id

    def get_index(self, row, col):
        pass
    
    def get_position(self, index, entry_side):
        pass


def get_input():
    parts = [line for line in sys.stdin.read().split("\n\n")]
    raw_map = parts[0].split("\n")
    
    raw_instructions = parts[1]
    val = 0
    instructions = []
    for c in raw_instructions:
        if ord(c) >= ord("0") and ord(c) <= ord("9"):
            val *= 10
            val += ord(c) - ord("0")
            continue
        if val != 0:
            instructions.append(val)
            val = 0
        instructions.append(c)
    if val != 0:
            instructions.append(val)
    length = max(len(raw_map), max(len(v) for v in raw_map))//4
    return raw_map, instructions, length

def label_map(cube_map, length):
    index = 0
    result = {}
    first = None
    for row in range(0, len(cube_map), length):
        for col in range(0, len(cube_map[row]), length):
            if cube_map[row][col] != " ":
                if first is None:
                    first = (row, col)
                result[(row, col)] = index
                index += 1
    return result, first

def main():
    cube_map, instructions, length = get_input()
    map_labels, first_face = label_map(cube_map, length)
    faces = [Face(length) for _ in range(6)]

    faces[0].set_face(0, 0, first_face[0], first_face[1], length)
    que = deque()
    que.append((first_face, 0))
    while len(que) > 0:
        (row, col), face_id = que.popleft()
        input_id = map_labels[(row, col)]
        rotation = faces[face_id].rotation
        for i in range(4):
            next_row = row + FACE_DELTAS[i][0]*length
            next_col = col + FACE_DELTAS[i][1]*length
            if (next_input_id := map_labels.get((next_row, next_col))) is None:
                continue
            next_face_id, entry_side = BASE_CUBE[face_id][i]
            if faces[next_face_id].filled:
                continue
            next_rotation = None # xcxc
            faces[next_face_id].set_face(
                next_rotation,
                next_input_id,
                next_row, next_col, length
            )
            


    

    #print(cube_map)
    print(instructions)
    print(length)
    print(map_labels)
    print(first_face)

if __name__ == "__main__":
    main()