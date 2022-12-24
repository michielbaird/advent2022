import sys


DELTAS = [(0,1), (1,0), (-1, 0), (0, -1)]

def main():
    valley = sys.stdin.read().split("\n")
    start = (-1, valley[0].index(".") -1)
    end = (len(valley)-2, valley[-1].index(".") - 1)
    width = len(valley[0])-2
    height = len(valley) - 2
    left_blizzard = [
        set(x-1 for x in range(1,len(line)-1) if line[x] == "<")
        for line in valley[1:-1]
    ]
    right_blizzard = [
        set(x-1 for x in range(1,len(line)-1) if line[x] == ">")
        for line in valley[1:-1]
    ]
    up_blizzard = [
        set(x-1 for x in range(1, len(valley)-1) if valley[x][y] == "^")
        for y in range(1,len(valley[0])-1)
    ]
    down_blizzard = [
        set(x-1 for x in range(1,len(valley)-1) if valley[x][y] == "v")
        for y in range(1,len(valley[0])-1)
    ]
    #print(le)

    print(end)
    def check_blizzards(row, col, time):
        nonlocal width, height
        if row == -1 or row == height:
            return False
        return ((col - time) % width) in right_blizzard[row] or \
                        ((col + time) % width) in left_blizzard[row] or \
                        ((row - time) % height) in down_blizzard[col] or \
                        ((row + time) % height) in up_blizzard[col]
    t = 0
    for begin, goal in [(start, end), (end, start), (start, end)]:
        que = {begin}
        found = False
        while len(que) > 0:
            next_que = set()
            next_t = t+1
            for row, col in que:
                if not check_blizzards(row, col, next_t):
                    next_que.add((row, col))
                for dr, dc in DELTAS:
                    next_row, next_col = row + dr, col + dc
                    if (next_row, next_col) == goal:
                        print("Goal Reached: ", next_t)
                        found = True
                        break
                    if next_row < 0 or next_row >= height or \
                        next_col < 0 or next_col >= width:
                        # We hit a wall
                        continue
                    if check_blizzards(next_row, next_col, next_t):
                        # There is a blizzard in the way
                        continue
                    next_que.add((next_row, next_col))
                if found:
                    break
            if found:
                break
            # print(next_t, next_que)
            # if next_t == 20: 
            #     break

            que = next_que
            t = next_t

    print(width, height)
    print(start, end)



    pass



if __name__ == "__main__":
    main()

