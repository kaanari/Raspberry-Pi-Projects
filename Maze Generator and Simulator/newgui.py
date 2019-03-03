import pygame
import mazegenerator
import mazesolver
import pygame.gfxdraw
import copy

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
maze_height = 12 # X axis
maze_width = 12 # Y axis

cell_edge_length = 30 #Each Cell Edge Length
wall_thickness = 5 #Wall Thickness
###          ###


pygame.init()
pygame.font.init()
pygame.mixer.quit()
font = pygame.font.SysFont('Comic Sans MS', 20)
font2 = pygame.font.SysFont('Courier', 18)
font3 = pygame.font.Font("freesansbold.ttf", 12)

total_cell_edge = int(cell_edge_length + 2 * wall_thickness)
mazesize = [maze_height,maze_width]
h_maze = cell_edge_length * mazesize[0] + (mazesize[0]+1)*wall_thickness
w_maze = cell_edge_length * mazesize[1]+ (mazesize[1]+1)*wall_thickness

h_information = 150
w_information2 = 200
w_screen = w_maze + w_information2
h_screen = h_maze + h_information
h_button = (h_maze-2*wall_thickness)/6
w_button = w_information2*3/4
padding_button = (h_maze-h_button * 4)/4

button = 0
selected_x=0
selected_y=0
starting_x = '-'
starting_y = '-'
final_x = '-'
final_y = '-'
direction = 0


screen = pygame.display.set_mode((w_screen, h_screen))
pygame.display.set_caption('Maze Tester')
done = False
clock = pygame.time.Clock()

position = [0,0] # (x,y)

keys = [False,False,False,False]
validation = False
validation_shortest = False
button_valid = True
starting_flag = False
shortest_path = False
press_counter = True

maze_number,maze_ascii,maze_v2 = mazegenerator.make_maze(mazesize[0],mazesize[1])

shortest_path = copy.deepcopy(maze_v2)

maze = []
clock = pygame.time.Clock()

def text_objects(text, font,color = (0,0,0)):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def robotbody(x,y,direction = 0 ,simple = 0):
    len = 14
    x,y = int((cell_edge_length / 2) + wall_thickness - 7) + int(y * (cell_edge_length + wall_thickness)),int(((cell_edge_length / 2) - 9) + wall_thickness) + int(x * (cell_edge_length + wall_thickness))
    if simple == 0:
        if direction == 0: # DOWNWARD
            pygame.draw.circle(screen, (0,0,0), (int(x+len/2),y + len), int(len/2))
            pygame.draw.rect(screen,(0,0,0),(x,y,len,len)) ## 200,150
            pygame.draw.rect(screen,(255,0,0),(x + 6,y + 16,2,6))
            pygame.draw.rect(screen,(255,0,0),(x - 2,y + len,6,2))
            pygame.draw.rect(screen,(255,0,0),(x + 10,y + len,6,2))
            pygame.draw.rect(screen,(0,255,0),(x - 2,y + 2,3,6))
            pygame.draw.rect(screen,(0,255,0),(x + 13,y + 2,3,6))

        elif direction == 1: # RIGHT
            pygame.draw.circle(screen, (0,0,0), (x + len,y + int(len/2)), int(len/2))
            pygame.draw.rect(screen,(0,0,0),(x,y,len,len))
            pygame.draw.rect(screen,(255,0,0),(x + len + 3,y + 6,6,2))
            pygame.draw.rect(screen,(255,0,0),(x + len,y + 10,2,6))
            pygame.draw.rect(screen,(255,0,0),(x + len,y - 2,2,6))
            pygame.draw.rect(screen,(0,255,0),(x + 2,y - 2,6,3))
            pygame.draw.rect(screen,(0,255,0),(x + 2,y + 13,6,3))

        elif direction == -1: # LEFT
            pygame.draw.circle(screen, (0, 0, 0), (x+2, y + int(len/2)), int(len/2))
            pygame.draw.rect(screen, (0, 0, 0), (x+2, y, len, len))
            pygame.draw.rect(screen, (255, 0, 0), (x - 7, y + 6, 6, 2))
            pygame.draw.rect(screen, (255, 0, 0), (x, y + 10, 2, 6))
            pygame.draw.rect(screen, (255, 0, 0), (x, y - 2, 2, 6))
            pygame.draw.rect(screen, (0, 255, 0), (x + 8, y - 2, 6, 3))
            pygame.draw.rect(screen, (0, 255, 0), (x + 8, y + 13, 6, 3))

        else: # UPWARD
            pygame.draw.circle(screen, (0, 0, 0), (x + int(len/2), y +3), int(len/2))
            pygame.draw.rect(screen, (0, 0, 0), (x, y+4, len, len))
            pygame.draw.rect(screen, (255, 0, 0), (x + 6, y - 5, 2, 6))
            pygame.draw.rect(screen, (255, 0, 0), (x - 2, y +3, 6, 2))
            pygame.draw.rect(screen, (255, 0, 0), (x + 10, y +3, 6, 2))
            pygame.draw.rect(screen, (0, 255, 0), (x - 2, y + 11, 3, 6))
            pygame.draw.rect(screen, (0, 255, 0), (x + 13, y + 11, 3, 6))

    else:
        pygame.draw.circle(screen,(0,0,0),(int((cell_edge_length/2) + wall_thickness)+ int(position[1]*(cell_edge_length + wall_thickness)),int(((cell_edge_length/2)) + wall_thickness) + int(position[0]*(cell_edge_length + wall_thickness))),5) ## Position Point

