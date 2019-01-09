"""
    THIS PROGRAM requires the user to enter coordinate points of graphs,
    the section of this original graph they would like re-drawn (source_rect),
    and the dimensions of the rectangle they would like these points to be
    drawn in on the screen (target_rect).
    It THEN draws the new "chopped" graph to the screen inside the target
    rectangle. Various visual attributes may be specified regarding the final
    graph, including line widths and colors, labels, axis, and graph title. 

Author: Karissa Brickey
7/16/2018
"""

# All imports and default pygame things go here. 
import pygame
from DrawGraph import *
pygame.init()

# Set screen size and display the screen.
size = (600, 500)
screen = pygame.display.set_mode(size)

# Declare color constants.
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0 , 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Below are all parameters that may be specified when instantiating a
# Plot object (must use exact variable names):
"""
EXAMPLE:

background_color = WHITE
border_color = BLACK
border_width = 1
axis_on = True
axis_labels_on = True
axis_label_color = BLACK
axis_ticks_on = True
axis_ticks_spacing = 50
graph_title = "your text here"
point_labels_on = True
point_label_color = BLACK
circle_points = True
"""

#----------------------------------------------------------------------------#
#    MAIN EVENT LOOP:
#----------------------------------------------------------------------------#

# Lists of coordinate points representing different graphs belong here-
# line color and width may be specified.
# Syntax: (linecolor = ... linewidth = ... points = [(x,y),(x,y)...] )
line0 = Line(linecolor = RED, linewidth = 1,
             points = [(-10,-12), (0,0), (60,50), (95,35), (120,150)])
line1 = Line(linecolor = GREEN, linewidth = 1,
             points = [(-12, 35), (20,30), (60, 60), (90,90), (120,120),
             (140,140)])
line2 = Line(linecolor = YELLOW, linewidth = 1,
             points = [(60,-8), (70,10), (80,5), (100,30), (130,10), (150,50)])
line3 = Line(linecolor = BLUE, linewidth = 1,
             points = [(0,50), (50,100), (100,70), (145,10), (151,20)])
   
# The source rectangle specifies which of the coordinate points in the 'lines'
# created above should be drawn i.e. "puts a box" around the section of the
# graph the user would like to have drawn on the screen. 
source_x = -15; source_y = -15; source_width = 165; source_height = 165;
source_rect = [source_x, source_y, source_width, source_height]

# The target rectangle specifies the dimensions of the graph that will actually
# be drawn on the screen.
# NOTE the dimensions do NOT have to match those of the source rectagle- the
# graphs will be drawn proportionally to match any dimensions. 
target_x = 100; target_y = 50; target_width = 300; target_height = 400;
target_rect = [target_x, target_y, target_width, target_height]

count =  1 # To print the stats only once.
running = True
while(running):

    # End loop if X button is pressed. 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen i.e fill with a background color of the user's choice.
    screen.fill([186, 186, 186])

    # Create Plot object:
    graph1 = Plot(source_rect = source_rect, target_rect = target_rect,
                  background_color = WHITE, border_color = BLACK,
                  border_width = 1, axis_on = True, axis_labels_on = False,
                  axis_label_color = BLACK, axis_ticks_on = True,
                  axis_ticks_spacing = 10, graph_title = "GRAPH 1",
                  point_labels_on = False, point_label_color = BLACK,
                  circle_points = False, screen = screen)

    # Add each graph to the Plot object:
    graph1 += line0
    graph1 += line1
    graph1 += line2
    graph1 += line3
    
    # Call drawing funciton.
    graph1.draw()

    # Print out stats.
    if count == 1:
        graph1.print_stats(); count = 2;
    
    # Update the screen.
    pygame.display.flip()

# Close the window and end the program.
pygame.quit()

#----------------------------------------------------------------------------#
# End of file.
