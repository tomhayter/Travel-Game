import pygame
from util.font import write_string

class Camera:
    def __init__(self, current_pos):
        self.current_pos = current_pos

    def update_camera_loc(self, key_down, map_size, res):
        match key_down:
            case pygame.K_UP | pygame.K_w:
                self.current_pos = (self.current_pos[0], self.current_pos[1]+10)
            case pygame.K_DOWN | pygame.K_s:
                self.current_pos = (self.current_pos[0], self.current_pos[1]-10)
            case pygame.K_LEFT | pygame.K_a:
                self.current_pos = (self.current_pos[0]+10, self.current_pos[1])
            case pygame.K_RIGHT | pygame.K_d:
                self.current_pos = (self.current_pos[0]-10, self.current_pos[1])

        if self.current_pos[0] > 0:
            self.current_pos = (0, self.current_pos[1])
        if self.current_pos[0] < -1 * (map_size[0] - res[0]):
            self.current_pos = (-1 * (map_size[0] - res[0]), self.current_pos[1])
        if self.current_pos[1] > 0:
            self.current_pos = (self.current_pos[0], 0)
        if self.current_pos[1] < -1 * (map_size[1] - res[1]):
            self.current_pos = (self.current_pos[0], -1 * (map_size[1] - res[1]))
        return self.current_pos
    
    def display(self, screen, item, loc):
        screen.blit(item, (loc[0]+self.current_pos[0], loc[1]+self.current_pos[1]))

    def get_img_rect(self, img, loc):
        return img.get_rect(x=loc[0]+self.current_pos[0], y=loc[1]+self.current_pos[1])
    
    def draw_line(self, screen, colour, start, end, thickness):
        new_start = (self.current_pos[0]+start[0], self.current_pos[1]+start[1])
        new_end = (self.current_pos[0]+end[0], self.current_pos[1]+end[1])
        pygame.draw.line(screen, colour, new_start, new_end, thickness)

    def write_string(self, screen, string, loc):
        write_string(screen, string, loc[0]+self.current_pos[0], loc[1]+self.current_pos[1])