def infobox1():
    global validation_shortest,shortest_path
    pygame.draw.rect(screen, (200, 200, 200),
                     pygame.Rect(wall_thickness, h_maze, w_screen - 2 * wall_thickness, h_information - wall_thickness))
    textSurf, textRect = text_objects("X = {0}".format(position[0]), font3)
    textRect.center = (wall_thickness + w_screen / 15, wall_thickness + h_maze + h_information / 8)
    screen.blit(textSurf, textRect)
    textSurf, textRect = text_objects("Y = {0}".format(position[1]), font3)
    textRect.center = (wall_thickness + 4 * w_screen / 15, wall_thickness + h_maze + h_information / 8)
    screen.blit(textSurf, textRect)

    textSurf, textRect = text_objects("Starting X = {0}".format(starting_x), font3)
    textRect.center = (wall_thickness + 8 * w_screen / 15, wall_thickness + h_maze + h_information / 8)
    screen.blit(textSurf, textRect)
    textSurf, textRect = text_objects("Starting Y = {0}".format(starting_y), font3)
    textRect.center = (wall_thickness + 12 * w_screen / 15, wall_thickness + h_maze + h_information / 8)
    screen.blit(textSurf, textRect)

    textSurf, textRect = text_objects("Finish X = {0}".format(final_x), font3)
    textRect.center = (wall_thickness + 8 * w_screen / 15, wall_thickness + h_maze + 3*h_information / 8)
    screen.blit(textSurf, textRect)
    textSurf, textRect = text_objects("Finish Y = {0}".format(final_y), font3)
    textRect.center = (wall_thickness + 12 * w_screen / 15, wall_thickness + h_maze + 3*h_information / 8)
    screen.blit(textSurf, textRect)

