import pygame
import math
import TreeMaker_Test
import time
import threading
import anytree

pygame.init()  # init pygame
running = True  # for turning of the game


class Game:
    def __init__(self):
        self.turn = 'b'
        self.turn_counter = 0
        for j in range(5):
            for i in range(5):
                self.current_board.append('n')

    width = 1200
    height = 900
    # board size must be divided by 6
    board_size = 800
    piece_size = board_size / 20
    block_size = board_size / 5
    black = (0, 0, 0)  # color for later use
    gray = (90, 90, 90)  # ^
    white_piece = (200, 200, 200)
    lewy_gorny_x = width / 2 - 2 * block_size
    lewy_gorny_y = height / 2 - 2 * block_size
    lewy_dolny_x = width / 2 - 2 * block_size
    lewy_dolny_y = 2 * block_size + height / 2
    prawy_gorny_x = block_size + width / 2 + block_size
    prawy_gorny_y = block_size + height / 2 - (3 * block_size)
    prawy_dolny_x = (2 * block_size + width / 2)
    prawy_dolny_y = (2 * block_size + height / 2)
    current_board = []
    current_board_matrix = [['n' for i in range(5)] for j in range(5)]
    win_condition = 0
    goatNum = 18

    def change_turn(self):
        self.turn_counter += 1
        if self.turn == 'b':
            self.turn = 'w'
        else:
            self.turn = 'b'

    def board_to_two_dimensions(self):
        for i in range(5):
            for j in range(5):
                self.current_board_matrix[i][j] = self.current_board[i * 5 + j]

    def check_rules(self, color, pos, onboard):

        piece_index = index_from_position(pos)
        # turns one and two (black initializing two pieces in row)
        if self.turn_counter < 2:
            if color == 'b' and self.current_board[piece_index] == 'n':
                self.turn_counter += 1
                if self.turn_counter == 2:
                    self.turn = 'w'
                self.board_to_two_dimensions()
                return True
        else:  # rest of the turns (black and white alternating)
            if self.turn == 'w':
                if game.turn_counter < 38:
                    if color == "w" and self.current_board[index_from_position(pos)] == 'n' and onboard is False:
                        self.board_to_two_dimensions()
                        self.change_turn()
                else:
                    if color == "w" and self.current_board[index_from_position(pos)] == 'n':
                        self.board_to_two_dimensions()
                        self.change_turn()
                return True

            else:
                if color == "b" and self.turn_counter > 1 and self.current_board[index_from_position(pos)] == 'n':
                    self.board_to_two_dimensions()
                    self.change_turn()
                    return True

        self.board_to_two_dimensions()
        return False

    def goat_AI(self):
        while True:
            if self.win_condition > 0:  # checks if game has ended
                return
            if self.turn == 'w':  # checks if its his turn
                # print(self.current_board)
                Root = TreeMaker_Test.make_tree(self.current_board, Piece((0, 0, 0), -1, -1), 4, self.goatNum,
                                                self.turn_counter)
                best_alpha = TreeMaker_Test.alphabeta(Root, 4, -math.inf, math.inf, False)
                # print(best_alpha)  # TESTING
                move = best_alpha.ancestors[1].move_done
                goatNum = best_alpha.ancestors[1].no_goats
                for Goat in Goat_Pieces:
                    if Goat.i == move[0] and Goat.j == move[1]:
                        Goat.make_a_move(self.current_board, move)
                        break
                if self.turn_counter > 40:
                    print(anytree.RenderTree(Root))
            else:
                time.sleep(5)


game = Game()
# Set up the drawing window with w and h
screen = pygame.display.set_mode([game.width, game.height])
pygame.display.set_caption('Main Tapal Empat')

pozycje = []
for j in range(5):
    for i in range(5):
        pozycje.append([game.lewy_gorny_x + i * game.block_size, game.lewy_gorny_y + j * game.block_size])


def dist_between_two_points(x1, y1, x2, y2):
    return math.hypot(x2 - x1, y2 - y1)


def highlight_pos(pos):
    for x in pos:
        i = x[2] * 5 + x[3]
        pygame.draw.circle(screen, (72, 184, 0), [pozycje[i][0], pozycje[i][1]], game.board_size / 80)


