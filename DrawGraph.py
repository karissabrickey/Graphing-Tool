"""
    THIS FILE accompanies main.py in the Graphing-Tool directory.
    Instructions for use can be found in main.py.

Author: Karissa Brickey
7/16/2018
"""

# All imports and default pygame things go here. 
import pygame 

# Declare color constants.
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0 , 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

#----------------------------------------------------------------------------#
#    CLASS FOR LINES- ALLOWS USER TO ENTER LINE SPECIFICATIONS IN ANY ORDER
#----------------------------------------------------------------------------#
class Line:
    def __init__(self, points, linecolor = BLACK, linewidth = 1):
        self.points = points
        self.linecolor = linecolor
        self.linewidth = linewidth

        
#----------------------------------------------------------------------------#
#    CLASS FOR DRAWING SPECIFIED SECTIONS OF GRAPHS IN SELECTED REGIONS ON
#    THE SCREEN.
#----------------------------------------------------------------------------#
class Plot:
    def __init__(self, screen, source_rect, target_rect,
                 background_color = WHITE, border_color = BLACK,
                 border_width = 5, axis_on = True, axis_labels_on = True,
                 axis_label_color = BLACK, axis_ticks_on = True,
                 graph_title = '', axis_ticks_spacing = 10,
                 point_labels_on = True, point_label_color = BLACK,
                 circle_points = True):
        self.screen = screen
        self.source_rect = source_rect
        self.target_rect = target_rect
        self.graphs = []
        self.border_width = border_width
        self.axis_on = axis_on
        self.axis_labels_on = axis_labels_on
        self.axis_label_color = axis_label_color
        self.axis_ticks_on = axis_ticks_on
        self.graph_title = graph_title
        self.axis_ticks_spacing = axis_ticks_spacing
        self.point_labels_on = point_labels_on
        self.point_label_color = point_label_color
        self.circle_points = circle_points
        self.line_width = []
        self.colors = []
        self.colors.append(background_color)
        self.colors.append(border_color)

        # Determine scale factor for x and y axis (for scaling coordiantes to
        # keep proportions the same betweem source and target rectangles).
        self.scale_x = self.target_rect[2] / float(self.source_rect[2])
        self.scale_y = self.target_rect[3] / float(self.source_rect[3])

    # Allows user to add lines to the Plot object via the += opperator
    def __iadd__(self, Line):
        self.colors.append(Line.linecolor)
        self.line_width.append(Line.linewidth)
        self.graphs.append(Line.points)
        return self

    # Prints all information regarding coordinates, colors, and specifications
    # of lines to the console window for the user's convenience. 
    def print_stats(self):
        print ' '
        print 'Source rectangle dimensions (x, y, width, height):', self.source_rect
        print 'Target rectangle dimensions (x, y, width, height):', self.target_rect
        for i in range (0, len(self.graphs)):
            print 'Line', i, 'coordinates:', self.graphs[i]
            print 'Line', i, 'color:', self.colors[i + 2], '... linewidth:', self.line_width[i]
        for i in range (0, len(self.new_points)):
            print 'Adjusted coordinates for line', i, ':', self.new_points[i]
        for i in range (0, len(self.point_in_bounds)):
            print 'Point in line', i, 'drawn? (True = yes, False = no):', self.point_in_bounds[i]
        print ' '

    #------------------------- All drawing code below! -----------------------#
    def draw(self):
        
        # Create list to hold altered coordinates (shifted to remain
        # proportionally identical to original graph) 
        self.point_in_bounds = [[] for i in range (0, len(self.graphs))]

        # Create list to remember which coordinates were within the bounds of
        #the source rectangle.
        self.new_points = [[] for i in range (0, len(self.graphs))]

        # Draw background of the target rectangle (color is specified by user).
        pygame.draw.rect(self.screen, self.colors[0],
                        (self.target_rect[0], self.target_rect[1],
                         self.target_rect[2], self.target_rect[3]), 0)

        # Draw axis before any lines are drawn, if turned on.
        x_axis = 0; y_axis = 0;
        myfont = pygame.font.SysFont("monospace", 18)
        x_origin_label = str(self.source_rect[0])
        y_origin_label = str(self.source_rect[1])
        x_origin = myfont.render(x_origin_label, 1, (self.axis_label_color))
        y_origin = myfont.render(y_origin_label, 1, (self.axis_label_color))

        if self.axis_on:
            # Draw x axis (check to see if axis should be '0' or the x-value
            # of the source_rect's left-hand side)
            if self.source_rect[0] < 0:
                x_axis = (0 - self.source_rect[0]) * self.scale_x
                x_origin = myfont.render("0", 1, (self.axis_label_color))
                pygame.draw.line(self.screen, self.axis_label_color,
                             [x_axis + self.target_rect[0],
                              self.target_rect[1]],
                             [x_axis + self.target_rect[0],
                              self.target_rect[1] + self.target_rect[3]],
                             1)

            # Draw y axis (check to see if axis should be '0' or the y-value
            # of the source_rect's bottom side)
            if self.source_rect[1] < 0:
                y_axis = (0 - self.source_rect[1]) * self.scale_y
                y_origin = myfont.render("0", 1, (self.axis_label_color))
                pygame.draw.line(self.screen, self.axis_label_color,
                        [self.target_rect[0],
                         self.target_rect[1] + self.target_rect[3] - y_axis],
                        [self.target_rect[0] + self.target_rect[2],
                         self.target_rect[1] + self.target_rect[3] - y_axis],
                        1)

        # Draw axis labels if turned on.
        if self.axis_labels_on:
            x_pos = x_axis - 4; y_pos = y_axis + 8
            if not y_axis:
                y_pos = 10
            if not x_axis:
                x_pos = 0
            x_axis_label = myfont.render("x", 1, (self.axis_label_color))
            y_axis_label = myfont.render("y", 1, (self.axis_label_color))
            self.screen.blit(y_origin, (self.target_rect[0] - 15,
                            (self.target_rect[1] + self.target_rect[3] - y_pos)))
            self.screen.blit(x_origin, ((self.target_rect[0] + x_pos),
                            (self.target_rect[1] + self.target_rect[3]) + 5))
            self.screen.blit(x_axis_label,
                            ((self.target_rect[0] + self.target_rect[2] + 10),
                            (self.target_rect[1] + self.target_rect[3] - 13)))
            self.screen.blit(y_axis_label, (self.target_rect[0] - 4,
                            self.target_rect[1] - 27))

        # Draw title above graph if turned on (text specified by user).
        if self.graph_title:
            myfont1 = pygame.font.SysFont("monospace", 16)
            title = myfont1.render(self.graph_title, 1, (self.axis_label_color))
            r = title.get_rect()
            self.screen.blit(title, (self.target_rect[0] +
                            (self.target_rect[2] - r.w) / 2,
                            self.target_rect[1] + r.h * 0.5))

        # Draw all axis label ticks- both x and y tick marks MUST be multipled
        # by the x and y scale factors to keep spacing proportional.
        if self.axis_ticks_on:

            # Draw axis label ticks from x_axis to right side of target rect.
            for i in range(int(self.target_rect[0] + x_axis +
                        self.axis_ticks_spacing * self.scale_x),
                        self.target_rect[0] + self.target_rect[2],
                        int(self.axis_ticks_spacing * self.scale_x)):
                pygame.draw.line(self.screen, self.axis_label_color,
                   [i, self.target_rect[1] + self.target_rect[3] - y_axis],
                   [i, self.target_rect[1] + self.target_rect[3] - y_axis + 5],
                   1)

            # Draw axis label ticks from x_axis to left side of target rect.
            for i in range(int(self.target_rect[0] + x_axis -
                        self.axis_ticks_spacing * self.scale_x),
                        self.target_rect[0],
                        int(-self.axis_ticks_spacing * self.scale_x)):
                pygame.draw.line(self.screen, self.axis_label_color,
                   [i, self.target_rect[1] + self.target_rect[3] - y_axis],
                   [i, self.target_rect[1] + self.target_rect[3] - y_axis + 5],
                   1)

            # Draw axis label ticks from y_axis to top of target rect.
            for i in range(int(self.target_rect[1] + self.target_rect[3] -
                        y_axis - self.axis_ticks_spacing * self.scale_y),
                        self.target_rect[1],
                        int(-self.axis_ticks_spacing * self.scale_y)):
                pygame.draw.line(self.screen, self.axis_label_color,
                   [self.target_rect[0] + x_axis - 5, i],
                   [self.target_rect[0] + x_axis, i], 1)

            # Draw axis label ticks from y_axis to bottom of target rect.
            for i in range(int(self.target_rect[1] + self.target_rect[3] -
                        y_axis + self.axis_ticks_spacing * self.scale_y),
                        (self.target_rect[1] + self.target_rect[3]),
                        int(self.axis_ticks_spacing * self.scale_y)):
                pygame.draw.line(self.screen, self.axis_label_color,
                   [self.target_rect[0] + x_axis - 5, i],
                   [self.target_rect[0] + x_axis, i], 1)

        #---------------------------------------------------------------------#
        # Drawing of each individual graph is done here
        #---------------------------------------------------------------------#        
        for j in range (0, len(self.graphs)):
            for i in range(0, len(self.graphs[j])):

                # Scale the coordinates of each point to the dimensions of
                # target rectangle so proportions remain unchanged.
                # Then add the new coorddinate to new_points list. 
                self.new_points[j].append((self.graphs[j][i][0] *
                                          self.scale_x + x_axis,
                                           self.graphs[j][i][1] *
                                           self.scale_y + y_axis))
                
                # Determine which points on the graph need to be drawn i.e
                # are in the boundaries of the source rectangle.
                if ((self.graphs[j][i][0] >= self.source_rect[0] and
                     self.graphs[j][i][0] <=
                     self.source_rect[0] + self.source_rect[2])
                    and 
                    (self.graphs[j][i][1] >= self.source_rect[1] and
                     self.graphs[j][i][1] <=
                     self.source_rect[1] + self.source_rect[3])):

                    #------------ Draw the appropriate points -------------#

                    # Determine whether to draw circles around the points:
                    if self.circle_points:

                        # Determine appropriate radius for circle based on
                        # width of the line the point belongs to.
                        radius = 4
                        if self.line_width[j] > 4 and self.line_width[j] < 8:
                            radius = 5
                        elif self.line_width[j] >= 8:
                            radius = 6
                            
                        pygame.draw.circle(self.screen, self.colors[j + 2],
                            (int(self.new_points[j][i][0] + self.target_rect[0]),
                             int((self.target_rect[1] + self.target_rect[3]) -
                             self.new_points[j][i][1])),
                            radius, # radius of the circle
                            radius) # line width

                        # If not, draw the point as a single dot.
                    else:    
                        pygame.draw.line(self.screen, self.colors[j + 2],
                            [self.new_points[j][i][0] + self.target_rect[0],
                             (self.target_rect[1] + self.target_rect[3]) -
                              self.new_points[j][i][1]],
                            [self.new_points[j][i][0] + self.target_rect[0],
                             (self.target_rect[1] + self.target_rect[3]) -
                              self.new_points[j][i][1]],
                            1) # last number is the line width. 
  
                    # Reccord which points were drawn in the 'points_in_bounds'
                    # list.
                    self.point_in_bounds[j].append(True)
                else:
                    self.point_in_bounds[j].append(False)

        # Draw lines connecting each of the points that were drawn.
        for j in range (0, len(self.point_in_bounds)):
            for i in range (0, len(self.point_in_bounds[j])):

                if (i == len(self.point_in_bounds[j]) -1):
                    break
                if (self.point_in_bounds[j][i] and
                    self.point_in_bounds[j][i+1]):
                    pygame.draw.line(self.screen, self.colors[j + 2],
                        [self.new_points[j][i][0] + self.target_rect[0],
                         (self.target_rect[1] + self.target_rect[3]) -
                          self.new_points[j][i][1]],
                        [self.new_points[j][i+1][0] + self.target_rect[0] + 1,
                         (self.target_rect[1] + self.target_rect[3]) -
                          self.new_points[j][i+1][1]], self.line_width[j])

            # Draw point labels if on. 
            if self.point_labels_on:
                for j in range (0, len(self.new_points)):
                    for i in range (0, len(self.new_points[j])):

                        myfont = pygame.font.SysFont("Arial", 11)
                        label = myfont.render(str(self.graphs[j][i]), 1,
                                              (self.point_label_color))
                        self.screen.blit(label,
                                         (self.new_points[j][i][0] +
                                          self.target_rect[0] - 25,
                                          self.target_rect[1] +
                                          self.target_rect[3] -
                                          self.new_points[j][i][1] - 15))
                            
        # Draw the border of the target rectangle (color is 'colors[1]').
        pygame.draw.rect(self.screen, self.colors[1],
                         (self.target_rect[0], self.target_rect[1],
                          self.target_rect[2], self.target_rect[3]),
                          self.border_width)
        
#----------------------------------------------------------------------------#
# End of file