def infobox2():
    pygame.draw.rect(screen, (150, 150, 150), pygame.Rect(w_maze,
                                                        wall_thickness,
                                                        w_information2-wall_thickness,
                                                        h_maze-wall_thickness*2))  ## Background

    if button == 1: pygame.draw.rect(screen, (40, 220, 40), pygame.Rect(w_maze + w_information2 / 2 - w_button / 2,
                                                            h_maze / 80 + wall_thickness + (h_maze) / 8 - h_button / 2,
                                                            w_button - wall_thickness,
                                                            h_button))

    else: pygame.draw.rect(screen, (50, 200, 50), pygame.Rect(w_maze + w_information2 / 2 - w_button / 2,
                                                            h_maze / 80 + wall_thickness + (h_maze) / 8 - h_button / 2,
                                                            w_button - wall_thickness,
                                                            h_button))

    textSurf, textRect = text_objects("{0}".format(button1_text), font3)
    textRect.center = (w_maze+ w_information2/2 , h_maze/80+wall_thickness+(h_maze)/8)
    screen.blit(textSurf, textRect)

    if button == 2: pygame.draw.rect(screen, (40, 40, 240), pygame.Rect(w_maze + w_information2 / 2 - w_button / 2,
                                                            h_maze / 80 + wall_thickness + 2 * (
                                                                h_maze) / 8 - h_button / 2 + padding_button,
                                                            w_button - wall_thickness,
                                                            h_button))

    else: pygame.draw.rect(screen, (30, 30, 200), pygame.Rect(w_maze + w_information2 / 2 - w_button / 2,
                                                            h_maze / 80 + wall_thickness + 2 * (
                                                                h_maze) / 8 - h_button / 2 + padding_button,
                                                            w_button - wall_thickness,
                                                            h_button))

    textSurf, textRect = text_objects("{0}".format(button2_text), font3,(255,255,255))
    textRect.center = (w_maze + w_information2 / 2, h_maze/80+wall_thickness+2*(h_maze)/8-h_button/2+padding_button+h_button/2)
    screen.blit(textSurf, textRect)

    if button == 3: pygame.draw.rect(screen, (230,30, 30), pygame.Rect(w_maze+ w_information2/2 - w_button/2,  h_maze/80+wall_thickness+3*(h_maze)/8-h_button/2+2*padding_button, w_button-wall_thickness, h_button))
    else: pygame.draw.rect(screen, (200,20, 20), pygame.Rect(w_maze+ w_information2/2 - w_button/2,  h_maze/80+wall_thickness+3*(h_maze)/8-h_button/2+2*padding_button, w_button-wall_thickness, h_button))

    if press_counter: button3_text = "Show Shortest Path"
    else: button3_text = "Close Shortest Path"

    textSurf, textRect = text_objects(button3_text, font3)
    textRect.center = (w_maze + w_information2 / 2, h_maze/80+wall_thickness+3*(h_maze)/8-h_button/2+2*padding_button + h_button/2)
    screen.blit(textSurf, textRect)

    if button == 4: pygame.draw.rect(screen, (60, 140, 255), pygame.Rect(w_maze + w_information2 / 2 - w_button / 2,
                                                             h_maze / 80 + wall_thickness + 4 * (
                                                                 h_maze) / 8 - h_button / 2 + 3 * padding_button,
                                                             w_button - wall_thickness,
                                                             h_button))

    else: pygame.draw.rect(screen, (40, 100, 255), pygame.Rect(w_maze + w_information2 / 2 - w_button / 2,
                                                             h_maze / 80 + wall_thickness + 4 * (
                                                                 h_maze) / 8 - h_button / 2 + 3 * padding_button,
                                                             w_button - wall_thickness,
                                                             h_button))

    textSurf, textRect = text_objects("Test you Algorithm", font3)
    textRect.center = (w_maze + w_information2 / 2, h_maze/80+wall_thickness+4*(h_maze)/8-h_button/2+3*padding_button + h_button/2)
    screen.blit(textSurf, textRect)


