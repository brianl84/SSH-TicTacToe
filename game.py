board = [""] * 9

def show():
    print(board[0], "  |", board[1], " |", board[2])
    print("---+---+---")
    print(board[3], "  |", board[4], " |", board[5])
    print("---+---+---")
    print(board[6], "  |", board[7], " |", board[8])

turn = "X"
while True:
    show()
    m = input(turn + " pick from 1-9:")
    board[int(m) - 1] = turn
if turn == "X":
    turn = "O"
else:
    turn = "X"