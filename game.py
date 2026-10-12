import random

def save_score(name, result):
    f = open("scores.txt", "a")
    f.write(name + "," + result + "\n")
    f.close()

def clear():
    print("\033[2J\033[H")

board = [""] * 9

def show():
    print(board[0] or "1", "|", board[1] or "2", "|", board[2] or "3")
    print("--+---+--")
    print(board[3] or "4", "|", board[4] or "5", "|", board[5] or "6")
    print("--+---+--")
    print(board[6] or "7", "|", board[7] or "8", "|", board[8] or "9")

wins=[(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]

def win_check(bd, p):
    for a,b,c in wins:
        if bd[a] == p and bd[b] == p and bd[c] == p:
            return True
    return False

def play(mode, name):
    global board
    board = [""] * 9
    turn = "X"
    while True:
        clear()
        show()

        if mode == "2" and turn == "O":
            m = str(random.choice([i + 1 for i in range(9) if board[i] == ""]))
        else:
            m = input(turn + " pick from 1-9:")

        if not m.isdigit() or int(m) < 1 or int(m) > 9:
            print("Bad Input!")
            continue
        if board[int(m) - 1] != "":
            print("This board is taken!")
            continue
        board[int(m) - 1] = turn
        if win_check(board, turn):
            show()
            print(turn, "Wins!")
            save_score(name, turn + "Won")
            return
        if "" not in board:
            show()
            print("Draw!")
            save_score(name, "draw")
            return
        if turn == "X":
            turn = "O"
        else:
            turn = "X"
def main():
    clear()
    print("=== SSH TIC TAC TOE ===")
    name = input("Your Name: ")
    while True:
        mode = input("1 = Two players, 2 = Vs computer: ")
        play(mode, name)
        again = input("Play again? (y/n): ")
        if again !="y":
            break
    print("Bye!")

if __name__ == "__main__":
    main()