while not done:
    clock.tick(60)  # framerate 30 per second
    pygame.event.pump()
    events = pygame.event.get()
    pygame.key.set_repeat(10, 10)

    for event in events: ## EVENTS
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP: keys[0] = True
            elif event.key == pygame.K_DOWN: keys[1] = True
            elif event.key == pygame.K_LEFT: keys[2] = True
            elif event.key == pygame.K_RIGHT: keys[3] = True
            elif event.key == pygame.K_q: done = True

            validation = True

        elif event.type == pygame.KEYUP:
            keys = [False,False,False,False]
        elif event.type == pygame.MOUSEMOTION:
            selected_y,selected_x=pygame.mouse.get_pos()
            if (selected_y > w_maze+ w_information2/2 - w_button/2) and selected_y < w_maze+ w_information2/2 - w_button/2+w_button-wall_thickness and button_valid:
                if (selected_x < h_maze/80+wall_thickness+(h_maze)/8-h_button/2+h_button) and (selected_x > h_maze/80+wall_thickness+(h_maze)/8-h_button/2): button = 1
                elif (selected_x < h_maze/80+wall_thickness+2*(h_maze)/8-h_button/2+padding_button+h_button) and (selected_x > h_maze/80+wall_thickness+2*(h_maze)/8-h_button/2+padding_button): button = 2
                elif (selected_x < h_maze/80+wall_thickness+3*(h_maze)/8-h_button/2+2*padding_button+h_button) and (selected_x > h_maze/80+wall_thickness+3*(h_maze)/8-h_button/2+2*padding_button): button = 3
                elif (selected_x < h_maze/80+wall_thickness+4*(h_maze)/8-h_button/2+3*padding_button+h_button) and (selected_x > h_maze/80+wall_thickness+4*(h_maze)/8-h_button/2+3*padding_button): button = 4
                else:
                    if button_valid: button = 0

            else:
                if button_valid: button = 0

            if (selected_x > 0 and selected_y > 0) and (selected_x < h_maze and selected_y < w_maze-2): selected_x, selected_y = int((selected_x - wall_thickness) / (total_cell_edge - wall_thickness)) + 1, int((selected_y - wall_thickness) / (total_cell_edge - wall_thickness)) + 1
            else: selected_x, selected_y = False, False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button:
                button_valid = False
                if selected_x and selected_y and button == 1:
                    shortest_path = copy.deepcopy(maze_v2)
                    starting_x = selected_x -1
                    starting_y = selected_y -1
                    position[0] = starting_x
                    position[1] = starting_y
                    button = 0
                    button_valid = True
                    starting_flag = False
                    validation_shortest = False


                if selected_x and selected_y and button == 2:
                    shortest_path = copy.deepcopy(maze_v2)
                    final_x = selected_x -1
                    final_y = selected_y -1
                    button = 0
                    button_valid = True
                    validation_shortest = False

                if button == 3:
                    if final_x != '-' and final_y != '-' and not validation_shortest:
                        shortest_path[2 * (int(final_x)) + 1][2 * (int(final_y)) + 1] = 'F'
                        shortest_path = mazesolver.bfs(shortest_path, (2 * (int(starting_y)) + 1, 2 * (int(starting_x)) + 1),maze_width * 2 + 1, maze_height * 2 + 1)
                        validation_shortest = True
                        press_counter = False

                    else:
                        press_counter = not press_counter

                    button = 0
                    button_valid = True

        break
        #pygame.time.wait(0)

    ## DRAWING MAZE FRAME ##

    pygame.draw.rect(screen, (150, 150, 150),pygame.Rect(wall_thickness,wall_thickness,(cell_edge_length + wall_thickness) * mazesize[1],(cell_edge_length + wall_thickness) * mazesize[1]))

    ## DRAWING MAZE FRAME ##




    ## DRAWING MAZE ##
    a = 0
    d = 1

    for i in maze_number:
        pygame.time.wait(0)
        b = 0
        c = 0
        e = 0
        f = 0
        for wall in i:
            wall = int(wall)
            if a % 2 == 0:
                if wall == 1:  # tamam
                    pygame.draw.rect(screen, (100, 0, 0), pygame.Rect(
                        (b) * (total_cell_edge - wall_thickness),
                        (a / 2) * (total_cell_edge - wall_thickness) + wall_thickness, wall_thickness,
                        cell_edge_length))
                    f += 1

                elif wall == 2:
                    f += 1

                else:
                    f += 1
                    b += 1

            else:

                if wall == 1:  # tamam
                    pygame.draw.rect(screen, (100, 0, 0), pygame.Rect(
                        (c) * (total_cell_edge - wall_thickness) + wall_thickness,
                        ((((a - 1)) / 2) + 1) * (total_cell_edge - wall_thickness), cell_edge_length,
                        wall_thickness))

                    e += 1
                    c += 1

                elif wall == 2:  # tamam
                    pygame.draw.rect(screen, (100, 0, 0), pygame.Rect(
                        (c) * (total_cell_edge - wall_thickness),
                        ((a / 2)) * (total_cell_edge - wall_thickness) + cell_edge_length - 2 * wall_thickness - 2,
                        wall_thickness,
                        wall_thickness))
                    e += 1

                else:
                    e += 1
                    c += 1

        if a % 2 == 1:
            d += 1

        a += 1

    if not press_counter: ## SHOWING SHORTEST PATH
        row = 0
        for i in range(len(shortest_path)):
            col = 0

            for wall in range(len(shortest_path)):
                if shortest_path[i][wall] == 'X':
                    pygame.draw.rect(screen, (255, 200, 50), pygame.Rect(
                            wall_thickness + (wall -1)/ 2 * (cell_edge_length + wall_thickness),
                            wall_thickness + (i - 1)/2 * (cell_edge_length + wall_thickness), cell_edge_length,
                            cell_edge_length))  ## Maze Background Color
                    col += 1

    if selected_y and selected_x: pygame.gfxdraw.box(screen, pygame.Rect(wall_thickness + (selected_y - 1) * (cell_edge_length + wall_thickness),wall_thickness + (selected_x - 1) * (cell_edge_length + wall_thickness),cell_edge_length,cell_edge_length), (200, 200, 200, 150))
        #pygame.draw.rect(screen, (200, 200, 200),pygame.Rect(wall_thickness + (selected_y - 1) * (cell_edge_length + wall_thickness),wall_thickness + (selected_x - 1) * (cell_edge_length + wall_thickness),cell_edge_length,cell_edge_length))  ## Maze Background Color

    pygame.draw.rect(screen, (100,0, 0), pygame.Rect(0, 0, wall_thickness, h_maze)) ## Red Frame
    pygame.draw.rect(screen, (100,0, 0), pygame.Rect(0, 0, w_maze, wall_thickness)) ## Red Frame
    pygame.draw.rect(screen, (100,0, 0), pygame.Rect(0, h_maze-wall_thickness, w_maze, wall_thickness)) ## Red Frame
    pygame.draw.rect(screen, (100,0, 0), pygame.Rect(w_maze-wall_thickness, 0, wall_thickness, h_maze)) ## Red Frame

    if starting_x != "-" and starting_y != "-":
        pygame.draw.rect(screen, (100, 200, 100), pygame.Rect(
            wall_thickness + (starting_y) * (cell_edge_length + wall_thickness),
            wall_thickness + (starting_x) * (cell_edge_length + wall_thickness), cell_edge_length,
            cell_edge_length))  ## Maze Background Color
        button1_text = 'Change Starting Point'
        starting_flag = True

        if not starting_flag: position[0], position[1] =starting_y - 1, starting_x - 1

    else:  button1_text = 'Choose Starting Point'

    if final_x != "-" and final_y != "-":
        pygame.draw.rect(screen, (100, 100, 200), pygame.Rect(
            wall_thickness + (final_y) * (cell_edge_length + wall_thickness),
            wall_thickness + (final_x) * (cell_edge_length + wall_thickness), cell_edge_length,
            cell_edge_length))  ## Maze Background Color
        button2_text = 'Change Finish Point'

    else:
        button2_text = 'Choose Finish Point'

    ## DRAWING MAZE ##

    ## DRAWING MAZE INFO BOX ##

    ##INFO BOXES FRAME
    pygame.draw.rect(screen, (100,0, 0), pygame.Rect(0, h_maze, wall_thickness, h_information)) ## Red Frame Information 1 Box Left
    pygame.draw.rect(screen, (100,0, 0), pygame.Rect(w_maze, 0, w_information2, wall_thickness)) ## Red Frame Information 1 Box Left
    pygame.draw.rect(screen, (100,0, 0), pygame.Rect(w_screen-wall_thickness, 0, wall_thickness, h_screen)) ## Red Frame Right
    pygame.draw.rect(screen, (100,0, 0), pygame.Rect(0, h_screen-wall_thickness, w_screen, wall_thickness)) ## Red Frame Bottom
    pygame.draw.rect(screen, (100,0, 0), pygame.Rect(0, h_maze-wall_thickness, w_screen, wall_thickness)) ## Red Frame Information Box Top
    ##INFO BOXES FRAME

    ## INFO BOX 1
    infobox1()
    ## INFO BOX 1

    ## INFO BOX 2
    infobox2()
    ## INFO BOX 2
    ## DRAWING MAZE INFO BOX ##


    if validation:

        if keys[0]:
            if direction == 0 and position[0] < mazesize[0] - 1 and int(maze_v2[2*(position[0]+1)][2*(position[1])+1]) == 0: position[0]+=1
            elif direction == 1 and position[1] < mazesize[1] - 1 and int(maze_v2[1+2*position[0]][2*(position[1]+1)]) == 0: position[1]+=1
            elif direction == -1 and position[1] > 0 and int(maze_v2[1+2*position[0]][2*(position[1])]) == 0: position[1]-=1
            elif (direction == -2 or direction == 2) and position[0] > 0 and int(maze_v2[2*(position[0])][2*(position[1])+1]) == 0: position[0]-=1

        if keys[1]:
            if (direction == -2 or direction == 2) and position[0] < mazesize[0] - 1 and int(maze_v2[2*(position[0]+1)][2*(position[1])+1]) == 0: position[0]+=1
            elif direction == -1 and position[1] < mazesize[1] - 1 and int(maze_v2[1+2*position[0]][2*(position[1]+1)]) == 0: position[1]+=1
            elif direction == 1 and position[1] > 0 and int(maze_v2[1+2*position[0]][2*(position[1])]) == 0: position[1]-=1
            elif direction == 0 and position[0] > 0 and int(maze_v2[2*(position[0])][2*(position[1])+1]) == 0: position[0]-=1

        if keys[2]:
            direction+=1
            if direction == 3: direction = -1
            elif direction == -3: direction = 1

        if keys[3]:
            direction-=1
            if direction == 3: direction = -1
            elif direction == -3: direction = 1

        validation = False

    if starting_flag: robotbody(position[0],position[1],direction)

    pygame.display.flip()
    
pygame.quit()