import pygame
from math import sin, cos, pi, radians

#stores three points of the triangle
class Triangle:
    def __init__(self, p1, p2, p3):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

def makeTriangle(scale, internalAngle, rotation):
    #define the points in a uint space
    ia = (radians(internalAngle) * 2) - 1
    p1 = (0, -1)
    p2 = (cos(ia), sin(ia))
    p3 = (cos(ia) * -1, sin(ia))

    #rotate the points
    ra = radians(rotation)
    rp1x = p1[0] * cos(ra) - p1[1] * sin(ra)
    rp1y = p1[0] * sin(ra) + p1[1] * cos(ra)                 
    rp2x = p2[0] * cos(ra) - p2[1] * sin(ra)
    rp2y = p2[0] * sin(ra) + p2[1] * cos(ra)                        
    rp3x = p3[0] * cos(ra) - p3[1] * sin(ra)                         
    rp3y = p3[0] * sin(ra) + p3[1] * cos(ra)
    rp1 = ( rp1x, rp1y )
    rp2 = ( rp2x, rp2y )
    rp3 = ( rp3x, rp3y )

    #scale the points 
    sp1 = [rp1[0] * scale, rp1[1] * scale]
    sp2 = [rp2[0] * scale, rp2[1] * scale]
    sp3 = [rp3[0] * scale, rp3[1] * scale]
                    
    return Triangle(sp3, sp1, sp2)

def drawTriangle(window, tri, color=(255, 255, 255), debug=False):
    pygame.draw.polygon(window, color,
                        [tri.p1, tri.p2, tri.p3])
    
    #pygame.draw.line(window, color, tri.p1, tri.p2)
    #pygame.draw.line(window, color, tri.p2, tri.p3)
    #pygame.draw.line(window, color, tri.p3, tri.p1)
    if debug:
        pygame.draw.circle(window, (220,0,0), tri.p1, 4)
        pygame.draw.circle(window, (0,220,0), tri.p2, 4)
        pygame.draw.circle(window, (0,0,220), tri.p3, 4)
        pygame.draw.circle(window, (220,220,0), getCenter(tri), 4)
        

def offsetTriangle(triangle, offsetx, offsety):
    #print((offsetx, offsety))
    triangle.p1 = list(triangle.p1)
    triangle.p2 = list(triangle.p2)
    triangle.p3 = list(triangle.p3)
    triangle.p1[0] += offsetx;  triangle.p1[1] += offsety;
    triangle.p2[0] += offsetx;  triangle.p2[1] += offsety;
    triangle.p3[0] += offsetx;  triangle.p3[1] += offsety;
    triangle.p1 = tuple(triangle.p1)
    triangle.p2 = tuple(triangle.p2)
    triangle.p3 = tuple(triangle.p3)

def setTrianglePos(triangle, pos=(0,0)):
    offsetx = pos[0] - getCenter(triangle)[0]
    offsety = pos[1] - getCenter(triangle)[1]

    offsetTriangle(triangle, offsetx, offsety)


def rotateTriangle(tri, angle):
    ra = radians(angle)
    
    # Translates the triangle so the midpoint is at the origin
    (mx, my) = getCenter(tri)

    p1 = (tri.p1[0]-mx, tri.p1[1]-my)
    p2 = (tri.p2[0]-mx, tri.p2[1]-my)
    p3 = (tri.p3[0]-mx, tri.p3[1]-my)

    rp1x = p1[0] * cos(ra) - p1[1] * sin(ra)
    rp1y = p1[0] * sin(ra) + p1[1] * cos(ra)                 
    rp2x = p2[0] * cos(ra) - p2[1] * sin(ra)
    rp2y = p2[0] * sin(ra) + p2[1] * cos(ra)                        
    rp3x = p3[0] * cos(ra) - p3[1] * sin(ra)                         
    rp3y = p3[0] * sin(ra) + p3[1] * cos(ra)

    # Translate back to original point
    rp1 = ( rp1x+mx, rp1y+my )
    rp2 = ( rp2x+mx, rp2y+my )
    rp3 = ( rp3x+mx, rp3y+my )
    tri.p1 = rp1
    tri.p2 = rp2
    tri.p3 = rp3

def getCenter(tri):
    m1_x = (tri.p1[0] + tri.p3[0]) / 2
    m1_y = (tri.p1[1] + tri.p3[1]) / 2

    m2_x = (m1_x + tri.p2[0]) / 2
    m2_y = (m1_y + tri.p2[1]) / 2  
    return (m2_x, m2_y)

# Used for testing
if __name__ == "__main__":
    triangle = makeTriangle(100, 60, 0)
    offsetTriangle(triangle, 200, 200)

    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    clock = pygame.time.Clock()

    running = True
    while running:
        screen.fill((31,31,31))
        clock.tick(60)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False;
            
        drawTriangle(screen, triangle, (200,200,200))
        #rotateTriangle(triangle, -1)
        pygame.display.update()

    pygame.quit()

