import pygame
import random
pygame.font.init()

# create window
WIDTH = 600
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Tic Tac Toe")

# set fonts
WINNER_FONT = pygame.font.SysFont('comicsans', 40, bold=False, italic=False)
CHOOSE_PLAYER_FONT = pygame.font.SysFont('comicsans', 20, bold=False, italic=False)

# rgb color values
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

# load (local) image files
X_image = pygame.image.load('X.png')
O_image = pygame.image.load('O.png')

# stores a range of positions for each square of the tic tac toe grid
board_positions = [
    (range(0, 200), range(0, 200)),
    (range(200, 400), range(0, 200)),
    (range(400, 600), range(0, 200)),
    (range(0, 200), range(200, 400)),
    (range(200, 400), range(200, 400)),
    (range(400, 600), range(200, 400)),
    (range(0, 200), range(400, 600)),
    (range(200, 400), range(400, 600)),
    (range(400, 600), range(400, 600))
]

# stores the positions of where each character (either X or O) will be drawn
char_positions = [
    (75, 75),
    (250, 75),
    (425, 75),
    (75, 250),
    (250, 250),
    (425, 250),
    (75, 450),
    (250, 450),
    (425, 450)
]

# draws the grid, and draws all of the moves based off of the board variable
def create_board(board):
    pygame.draw.line(WIN, BLACK, (200, 50), (200, 550), 2)
    pygame.draw.line(WIN, BLACK, (400, 50), (400, 550), 2)
    pygame.draw.line(WIN, BLACK, (50, 200), (550, 200), 2)
    pygame.draw.line(WIN, BLACK, (50, 400), (550, 400), 2)
    for i in range(9):
        if board[i] == 'X':
            WIN.blit(X_image, char_positions[i])
        elif board[i] == 'O':
            WIN.blit(O_image, char_positions[i])

# returns a list of all possible moves, used for the minimax algorithm
def possibleMoves(board):
    tempList = []
    for i in range(9):
        if board[i] == ' ':
            tempList.append(i)
    return tempList

# minimax algorithm
# uses recursion to go through each possible branch of moves
# evaluates each move
# evaluation is based off a minimizing player and a maximizing player
# a winning move for the minimizing player (O in this case) will be negative, and vice versa for the maximizing player (X)
def minimax(board, maximizingPlayer, depth, alpha, beta):
    childBoard = board.copy()

    if checkwin(board) == 1: 
        return 10 - depth
    if checkwin(board) == -1: 
        return -10 + depth
    if len(possibleMoves(board)) == 0: 
        return 0
    
    if maximizingPlayer:
        bestEval = -1000
        for i in (possibleMoves(board)):
            childBoard[i] = 'X'
            eval = minimax(childBoard, False, depth + 1, alpha, beta)
            childBoard = board.copy()
            bestEval = max(eval, bestEval)
            alpha = max(alpha, bestEval)
            if beta <= alpha:
                break
        return bestEval
    else:
        bestEval = 1000
        for i in (possibleMoves(board)):
            childBoard[i] = 'O'
            eval = minimax(childBoard, True, depth + 1, alpha, beta)
            childBoard = board.copy()
            bestEval = min(bestEval, eval)
            beta = min(beta, bestEval)
            if beta <= alpha:
                break
        return bestEval

# finds the best move for either the maximizing player or the minimizing player
# uses the minimax algorithm to evaluate each possible move, and makes a list of the best moves
# returns a random move from the best moves list
def findBestMove(board, player):
    maxEval = -100
    minEval = 100
    alpha = -100
    beta = 100
    bestMoves = []
    childBoard = board.copy()

    if player == 'X':
        maximizingPlayer = True
    elif player == 'O':
        maximizingPlayer = False

    if maximizingPlayer:
        for i in (possibleMoves(board)):
            childBoard[i] = 'X'
            eval = minimax(childBoard, 0, False, alpha, beta)
            childBoard = board.copy()
            if eval > maxEval:
                maxEval = eval
                bestMove = i
        for i in possibleMoves(board):
            childBoard = board.copy()
            childBoard[i] = 'X'
            eval = minimax(childBoard, 0, False, alpha, beta)
            if eval == maxEval:
                bestMoves.append(i)
        return bestMoves[random.randrange(len(bestMoves))]
    else:
        for i in (possibleMoves(board)):
            childBoard[i] = 'O'
            eval = minimax(childBoard, 1, True, alpha, beta)
            childBoard = board.copy()
            if eval < minEval:
                minEval = eval
                bestMove = i
        for i in possibleMoves(board):
            childBoard = board.copy()
            childBoard[i] = 'O'
            eval = minimax(childBoard, 1, True, alpha, beta)
            if eval == minEval:
                bestMoves.append(i)
        return bestMoves[random.randrange(len(bestMoves))] 