def draw_playground():
    for y in range(4):
        for x in range(4):
            rect = pygame.Rect(x * game.block_size + game.width / 2 - (2 * game.block_size),
                               y * game.block_size + game.height / 2 - (2 * game.block_size),
                               game.block_size, game.block_size)
            pygame.draw.rect(screen, game.gray, rect, 4)

    # drawing diagonal
    pygame.draw.line(screen, game.gray,
                     (game.lewy_gorny_x, game.lewy_gorny_y),
                     (game.prawy_dolny_x,
                      game.prawy_dolny_y), 4)

    # drawing second diagonal
    pygame.draw.line(screen, game.gray,
                     (game.prawy_gorny_x, game.prawy_gorny_y),
                     (game.lewy_dolny_x, game.lewy_dolny_y
                      ), 4)

    # drawing big rect :D
    pygame.draw.line(screen, game.gray,
                     (game.lewy_gorny_x + (game.prawy_gorny_x - game.lewy_gorny_x) / 2, game.lewy_gorny_y),
                     (game.lewy_gorny_x, game.lewy_gorny_y + (game.lewy_dolny_y - game.lewy_gorny_y) / 2), 4)
    pygame.draw.line(screen, game.gray,
                     (game.lewy_gorny_x + (game.prawy_gorny_x - game.lewy_gorny_x) / 2, game.lewy_gorny_y),
                     (game.prawy_gorny_x, game.prawy_gorny_y + (game.prawy_dolny_y - game.prawy_gorny_y) / 2), 4)
    pygame.draw.line(screen, game.gray,
                     (game.lewy_gorny_x, game.lewy_gorny_y + (game.lewy_dolny_y - game.lewy_gorny_y) / 2),
                     (game.lewy_dolny_x + (game.prawy_dolny_x - game.lewy_dolny_x) / 2, game.lewy_dolny_y), 4)
    pygame.draw.line(screen, game.gray,
                     (game.prawy_gorny_x, game.prawy_gorny_y + (game.prawy_dolny_y - game.prawy_gorny_y) / 2),
                     (game.lewy_dolny_x + (game.prawy_dolny_x - game.lewy_dolny_x) / 2, game.lewy_dolny_y), 4)

    # drawing circle in the middle
    pygame.draw.circle(screen, game.gray, screen.get_rect().center, game.board_size / 80)


def snap(pos):
    tmin = 1000000
    ans_x = 0
    ans_y = 1
    for p in pozycje:
        dist = dist_between_two_points(int(pos[0]), int(pos[1]), int(p[0]), int(p[1]))
        if dist < tmin:
            tmin = dist
            ans_x = p[0]
            ans_y = p[1]

    return ans_x - game.piece_size, ans_y - game.piece_size


