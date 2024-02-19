from triangle import Triangle, getCenter, makeTriangle, drawTriangle, offsetTriangle, setTrianglePos, rotateTriangle
import pygame
from vector2d import Vector2D


class DrawableTriangle:

    def __init__(self, scale, internalAngle, rotation, pos=(0,0)) -> None:
        self.tri: Triangle = makeTriangle(scale, internalAngle, rotation)
        setTrianglePos(self.tri, pos)
        self.direction = rotation

    def set_pos(self, pos: (int)):
        setTrianglePos(self.tri, pos)

    def set_direction(self, direction):
        self.direction = direction

    def draw(self, window, color=(255, 255, 255), debug=False):
        drawTriangle(window, self.tri, color, debug)
    
    def rotate_to_angle(self, target_angle, x_diff=0):
        # Rotates the triangle to the target angle
        if x_diff > 0:
            target_angle -= 90
            diff = self.direction - target_angle
            self.direction = target_angle
            rotateTriangle(self.tri, -diff)
        elif x_diff < 0:
            target_angle += 90
            diff = self.direction - target_angle
            self.direction = target_angle
            rotateTriangle(self.tri, -diff)



# used for testing
if __name__ == "__main__":
    pygame.init()
    window = pygame.display.set_mode((800, 600))
    running = True

    my_font = pygame.font.SysFont('Comic Sans MS', 30)

    dt = DrawableTriangle(50, 60, 0, (400, 300))
    while running:
        window.fill((31, 31, 31))
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        mouse_pos = pygame.mouse.get_pos()
        mouse_vec = Vector2D(mouse_pos[0], mouse_pos[1])
        center = getCenter(dt.tri)
        center_vec = Vector2D(center[0], center[1])
        
        angle_between = center_vec.get_angle_between(mouse_vec)
        direction = center_vec.look_at(mouse_vec).get_angle()
        dt.rotate_to_angle(direction, center_vec.x - mouse_vec.x)

        t1_surface = my_font.render(f"Triangle angle: {(dt.direction+90) % 360}°", False, (0, 0, 0))
        t2_surface = my_font.render(f"Target angle: {(direction+90) % 360}°", False, (0, 0, 0))
        t3_surface = my_font.render(f"Angle between: {angle_between}°", False, (0, 0, 0))
        window.blit(t1_surface, (0, 0))
        window.blit(t2_surface, (0, 30))
        window.blit(t3_surface, (0, 60))
       
        dt.draw(window, (230,230,230), True)
    


        pygame.display.flip()
    pygame.quit()