# returns 1 if X won, and -1 if O won
def checkwin(board):
    # Horizontal win positions
    if board[0] == 'X' and board[1] == 'X' and board[2] == 'X': return 1
    if board[0] == 'O' and board[1] == 'O' and board[2] == 'O': return -1

    if board[3] == 'X' and board[4] == 'X' and board[5] == 'X': return 1
    if board[3] == 'O' and board[4] == 'O' and board[5] == 'O': return -1

    if board[6] == 'X' and board[7] == 'X' and board[8] == 'X': return 1
    if board[6] == 'O' and board[7] == 'O' and board[8] == 'O': return -1

    # Vertical win positions
    if board[0] == 'X' and board[3] == 'X' and board[6] == 'X': return 1
    if board[0] == 'O' and board[3] == 'O' and board[6] == 'O': return -1

    if board[1] == 'X' and board[4] == 'X' and board[7] == 'X': return 1
    if board[1] == 'O' and board[4] == 'O' and board[7] == 'O': return -1

    if board[2] == 'X' and board[5] == 'X' and board[8] == 'X': return 1
    if board[2] == 'O' and board[5] == 'O' and board[8] == 'O': return -1

    # Diagonal win positions
    if board[0] == 'X' and board[4] == 'X' and board[8] == 'X': return 1
    if board[0] == 'O' and board[4] == 'O' and board[8] == 'O': return -1

    if board[2] == 'X' and board[4] == 'X' and board[6] == 'X': return 1
    if board[2] == 'O' and board[4] == 'O' and board[6] == 'O': return -1

    return 0

# draws "player goes first" and "computer goes first" to the screen
def draw_choices(choice1, choice2):
    WIN.fill(WHITE)
    draw_choice1 = CHOOSE_PLAYER_FONT.render(choice1, 1, (0, 0, 0))
    draw_choice2 = CHOOSE_PLAYER_FONT.render(choice2, 1, (0, 0, 0))

    WIN.blit(draw_choice1, (WIDTH // 3 - draw_choice1.get_width() // 3, WIDTH // 2 - draw_choice1.get_height()))
    WIN.blit(draw_choice2, (2 * WIDTH // 3 - draw_choice2.get_height() // 3, WIDTH // 2 - draw_choice2.get_height()))
    pygame.display.update()

    return (pygame.Rect(WIDTH // 3 - draw_choice1.get_width() // 3, WIDTH // 2 - draw_choice1.get_height(), draw_choice1.get_width(), draw_choice1.get_height()), pygame.Rect(2 * WIDTH // 3 - draw_choice2.get_width() // 3, WIDTH // 2 - draw_choice2.get_height(), draw_choice2.get_width(), draw_choice2.get_height()))

def main():
    board = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
    run = True
    
    # these variables store which player is which
    # for example, if computer is X, then the computer will store 'X'
    computer = ''
    player = ''
    
    # X goes first, so the turn variable is initially X
    turn = 'X'

    choice1, choice2 = draw_choices("Player Goes First", "Computer Goes First")
    
    # manages the events for the start screen
    while computer == '':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    if choice1.collidepoint(pygame.mouse.get_pos()):
                        computer = 'O'
                        player = 'X'
                    elif choice2.collidepoint(pygame.mouse.get_pos()):
                        computer = 'X'
                        player = 'O'
    
    # game loop
    while run:
        WIN.fill(WHITE)
        create_board(board)
        pygame.display.update()

        # if it is the computers turn, computer's move is the best move, and then it's the players turn
        # the delay makes it a bit more natural
        if turn == computer:
            move = findBestMove(board, turn)
            board[move] = turn
            turn = player
            pygame.time.delay(200)

        # manage events
        # if the user clicks one of the squares, that square will be passed on as the move, and the turn will alternate
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(len(board_positions)):
                    if player == turn:
                        if pygame.mouse.get_pos()[0] in board_positions[i][0] and pygame.mouse.get_pos()[1] in board_positions[i][1]:
                            if i in possibleMoves(board):
                                board[i] = player
                                turn = computer
        
        # check to see if the game is over
        # if it is, display the winner and restart the game
        if checkwin(board):
            if player == 'X':
                player = 'O'
            else:
                player = 'X'

            create_board(board)
            winner_text = WINNER_FONT.render("Player {} wins!".format(player), 1, (255, 0, 0))
            WIN.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, WIDTH // 2 - winner_text.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(2000)
            main()
        elif not len(possibleMoves(board)):
            create_board(board)
            winner_text = WINNER_FONT.render("Draw!".format(player), 1, (255, 0, 0))
            WIN.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, WIDTH // 2 - winner_text.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(2000)
            create_board(board)
            main()
    
    # if the user exits out, then run will be set to false, the game loop will end, and the window will be closed
    pygame.quit()

# make sure that the main function will only run if the program isn't being imported
if __name__ == "__main__":
    main()