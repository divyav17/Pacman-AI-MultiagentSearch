import sys

playerO = "O"
playerX = "X"
ticTakToeGameState = ["O","O","X","X",4,"O",6,7,"X"]


def getOpenSpotFromBoard(board):
    openSpot = []
    for spots in board:
        if spots is not "X" and spots is not "O":
            openSpot = openSpot + [spots]
    return openSpot


def checkWinCondition(board, player):
    if ((board[0] is player and board[1] is player and board[2] is player)
        or
        (board[3] is player and board[4] is player and board[5] is player)
        or
        (board[6] is player and board[7] is player and board[8] is player)
        or
        (board[0] is player and board[3] is player and board[6] is player)
        or
        (board[1] is player and board[4] is player and board[7] is player)
        or
        (board[2] is player and board[5] is player and board[8] is player)
        or
        (board[0] is player and board[4] is player and board[8] is player)
        or
        (board[2] is player and board[4] is player and board[6] is player)):
        return True
    else:
        return False


def Utility(board, openSpots):
    if (checkWinCondition(board, playerO)):
        return -1
    elif checkWinCondition(board, playerX):
        return  1
    elif (len(openSpots) == 0):
        return  0
    else:
        return None

def minimax(board, currentTurn):

    getOpenSpots = getOpenSpotFromBoard(board)
    value = Utility(board, getOpenSpots)
    if (value is not None):
        return {"utilityScore" : value}

    moves = []

    for spots in getOpenSpots:
        move = {}
        move["index"] = spots
        board[spots] = currentTurn
        if currentTurn is playerX:
            res = minimax(board, playerO)
            move["utilityScore"] = res["utilityScore"]
        else:
            res = minimax(board,playerX)
            move["utilityScore"] = res["utilityScore"]

        board[spots] = move["index"]
        moves = moves + [move.copy()]
    bestMove =0
    if (currentTurn is playerX):
        bestScore = -sys.maxint - 1
        i =-1
        for move in moves:
            i+=1
            if (move["utilityScore"] > bestScore):
                bestScore = move["utilityScore"]
                bestMove = i
    else:
        bestScore = sys.maxint
        i = -1
        for move in moves:
            i+=1
            if(move["utilityScore"] < bestScore):
                bestScore = move["utilityScore"]
                bestMove = i;
    return moves[bestMove]



def testcase():
    # Check for given game state in Q2(a) (Check for player wins)
    print("The Best Possible Move for problem given in Q2(a) Game State")
    ticTakToeGameState = ["O", "O", "X", "X", 4, "O", 6, 7, "X"]
    bestSpot = minimax(ticTakToeGameState, playerX)
    print("THe index to be placed and  utility utilityScore is")
    print(bestSpot)
    print("+++++++++++++++++++++++++++++++++++++++++++++++++")
    # Check for Player draws
    print("The Best Possible Move for consiering draw state")
    # O has moved optimally hence best outcome for X is draw
    ticTakToeGameState = ["O", 1, "O", "X", 4, 5, 6, 7, "X"]
    bestSpot = minimax(ticTakToeGameState, playerX)
    print("THe index to be placed and  utility utilityScore is" )
    print(bestSpot)

    print("+++++++++++++++++++++++++++++++++++++++++++++++++")
    # Game has not ended yet.
    print("Checking function for Utility")
    ticTakToeGameState = ["O", "O", "X", "X", 4, "O", 6, 7, "X"]

    result = Utility(ticTakToeGameState, [4,6,7])
    if result is None:
        print("Utility is successful in indentifying that the bord is not at a terminal state")
    else:
        print("Utility func failed.")

    print("+++++++++++++++++++++++++++++++++++++++++++++++++")
    # Ramdom game state check
    print("Considering both play optimally from the start")
    # O has moved optimally hence best outcome for X is draw
    ticTakToeGameState = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    bestSpot = minimax(ticTakToeGameState, playerX)
    print("THe index to be placed and  utility utilityScore is")
    print(bestSpot)


testcase()