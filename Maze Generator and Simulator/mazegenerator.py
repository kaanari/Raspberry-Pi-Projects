from random import shuffle, randrange

def make_maze(w=2, h=4):
    vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]
    ver = [["10"] * w + ['1'] for _ in range(h)] + [[]]
    hor = [["21"] * w + ['2'] for _ in range(h + 1)]

    vis2 = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]
    ver2 = [["|  "] * w + ['|'] for _ in range(h)] + [[]]
    hor2 = [["+--"] * w + ['+'] for _ in range(h + 1)]

    vis3 = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]
    ver3 = [["10"] * w + ['1'] for _ in range(h)] + [[]]
    hor3 = [["11"] * w + ['1'] for _ in range(h + 1)]

    def walk(x, y):
        vis[y][x] = 1
        vis2[y][x] = 1


        d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        shuffle(d)
        for (xx, yy) in d:
            if vis[yy][xx]: continue
            if xx == x: hor[max(y, yy)][x] = "20"
            if yy == y: ver[y][max(x, xx)] = "0"
            if vis2[yy][xx]: continue
            if xx == x: hor2[max(y, yy)][x] = "+  "
            if yy == y: ver2[y][max(x, xx)] = "   "
            if vis3[yy][xx]: continue
            if xx == x: hor3[max(y, yy)][x] = "10"
            if yy == y: ver3[y][max(x, xx)] = "00"

            walk(xx, yy)

    walk(randrange(w), randrange(h))
    s = ""

    for (a, b) in zip(hor, ver):
        s += ''.join(a + ['\n'] + b + ['\n'])
    maze = list(filter(None, s.split('\n')))  # fastest
    maze_number = []
    for i in maze:
        maze_number.append(list(i[1:len(i)-1]))

    maze_number = maze_number[1:len(maze_number)-1]
    maze_ascii = ""
    for (a, b) in zip(hor2, ver2):
        maze_ascii += ''.join(a + ['\n'] + b + ['\n'])

    #print(maze_ascii)


    s2=""
    for (a, b) in zip(hor3, ver3):
        s2 += ''.join(a + ['\n'] + b + ['\n'])
    s2 = list(filter(None, s2.split('\n')))  # fastest

    maze_number_v2 = []
    for i in s2:
        maze_number_v2.append(list(i))

    #print(maze_number)

    return maze_number,maze_ascii,maze_number_v2

#make_maze(4,4)


