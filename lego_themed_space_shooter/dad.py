
import pygame.draw

X = 0
Y = 1

#
#  point_between()
#
#  Return the coordinates of the point <percentage> way along the line between p1,p2
#
def point_between(p1, p2, percent):
    return (p1[X] + (p2[X]-p1[X]) * percent,
            p1[Y] + (p2[Y]-p1[Y]) * percent)

#
# draw_line_segment()
#
# Draw part of the line between p1,p2 defined by the start and end percentages
# e.g. if start_perecent = 0.5 would start halfway bewteen the points
#
def draw_line_segment(screen, p1, p2, start_percent, end_percent, width):
    pygame.draw.line(screen.surface,
                     (0,255,0),
                     point_between(p1, p2, start_percent),
                     point_between(p1, p2, end_percent),
                     width = width)


def draw_laser(screen, start, end, step):

  start_percent = (  0,    0,  0.5, 0.75, 0.87, 0.93)  # start points along line (%)
  end_percent =   (0.5, 0.75, 0.87, 0.93, 0.96,    1)  # end points along line (%)

  step -= 1
  if step >= 0 and step < len(start_percent):
    draw_line_segment(screen, (start[X]-3, start[Y]), end, start_percent[step], end_percent[step], 3)
    draw_line_segment(screen,  start,                 end, start_percent[step], end_percent[step], 3)
    draw_line_segment(screen, (start[X]+3, start[Y]), end, start_percent[step], end_percent[step], 3)



