import anytree
from copy import deepcopy
import math

def grid_to_two_dimensions(grid):
    temp_matrix = [['n' for i in range(5)] for j in range(5)]
    for i in range(5):
        for j in range(5):
            temp_matrix[i][j] = grid[i * 5 + j]
    return temp_matrix

def modify_Piece(data, piece):
    piece.color = data[0]
    piece.i = data[1]
    piece.j = data[2]
    piece.on_board = data[3]
    piece.drag = data[4]

def find_tigers(grid):
    Tigers = []
    for pos in range(len(grid)):
        if grid[pos] == "b":
            i = math.floor(pos / 5)
            j = pos % 5
            Tigers.append(((0,0,0), i, j, True, False)) #Color, x, y, on_board, drag
    if len(Tigers) < 2:
        Tigers = []
        Tigers.append(((0, 0, 0), -1, -1, False, False)) #Color, x, y, on_board, drag
    return Tigers

def find_goats( grid, no_goats):
    Goats = []
    for pos in range(len(grid)):
        if grid[pos] == "w":
            i = math.floor(pos / 5)
            j = pos % 5
            Goats.append(((200, 200, 200), i, j, True, False)) #Color, x, y, on_board, drag
    if len(Goats) < no_goats:
        Goats = []
        Goats.append(((200, 200, 200), -1, -1, False, False)) #Color, x, y, on_board, drag
    return Goats

def evaluate(Grid, test_piece, turn_counter, no_goat):
    score =  (18 - no_goat) * 10
    Tigers = find_tigers(Grid)
    for Tiger in Tigers:
        modify_Piece(Tiger, test_piece)
        test_piece.update_moves(grid_to_two_dimensions(Grid), turn_counter)
        for move in test_piece.possible_moves:
            if len(move) > 4:
                score += 10
            score += 1
    return score



def make_tree(curr_grid, test_piece, depth, goatNum, curr_turn):
    Root = anytree.Node("root", grid=deepcopy(curr_grid), grid_matrix= grid_to_two_dimensions(curr_grid), no_goats=deepcopy(goatNum))
    ChildNum = 0
    turn_counter = deepcopy(curr_turn)
    Tigers = find_tigers(Root.grid)
    Goats = find_goats(Root.grid, Root.no_goats)


    isBlack = False
    for times in range(depth):
        for node in anytree.findall(Root, filter_=lambda node: node.is_leaf):
            if node.is_leaf:
                if node.no_goats < 17:
                    if node.no_goats < 16:
                        print()
                Tigers = find_tigers(node.grid)
                Goats = find_goats(node.grid, node.no_goats)

                if (isBlack):
                    for Tiger in Tigers:
                        modify_Piece(Tiger, test_piece)
                        test_piece.update_moves(grid_to_two_dimensions(node.grid), turn_counter)
                        for move in test_piece.possible_moves:
                            if len(move) > 4:
                                new_no_goats = node.no_goats - 1
                            else:
                                new_no_goats = deepcopy(node.no_goats)

                            temp_grid = deepcopy(node.grid)
                            if test_piece.update_grid(temp_grid, move):
                                anytree.Node("Child" + str(ChildNum),grid=deepcopy(temp_grid), move_done= move, no_goats=deepcopy(new_no_goats),
                                             turn= turn_counter, value = evaluate(temp_grid, deepcopy(test_piece), turn_counter, new_no_goats), parent=node)
                                ChildNum += 1


                else:
                    for Goat in Goats:
                        modify_Piece(Goat, test_piece)
                        test_piece.update_moves(grid_to_two_dimensions(node.grid), turn_counter)
                        for move in test_piece.possible_moves:
                            temp_grid = deepcopy(node.grid)
                            if test_piece.update_grid(temp_grid, move):
                                anytree.Node("Child" + str(ChildNum), grid=deepcopy(temp_grid), move_done=move, no_goats=deepcopy(node.no_goats),
                                             turn=turn_counter, value=evaluate(temp_grid, deepcopy(test_piece), turn_counter, node.no_goats), parent=node)
                                ChildNum += 1
        turn_counter += 1
        #pool = multiprocessing.Pool(processes=6)
        #pool.starmap(node_processing, args)
        #pool.close()
        #pool.join()

        if isBlack == True :
            isBlack = False
        else :
            isBlack = True
    return Root

def alphabeta(node, depth, alpha, beta, maximizer):  # na start alpha = -inf, beta = inf
    if depth == 0 or node.is_leaf:
        return node
    elif maximizer:
        maxEva = -math.inf
        for child in node.children:
            temp_node = minmax(child, depth - 1, False)
            if maxEva < temp_node.value:
                maxEva = temp_node.value
                best_node = temp_node
            alpha = max(maxEva,alpha)
            if beta <= alpha:
                break
        return best_node
    else:
        minEva = math.inf
        for child in node.children:
            temp_node = minmax(child, depth - 1, True)
            if minEva > temp_node.value:
                minEva = temp_node.value
                best_node = temp_node
            beta = min(minEva,beta)
            if beta <= alpha:
                break
        return best_node

def minmax(node, depth, maximizer):
    if depth == 0 or node.is_leaf:
        return node
    elif maximizer:
        maxEva = -math.inf
        for child in node.children:
            temp_node = minmax(child, depth - 1, False)
            if maxEva < temp_node.value:
                maxEva = temp_node.value
                best_node = temp_node
        return best_node
    else:
        minEva = math.inf
        for child in node.children:
            temp_node = minmax(child, depth - 1, True)
            if minEva > temp_node.value:
                minEva = temp_node.value
                best_node = temp_node
        return best_node