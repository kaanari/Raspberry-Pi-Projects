import pygame
import mazegenerator
import mazesolver
'''

+---------->
|    Y
|
| X
|
|
v

'''
### SETTINGS ###
maze_height = 12# X axis
maze_width = 12 # Y axis

cell_edge_length = 30 #Each Cell Edge Length
wall_thickness = 5 #Wall Thickness
###          ###


pygame.init()
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 20)


total_cell_edge = int(cell_edge_length + 2 * wall_thickness)
mazesize = [maze_height,maze_width]
h_maze = total_cell_edge * mazesize[0] + int(2 * wall_thickness)
w_maze = total_cell_edge * mazesize[1] + int(2 * wall_thickness)

h_information = 150

w_screen = w_maze
h_screen = h_maze + h_information

selected_x=0
selected_y=0
screen = pygame.display.set_mode((w_screen, h_screen))
done = False
clock = pygame.time.Clock()

position = [0,0] # (x,y)

keys = [False,False,False,False]
validation = False

maze_number,maze_ascii,maze_v2 = mazegenerator.make_maze(mazesize[0],mazesize[1])

print(maze_ascii)

maze = []

while not done:
    for event in pygame.event.get(): ## EVENTS
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                keys[0] = True
            elif event.key == pygame.K_DOWN:
                keys[1] = True
            elif event.key == pygame.K_LEFT:
                keys[2] = True
            elif event.key == pygame.K_RIGHT:
                keys[3] = True
            elif event.key == pygame.K_q:
                done = True
            validation = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                keys[0] = False
            elif event.key == pygame.K_DOWN:
                keys[1] = False
            elif event.key == pygame.K_LEFT:
                keys[2] = False
            elif event.key == pygame.K_RIGHT:
                keys[3] = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # MOUSEBUTTONDOWN events have a pos and a button attribute
            # which you can use as well. This will be printed once per
            # event / mouse click.
            selected_x,selected_y=pygame.mouse.get_pos()
            selected_x= int(selected_x/ total_cell_edge)
            selected_y=int(selected_y/total_cell_edge)

    ## DRAWING MAZE FRAME ##
    pygame.draw.rect(screen, (100,0, 0), pygame.Rect(0, 0, w_maze, h_maze)) ## Red Frame
    pygame.draw.rect(screen, (200,200, 200), pygame.Rect(wall_thickness, wall_thickness, w_maze-int(wall_thickness*2), h_maze-int(wall_thickness*2))) ## Maze Background Color
    ## DRAWING MAZE FRAME ##
    if selected_y and selected_x :
        pygame.draw.rect(screen, (150, 150, 150),
                         pygame.Rect((wall_thickness+1+(selected_x*w_maze-1))/12, wall_thickness+1+(selected_y*h_maze-1)/12, total_cell_edge,
                                     total_cell_edge))  ## Maze Background Color
    ## DRAWING MAZE ##

    a = 0
    d=1
    for i in maze_number:
        b = 0
        c = 0
        e = 0
        f = 0
        for wall in i:
            wall = int(wall)
            if a % 2 == 0:
                if wall == 1:

                    pygame.draw.rect(screen, (100, 0, 0), pygame.Rect(wall_thickness + int((b)*(total_cell_edge-wall_thickness/mazesize[1])),wall_thickness + int(a*(total_cell_edge)/2),wall_thickness , total_cell_edge+wall_thickness))
                    f+=1

                elif wall == 2:
                    f+=1
                else:
                    f+=1
                    b+=1

            else:

                if wall == 1:

                    pygame.draw.rect(screen, (100, 0, 0), pygame.Rect(wall_thickness + int((c)*(total_cell_edge-wall_thickness/mazesize[1])),wall_thickness + d*total_cell_edge,total_cell_edge+2*wall_thickness/3, wall_thickness))
                    e+=1
                    c+=1
                elif wall==2:
                    e+=1
                    pass
                else:
                    e+=1
                    c+=1
        if a%2 == 1:
            d += 1

        a += 1

    ## DRAWING MAZE ##

    ## DRAWING MAZE INFO BOX ##
    pygame.draw.rect(screen, (100,0, 0), pygame.Rect(0, h_maze, w_maze, h_information)) ## Red Frame
    pygame.draw.rect(screen, (200,200, 200), pygame.Rect(wall_thickness, h_maze, w_maze-int(wall_thickness*2), h_information-int(wall_thickness*2))) ## Red Frame Background
    x_box = font.render('X = {0}'.format(position[0]), False, (0, 0, 0))
    screen.blit(x_box, (wall_thickness + w_screen/40 , wall_thickness + h_maze))
    y_box = font.render('Y = {0}'.format(position[1]), False, (0, 0, 0))
    screen.blit(y_box, (wall_thickness + (6 * w_screen / 40), wall_thickness + h_maze))
    x2_box = font.render('Selected X = {0}'.format(selected_x), False, (0, 0, 0))
    screen.blit(x2_box, (wall_thickness + 11*(w_screen / 40), wall_thickness + h_maze))
    y2_box = font.render('Selected Y = {0}'.format(selected_y), False, (0, 0, 0))
    screen.blit(y2_box, (wall_thickness + (20 * w_screen / 40), wall_thickness + h_maze))

    ## DRAWING MAZE INFO BOX ##


    #for i in range(mazesize[0] + 1):
     #   pygame.draw.rect(screen, (100, 0, 0), pygame.Rect(2.5+i*(total_cell_edge),0,wall_thickness , h_maze))
      #  pygame.draw.rect(screen, (100, 0, 0), pygame.Rect(0, 2.5+i*(total_cell_edge),w_maze , wall_thickness))

    if validation:

        if keys[0] and position[0] > 0 and int(maze_v2[2*(position[0])][2*(position[1])+1]) == 0:
            position[0]-=1
        if keys[1] and position[0] < mazesize[0] - 1  and int(maze_v2[2*(position[0]+1)][2*(position[1])+1]) == 0:
            position[0]+=1
        if keys[2] and position[1] > 0 and int(maze_v2[1+2*position[0]][2*(position[1])]) == 0:
            position[1]-=1
        if keys[3] and position[1] < mazesize[1] - 1 and int(maze_v2[1+2*position[0]][2*(position[1]+1)]) == 0:
            position[1]+=1
        validation = False

    #print("x = ",position[0]," y = ",position[1])
    pygame.draw.circle(screen,(0,0,0),(int((total_cell_edge/2) + wall_thickness)+ int(position[1]*(total_cell_edge)),int((total_cell_edge/2) + wall_thickness) + int(position[0]*(total_cell_edge))),5) ## Position Point
    pygame.display.flip()
    clock.tick(60)
pygame.quit()