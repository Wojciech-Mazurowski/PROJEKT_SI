import pygame


class Piece:

    def __init__(self, color, pos_x, pos_y):
        self.color = color
        self.x = pos_x
        self.y = pos_y
        self.radius = game.board_size / 20
        self.rect = pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        self.drag = False
        self.offset_x = 0
        self.offset_y = 0

    def draw_piece(self):

        pygame.draw.circle(screen, self.color, (self.rect.x + self.radius, self.rect.y + self.radius), self.radius)

    def dragging(self):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    self.drag = True
                    mouse_x, mouse_y = event.pos
                    self.offset_x = self.rect.x - mouse_x
                    self.offset_y = self.rect.y - mouse_y
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.drag:
                    temp_pos = snap((self.rect.x, self.rect.y))
                    self.rect.x = temp_pos[0]
                    self.rect.y = temp_pos[1]
                self.drag = False
        elif event.type == pygame.MOUSEMOTION:
            if self.drag:
                mouse_x, mouse_y = event.pos
                self.rect.x = mouse_x + self.offset_x
                self.rect.y = mouse_y + self.offset_y