def index_from_position(pos):
    for i in range(len(pozycje)):
        if pozycje[i][0] == pos[0] + game.piece_size and pozycje[i][1] == pos[1] + game.piece_size:
            return i
    return -1


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
        self.on_board = False
        self.possible_moves = []
        self.i = -1
        self.j = -1

    def is_capture(self, i, j):
        for move in self.possible_moves:
            if len(move) > 5:
                if move[4] == "C" and move[2] == i and move[3] == j:
                    return move
        return "N"

    def update_moves(self, grid_matrix, turn_counter):
        if self.get_color() == 'b':
            if turn_counter > 2:
                self.possible_moves = []
                # ruchy w lewo
                for j in range(self.j - 1, -1, -1):
                    if grid_matrix[self.i][j] == 'n':
                        self.possible_moves.append((self.i, self.j, self.i, j))
                    else:
                        break

                # ruchy w prawo
                for j in range(self.j + 1, 5):
                    if grid_matrix[self.i][j] == 'n':
                        self.possible_moves.append((self.i, self.j, self.i, j))
                    else:
                        break

                # ruch w góre
                for i in range(self.i + 1, 5):
                    if grid_matrix[i][self.j] == 'n':
                        self.possible_moves.append((self.i, self.j, i, self.j))
                    else:
                        break

                # ruchy w dół
                for i in range(self.i - 1, -1, -1):
                    if grid_matrix[i][self.j] == 'n':
                        self.possible_moves.append((self.i, self.j, i, self.j))
                    else:
                        break

                # ruchy w prawy dolny róg
                j = self.j
                if (self.i * 5 + self.j) % 2 == 0:
                    for i in range(self.i + 1, 5):
                        j += 1
                        if j > 4:
                            break
                        if grid_matrix[i][j] == 'n':
                            self.possible_moves.append((self.i, self.j, i, j))
                        else:
                            break

                # ruchy w prawy górny róg
                i = self.i
                if (self.i * 5 + self.j) % 2 == 0:
                    for j in range(self.j + 1, 5):
                        i -= 1
                        if i < 0:
                            break
                        if grid_matrix[i][j] == 'n':
                            self.possible_moves.append((self.i, self.j, i, j))
                        else:
                            break

                # ruchy w lewy dolny róg
                j = self.j
                if (self.i * 5 + self.j) % 2 == 0:
                    for i in range(self.i + 1, 5):
                        j -= 1
                        if j < 0:
                            break
                        if grid_matrix[i][j] == 'n':
                            self.possible_moves.append((self.i, self.j, i, j))
                        else:
                            break

                # ruchy w lewy górny róg
                j = self.j
                if (self.i * 5 + self.j) % 2 == 0:
                    for i in range(self.i - 1, -1, -1):
                        j -= 1
                        if j < 0:
                            break
                        if grid_matrix[i][j] == 'n':
                            self.possible_moves.append((self.i, self.j, i, j))
                        else:
                            break

                # BICIA OPONETNÓW w dół
                if self.i < 3:
                    if grid_matrix[self.i + 1][self.j] == 'w' and grid_matrix[self.i + 2][
                        self.j] == 'n':
                        self.possible_moves.append((self.i, self.j, self.i + 2, self.j, "C", self.i + 1, self.j))
                # BICIA OPONENTÓW W GÓRE:
                if self.i > 1:
                    if grid_matrix[self.i - 1][self.j] == 'w' and grid_matrix[self.i - 2][
                        self.j] == 'n':
                        self.possible_moves.append((self.i, self.j, self.i - 2, self.j, "C", self.i - 1, self.j))
                # left
                if self.j < 3:
                    if grid_matrix[self.i][self.j + 1] == 'w' and grid_matrix[self.i][
                        self.j + 2] == 'n':
                        self.possible_moves.append((self.i, self.j, self.i, self.j + 2, "C", self.i, self.j + 1))
                # right
                if self.j > 1:
                    if grid_matrix[self.i][self.j - 1] == 'w' and grid_matrix[self.i][
                        self.j - 2]=='n':
                        self.possible_moves.append((self.i, self.j, self.i, self.j - 2, "C", self.i, self.j - 1))

                # right down
                if (self.i * 5 + self.j) % 2 == 0:
                    if 3 > self.i and 3 > self.j:
                        if grid_matrix[self.i + 1][self.j + 1] == 'w' and \
                                grid_matrix[self.i + 2][self.j + 2] == 'n':
                            self.possible_moves.append(
                                (self.i, self.j, self.i + 2, self.j + 2, "C", self.i + 1, self.j + 1))

                # right up
                if (self.i * 5 + self.j) % 2 == 0:
                    if self.i > 1 and 3 > self.j:
                        if grid_matrix[self.i - 1][self.j + 1] == 'w' and \
                                grid_matrix[self.i - 2][self.j + 2] == 'n':
                            self.possible_moves.append(
                                (self.i, self.j, self.i - 2, self.j + 2, "C", self.i - 1, self.j + 1))

                # left down
                if (self.i * 5 + self.j) % 2 == 0:
                    if 3 > self.i and self.j > 1:
                        if grid_matrix[self.i + 1][self.j - 1] == 'w' and \
                                grid_matrix[self.i + 2][self.j - 2] == 'n':
                            self.possible_moves.append(
                                (self.i, self.j, self.i + 2, self.j - 2, "C", self.i + 1, self.j - 1))

                # left up
                if (self.i * 5 + self.j) % 2 == 0:
                    if self.i > 1 and self.j > 1:
                        if grid_matrix[self.i - 1][self.j - 1] == 'w' and \
                                grid_matrix[self.i - 2][self.j - 2] == 'n':
                            self.possible_moves.append(
                                (self.i, self.j, self.i - 2, self.j - 2, "C", self.i - 1, self.j - 1))

            elif turn_counter < 3 and self.on_board == 0:
                self.possible_moves = []
                for i in range(5):
                    for j in range(5):
                        if grid_matrix[i][j] == 'n':
                            self.possible_moves.append((self.i, self.j, i, j))
            else:
                self.possible_moves = []

        else:  # BIALE
            if turn_counter > 37:
                self.possible_moves = []
                # up
                if 4 > self.i:
                    if grid_matrix[self.i + 1][self.j] == 'n':
                        self.possible_moves.append((self.i, self.j, self.i + 1, self.j))
                # down
                if self.i > 0:
                    if grid_matrix[self.i - 1][self.j] == 'n':
                        self.possible_moves.append((self.i, self.j, self.i - 1, self.j))
                # left
                if 4 > self.j:
                    if grid_matrix[self.i][self.j + 1] == 'n':
                        self.possible_moves.append((self.i, self.j, self.i, self.j + 1))
                # right
                if self.j > 0:
                    if grid_matrix[self.i][self.j - 1] == 'n':
                        self.possible_moves.append((self.i, self.j, self.i, self.j - 1))
                # right down
                if (self.i * 5 + self.j) % 2 == 0:
                    if 4 > self.i and 4 > self.j:
                        if grid_matrix[self.i + 1][self.j + 1] == 'n':
                            self.possible_moves.append((self.i, self.j, self.i + 1, self.j + 1))

                # right up
                if (self.i * 5 + self.j) % 2 == 0:
                    if self.i > 0 and 4 > self.j:
                        if grid_matrix[self.i - 1][self.j + 1] == 'n':
                            self.possible_moves.append((self.i, self.j, self.i - 1, self.j + 1))

                # left down
                if (self.i * 5 + self.j) % 2 == 0:
                    if 4 > self.i and self.j > 0:
                        if grid_matrix[self.i + 1][self.j - 1] == 'n':
                            self.possible_moves.append((self.i, self.j, self.i + 1, self.j - 1))

                # left up
                if (self.i * 5 + self.j) % 2 == 0:
                    if self.i > 0 and self.j > 0:
                        if grid_matrix[self.i - 1][self.j - 1] == 'n':
                            self.possible_moves.append((self.i, self.j, self.i - 1, self.j - 1))
            elif turn_counter < 38 and self.on_board == 0:
                self.possible_moves = []
                for i in range(5):
                    for j in range(5):
                        if grid_matrix[i][j] == 'n':
                            self.possible_moves.append((self.i, self.j, i, j))
            else:
                self.possible_moves = []

    def draw_piece(self):

        pygame.draw.circle(screen, self.color, (self.rect.x + self.radius, self.rect.y + self.radius), self.radius)

    def dragging(self):

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos) and game.turn == self.get_color():
                    self.drag = True
                    print(self.possible_moves)
                    mouse_x, mouse_y = event.pos
                    self.offset_x = self.rect.x - mouse_x
                    self.offset_y = self.rect.y - mouse_y

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.drag:
                    temp_pos = snap((self.rect.x, self.rect.y))
                    if game.check_rules(color=self.get_color(), pos=temp_pos, onboard=self.on_board):
                        if game.current_board[index_from_position((self.x, self.y))] == 'b' or game.current_board[
                            index_from_position((self.x, self.y))] == 'w':
                            game.current_board[index_from_position((self.x, self.y))] = 'n'

                        game.current_board[index_from_position(temp_pos)] = self.get_color()
                        game.board_to_two_dimensions()
                        self.x = temp_pos[0]
                        self.y = temp_pos[1]
                        self.rect.x = temp_pos[0]
                        self.rect.y = temp_pos[1]
                        self.i = int(index_from_position(temp_pos) / 5)
                        self.j = int(index_from_position(temp_pos) % 5)
                        very_temp = self.is_capture(self.i, self.j)
                        if very_temp != "N":
                            game.current_board[very_temp[5] * 5 + very_temp[6]] = 'n'
                            game.board_to_two_dimensions()
                            for piece in Goat_Pieces:
                                if piece.i == very_temp[5] and piece.j == very_temp[6]:
                                    Goat_Pieces.remove(piece)
                                    game.goatNum -= 1
                                    break
                        counter = 0
                        for piece in Tiger_Pieces:
                            piece.update_moves(game.current_board_matrix, game.turn_counter)
                            if len(piece.possible_moves) == 0:
                                counter += 1

                        if counter == 2:
                            print("bialy wygral")
                            game.win_condition = 1

                        if len(Goat_Pieces) < 11:
                            print("czarny wygral")  # win condition
                            game.win_condition = 2
                        self.on_board = True

                        self.update_moves(game.current_board_matrix, game.turn_counter)
                    else:
                        self.rect.x = self.x
                        self.rect.y = self.y

                self.drag = False
        elif event.type == pygame.MOUSEMOTION:
            if self.drag:
                mouse_x, mouse_y = event.pos
                self.rect.x = mouse_x + self.offset_x
                self.rect.y = mouse_y + self.offset_y

    def get_color(self):
        if self.color == game.black:
            return 'b'
        else:
            return 'w'

    def make_a_move(self, grid, move):
        if len(move) > 4:
            piece_index = move[0] * 5 + move[1]
            target = move[2] * 5 + move[3]
            capture = move[5] * 5 + move[6]
            if grid[piece_index] == 'b' or grid[piece_index] == 'w' and piece_index >= 0:
                grid[piece_index] = 'n'  # swapping piece on grid
            grid[target] = self.get_color()  # ^
            grid[capture] = 'n'
            self.i = move[2]
            self.j = move[3]
            self.x = game.lewy_gorny_x + move[3] * Game.block_size - Game.piece_size
            self.y = game.lewy_gorny_y + move[2] * Game.block_size - Game.piece_size
            self.rect.x = game.lewy_gorny_x + move[3] * Game.block_size - Game.piece_size
            self.rect.y = game.lewy_gorny_y + move[2] * Game.block_size - Game.piece_size
            for piece in Goat_Pieces:
                if piece.i == move[5] and piece.j == move[6]:
                    Goat_Pieces.remove(piece)
                    break
            counter = 0

            game.board_to_two_dimensions()
            game.change_turn()

            for piece in Tiger_Pieces:
                piece.update_moves(game.current_board_matrix, game.turn_counter)
                if len(piece.possible_moves) == 0:
                    counter += 1
            if counter == 2:
                print("bialy wygral")
                game.win_condition = 1
            if len(Goat_Pieces) < 11:
                print("czarny wygral")  # win condition
                game.win_condition = 2
            self.on_board = True
            self.update_moves(game.current_board_matrix, game.turn_counter)
        else:
            piece_index = move[0] * 5 + move[1]
            target = move[2] * 5 + move[3]
            if grid[piece_index] == 'b' or grid[piece_index] == 'w' and piece_index >= 0:
                grid[piece_index] = 'n'  # swapping piece on grid
            grid[target] = self.get_color()  # ^
            self.i = move[2]
            self.j = move[3]
            self.x = game.lewy_gorny_x + move[3] * Game.block_size - Game.piece_size
            self.y = game.lewy_gorny_y + move[2] * Game.block_size - Game.piece_size
            self.rect.x = game.lewy_gorny_x + move[3] * Game.block_size - Game.piece_size
            self.rect.y = game.lewy_gorny_y + move[2] * Game.block_size - Game.piece_size
            counter = 0

            game.board_to_two_dimensions()
            game.change_turn()

            for piece in Tiger_Pieces:
                piece.update_moves(game.current_board_matrix, game.turn_counter)
                if len(piece.possible_moves) == 0:
                    counter += 1
            if counter == 2:
                print("bialy wygral")
                game.win_condition = 1
            if len(Goat_Pieces) < 11:
                print("czarny wygral")  # win condition
                game.win_condition = 2
            self.on_board = True
            self.update_moves(game.current_board_matrix, game.turn_counter)

    def update_grid(self, grid, move):
        piece_index = move[0] * 5 + move[1]
        target = move[2] * 5 + move[3]
        if grid[target] == 'b' or grid[target] == 'w':
            return False
        if grid[piece_index] == 'b' or grid[piece_index] == 'w' and piece_index >= 0:
            grid[piece_index] = 'n'  # swapping piece on grid
        grid[target] = self.get_color()  # ^
        if len(move) > 4:
            capture = move[5] * 5 + move[6]
            grid[capture] = 'n'
        return True


