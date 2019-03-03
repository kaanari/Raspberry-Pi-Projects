import collections

wall, clear, goal = "1", "0", "F"
width, height = 9, 9
grid = ['111111111',
        '100F10001',
        '101110101',
        '100000101',
        '101111111',
        '100010001',
        '111011101',
        '100000001',
        '111111111']
grid2 =['111111111',
        '100F10001',
        '101110101',
        '100000101',
        '101111111',
        '100010001',
        '111011101',
        '100000001',
        '111111111']

def bfs(grid, start,width,height):
    queue = collections.deque([[start]])
    seen = set([start])
    while queue:
        path = queue.popleft()
        x, y = path[-1]
        if grid[y][x] == goal:
            for x2,y2 in path:
                s = list(grid[y2])
                s[x2] = 'X'
                grid[y2] = "".join(s)
            return grid
        for x2, y2 in ((x+1,y), (x-1,y), (x,y+1), (x,y-1)):
            if 0 <= x2 < width and 0 <= y2 < height and grid[y2][x2] != wall and (x2, y2) not in seen:
                queue.append(path + [(x2, y2)])
                seen.add((x2, y2))


#path = bfs(grid, (1, 1),width,height)
#print(path)
# [(5, 2), (4, 2), (4, 3), (4, 4), (5, 4), (6, 4)]