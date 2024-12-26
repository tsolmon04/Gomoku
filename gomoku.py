def is_empty(board):
    return all(element == " " for row in board for element in row)


def is_free(board, y, x):
    return on_board(y, x, board) and board[y][x] == " "


def on_edge(board , y, x):
    if(y == 0  or x == 0  or y == len(board) -1  or x == len(board[0]) - 1 ):
        return True
    else:
        return False


def get_start(y_end , x_end , d_y , d_x , length):
    y_start = y_end - (d_y * (length - 1))
    x_start = x_end - (d_x * (length - 1))
    return y_start , x_start


def is_bounded(board, y_end, x_end, length, d_y, d_x):
    y_start, x_start = get_start(y_end, x_end, d_y, d_x, length)
    y_start -= d_y  # Move one step back from the start
    x_start -= d_x  # Move one step back from the start
    count = 0
    if is_free(board, y_start, x_start):
        count += 1
    if is_free(board, y_end + d_y, x_end + d_x):
        count += 1
    if count == 0:
        return "CLOSED"
    elif count == 1:
        return "SEMIOPEN"
    else:
        return "OPEN"


def on_board(y,x,board):
    return (0 <= y < len(board)  and 0 <= x < len(board[0]))


def is_colour(board , col , y_start, x_start, length, d_y, d_x ) :
    for i in range(length):
        if(board[y_start + (i*d_y)][x_start + (i*d_x)] != col) :
            return False
    if(on_board(y_start - d_y  , x_start - d_x  , board)):
        if(board[y_start - d_y][x_start - d_x] == col):
            return False
    if(on_board(y_start + (d_y*length)  , x_start + (d_x*length) , board)):
        if(board[y_start + (d_y*length)][x_start + (d_x*length)] == col):
            return False
    return True


def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    open_seq_count = 0
    semi_open_seq_count = 0
    if not on_edge(board, y_start, x_start) and not on_edge(board, y_start + (length - 1) * d_y, x_start + (length - 1) * d_x):
        return 0, 0
    while on_board(y_start, x_start, board):
        end_y = y_start + (length - 1) * d_y
        end_x = x_start + (length - 1) * d_x
        if not on_board(end_y, end_x, board):
            break
        if is_colour(board, col, y_start, x_start, length, d_y, d_x):
            boundedness = is_bounded(board, end_y, end_x, length, d_y, d_x)
            if boundedness == "OPEN":
                open_seq_count += 1
            elif boundedness == "SEMIOPEN":
                semi_open_seq_count += 1
        y_start += d_y
        x_start += d_x
    return open_seq_count, semi_open_seq_count


def detect_rows(board, col, length):
    open_seq_count, semi_open_seq_count = 0, 0
    for y in range(len(board)):
        for x in range(len(board[0])):
            if y == 0 or x == 0:
                counts = detect_row(board, col, y, x, length, 1, 0)
                open_seq_count += counts[0]
                semi_open_seq_count += counts[1]
                counts = detect_row(board, col, y, x, length, 0, 1)
                open_seq_count += counts[0]
                semi_open_seq_count += counts[1]
                counts = detect_row(board, col, y, x, length, 1, 1)
                open_seq_count += counts[0]
                semi_open_seq_count += counts[1]
            if y == len(board) - 1 or x == 0:
                counts = detect_row(board, col, y, x, length, -1, 1)
                open_seq_count += counts[0]
                semi_open_seq_count += counts[1]
    return open_seq_count, semi_open_seq_count


def free_moves(board):
    free = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            if(board[i][j] == " "):
                m = i , j
                free.append(m)
    return free


def copy_2D(board):
  out = []
  for r in board:
    row = []
    for e in r:
      row.append(e)
    out.append(row)
  return out


def search_max(board):
    max_move = None
    max_score = -float('inf')
    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] == " ":
                board[y][x] = "b"
                score_for_move = score(board)
                if score_for_move > max_score:
                    max_score = score_for_move
                    max_move = (y, x)
                board[y][x] = " "
    return max_move if max_move is not None else (0, 0)


def score(board):
    MAX_SCORE = 100000
    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}
    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)
    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE
    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE
    return (-10000 * (open_w[4] + semi_open_w[4])+
            500  * open_b[4]                     +
            50   * semi_open_b[4]                +
            -100  * open_w[3]                    +
            -30   * semi_open_w[3]               +
            50   * open_b[3]                     +
            10   * semi_open_b[3]                +
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])


def is_win(board):
    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] != " ":
                color = "Black" if board[y][x] == "b" else "White"
                for d_y, d_x in [(0, 1), (1, 0), (1, 1), (-1, 1), (0, -1), (-1, -1), (-1, 0), (1, -1)]:
                    if check_win_in_direction(board, y, x, d_y, d_x, board[y][x], 5):
                        return f"{color} won"
    if not any(" " in row for row in board):
        return "Draw"
    return "Continue playing"


def check_win_in_direction(board, y, x, d_y, d_x, player, length):
    consecutive_count = 0
    for step in range(length):
        new_y, new_x = y + step * d_y, x + step * d_x
        if not on_board(new_y, new_x, board) or board[new_y][new_x] != player:
            return False
        consecutive_count += 1
    return consecutive_count == length


def print_board(board):
    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"
    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1])
        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"
    print(s)


def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board


def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))


def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])
    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)
        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)
        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            print(game_res)
            return game_res
        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            print(game_res)
            return game_res



def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        if on_board(y, x, board):
            board[y][x] = col
            y += d_y
            x += d_x
        else:
            break

if __name__ == '__main__':
    play_gomoku(8)


def test_is_empty():
    board  = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")


def test_is_bounded():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)

    y_end = 3
    x_end = 5

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")


def test_detect_row():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_row(board, "w", 0,x,length,d_y,d_x) == (1,0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")

def test_detect_rows():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_rows(board, col,length) == (1,0):
        print("TEST CASE for detect_rows PASSED")
    else:
        print("TEST CASE for detect_rows FAILED")

def test_search_max():
    board = make_empty_board(8)
    x = 5; y = 0; d_x = 0; d_y = 1; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6; y = 0; d_x = 0; d_y = 1; length = 4; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    if search_max(board) == (4,6):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")

def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()

def some_tests():
    board = make_empty_board(8)

    board[0][5] = "w"
    board[0][6] = "b"
    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)

    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0

    y = 3; x = 5; d_x = -1; d_y = 1; length = 2

    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)

    # Expected output:
    #        *0|1|2|3|4|5|6|7*
    #        0 | | | | |w|b| *
    #        1 | | | | | | | *
    #        2 | | | | | | | *
    #        3 | | | | |b| | *
    #        4 | | | |b| | | *
    #        5 | |w| | | | | *
    #        6 | |w| | | | | *
    #        7 | |w| | | | | *
    #        *****************
    #
    #         Black stones:
    #         Open rows of length 2: 1
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 0
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #         White stones:
    #         Open rows of length 2: 0
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 1
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #

    y = 5; x = 3; d_x = -1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b");
    print_board(board);
    analysis(board);

    #        Expected output:
    #           *0|1|2|3|4|5|6|7*
    #           0 | | | | |w|b| *
    #           1 | | | | | | | *
    #           2 | | | | | | | *
    #           3 | | | | |b| | *
    #           4 | | | |b| | | *
    #           5 | |w|b| | | | *
    #           6 | |w| | | | | *
    #           7 | |w| | | | | *
    #           *****************
    #
    #
    #        Black stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0
    #        White stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0