Goat_Pieces = []
Tiger_Pieces = []


def initialize():
    global Tiger_Pieces
    # init tiger pieces
    tiger1 = Piece(game.black, 100, game.board_size - 50)
    tiger2 = Piece(game.black, 200, game.board_size - 50)
    Tiger_Pieces = [tiger1, tiger2]
    # init goat pieces

    for x in range(9):
        goat = Piece(game.white_piece, game.prawy_gorny_x + game.board_size / 20 + 30, (x + 1) * 90)
        Goat_Pieces.append(goat)

    for x in range(9):
        goat = Piece(game.white_piece, game.prawy_gorny_x + game.board_size / 20 + 130, (x + 1) * 90)
        Goat_Pieces.append(goat)


initialize()
# print(anytree.RenderTree(TreeMaker.make_tree(game.current_board,game.current_board_matrix, Piece((0,0,0), -1, -1), 2), maxlevel=4))  # DRZEWO TEST
# needed_node = best_path.ancestors[0]
# print(needed_node)

if __name__ == '__main__':

    AI = threading.Thread(target=game.goat_AI)
    AI.start()

    while running:

        # event handle section

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # turning off the game
            for piece in Tiger_Pieces:
                piece.dragging()
            # for piece in Goat_Pieces:
            # piece.dragging()

        # drawing section
        screen.fill((255, 255, 255))

        draw_playground()

        for piece in Tiger_Pieces:
            piece.draw_piece()
            if piece.drag:
                piece.update_moves(game.current_board_matrix, game.turn_counter)
                highlight_pos(piece.possible_moves)
        for piece in Goat_Pieces:
            piece.draw_piece()
            if piece.drag:
                piece.update_moves(game.current_board_matrix, game.turn_counter)
                highlight_pos(piece.possible_moves)

        pygame.display.flip()

    pygame.quit()
