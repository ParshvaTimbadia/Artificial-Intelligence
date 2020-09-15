
1. Implement genetic algorithm in Python for creating a list of N numbers that equal X when s squared and summed together. 




2.In this part, you’ll program a minimax module for the board game Othello, also known as Reversi. The main module that you’ll program will calculate the value for a given board position. But, code is also provided for you that will let you play against your AI if you like.

Provided files: othello.py (stub), clearBestMove.txt, clearBestCounterMove.txt, arbitraryBoard5.txt, arbitraryBoard8.txt, board1.txt, endgame.txt

The rules of Othello are as follows:
a)The two player colors are white and black. The white player goes first.
b)You capture an opponent’s pieces when they lie in a straight line between a piece you already had on the board and a piece you just played. (A straight line is left-right, up-down, or a 45 degree diagonal.)
c)You can only play a piece that would capture at least one piece. If you have no legal moves, the turn is passed.
d)The game is over when neither player has any legal moves left. Whoever controls the most pieces on the board at that point wins.

Something that is slightly unusual about Othello for minimax is the fact that a turn might be skipped if a player has no legal plays. You’ll have to take that into account in your minimax calculations. (Don’t have skipped turns count against the search depth.)

The AI is always presumed to be white for this assignment; if you try the demo mode, you as the human will be playing black.

The input will be the search depth on a single line, followed by an ASCII representation of the board (W for white, B for black, - for an empty space).

A)Download the provided othello.py code.
B)Implement basic depth-limited minimax for the minimax_value function, ignoring the alpha and beta arguments for now. Your evaluation function, when you bottom out, should just be the difference in piece count between white and black if it's not the end of the game, or WIN_VAL, -WIN_VAL, or 0 if it is the end of the game. You should be able to effectively use a depth of 5 or so without waiting too long.
Tip: While debugging, you’ll find it useful for minimax to print the board state it is evaluating and the value that it assigns to that board. Also, debug small depths before attempting larger ones.




C)Try running on the following boards that have a search depth of 5 or less: 	clearBestMove.txt: Value should be 2.
 clearBestCounterMove.txt: Value should be -3. arbitraryBoard5.txt: Value should be 1.

You can feed a text file to a program with input redirection:

python3 othello.py < clearBestMove.txt

D)Implement alpha-beta pruning.
E)Check that you still get the same values on the files from part C.

Your code should now run in a reasonable amount of time on arbitraryBoard8.txt, board1.txt, and endgame.txt.
