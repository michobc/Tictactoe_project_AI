from cmath import inf
import random
import pygame as pg
import sys 

WINDOW_SIZE = 700
CELL_SIZE = WINDOW_SIZE // 3
vec2 = pg.math.Vector2
CELL_CENTER = vec2(CELL_SIZE / 2)

# functions---------------:
#scale the image to match window size
def getScaledImage(path, res):
        img = pg.image.load(path)
        return pg.transform.smoothscale(img, res)

def checkWhichMarkWon(mark, board):
    if (board[0][0] == board[0][1] and board[0][0] == board[0][2] and board[0][0] == mark):
        return True
    elif (board[1][0] == board[1][1] and board[1][0] == board[1][2] and board[1][0] == mark):
        return True
    elif (board[2][0] == board[2][1] and board[2][0] == board[2][2] and board[2][0] == mark):
        return True
    elif (board[0][0] == board[1][0] and board[0][0] == board[2][0] and board[0][0] == mark):
        return True
    elif (board[0][1] == board[1][1] and board[0][1] == board[2][1] and board[0][1] == mark):
        return True
    elif (board[0][2] == board[1][2] and board[0][2] == board[2][2] and board[0][2] == mark):
        return True
    elif (board[0][0] == board[1][1] and board[0][0] == board[2][2] and board[0][0] == mark):
        return True
    elif (board[0][2] == board[1][1] and board[0][2] == board[2][0] and board[0][2] == mark):
        return True
    else:
        return False
    
#boolean value to test if the state is terminated
def isTerminalState(board):
    for i in range(0,3):
        for j in range(0,3):
            if board[i][j] == ' ':
                return False
    return True

# eval function = lines where X(or O) can win - lines where O(or X) can win
def checkVertical(board, play, opp):
    i=0
    res = 0
    while i<=2:
        countPlay = 0
        countOpp = 0
        countEmty = 0
        j = 0
        while j<=2:
            if board[j][i] == play:
                countPlay += 1
            else:
                if board[j][i] == opp:
                    countOpp += 1
                else:
                    countEmty += 1
            j += 1
        if countPlay == 1 and countEmty == 2:
            res += 1
        else:
            if countPlay == 2 and countEmty == 1:
                res += 1
            else:
                if countOpp == 1 and countEmty == 2:
                    res += -1
                else:
                    if countOpp == 2 and countEmty == 1:
                        res += -1
        i += 1
    return res

def checkHorizontal(board, play, opp):
    i=0
    res = 0
    while i<=2:
        countPlay = 0
        countOpp = 0
        countEmty = 0
        j = 0
        while j<=2:
            if board[i][j] == play:
                countPlay += 1
            else:
                if board[i][j] == opp:
                    countOpp += 1
                else:
                    countEmty += 1
            j += 1
        if countPlay == 1 and countEmty == 2:
            res += 1
        else:
            if countPlay == 2 and countEmty == 1:
                res += 1
            else:
                if countOpp == 1 and countEmty == 2:
                    res += -1
                else:
                    if countOpp == 2 and countEmty == 1:
                        res += -1
        i += 1
    return res

def checkDiagonal(board, play, opp):
    res = 0
    i = 0
    j = 0
    countPlay = 0
    countOpp = 0
    countEmty = 0
    while i<=2 and j<=2:
        if board[i][j] == play:
            countPlay += 1
        else:
            if board[i][j] == opp:
                countOpp += 1
            else:
                countEmty += 1
        j += 1
        i += 1
    if countPlay == 1 and countEmty == 2:
        res += 1
    else:
        if countPlay == 2 and countEmty == 1:
            res += 1
        else:
            if countOpp == 1 and countEmty == 2:
                res += -1
            else:
                if countOpp == 2 and countEmty == 1:
                    res += -1

    i=0
    j=2
    countPlay = 0
    countOpp = 0
    countEmty = 0
    while i<=2 and j>=0:
        if board[i][j] == play:
            countPlay += 1
        else:
            if board[i][j] == opp:
                countOpp += 1
            else:
                countEmty += 1
        j -= 1
        i += 1
    if countPlay == 1 and countEmty == 2:
        res += 1
    else:
        if countPlay == 2 and countEmty == 1:
            res += 1
        else:
            if countOpp == 1 and countEmty == 2:
                res += -1
            else:
                if countOpp == 2 and countEmty == 1:
                    res += -1
 
    return res

# Eval function
def checkAll(board, play, opp):
    return checkVertical(board, play, opp)+ checkHorizontal(board, play, opp) + checkDiagonal(board, play, opp)

# Welcome class___________:
class Welcome:
    def __init__(self, game):
        self.game = game
         # Load and scale the image
        self.background_image = getScaledImage("./images/back.jpeg", [WINDOW_SIZE]*2)
        self.font = pg.font.Font(None, 36)
        self.text = self.font.render("Choose your symbol (X or O):", True, 'black', 'white')
        self.text_rect = self.text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2 - 50))
        self.x_button = pg.Rect(WINDOW_SIZE // 4, WINDOW_SIZE // 2, 50, 50)
        self.o_button = pg.Rect(3 * WINDOW_SIZE // 4 - 50, WINDOW_SIZE // 2, 50, 50)

        # Add difficulty buttons
        self.easy_button = pg.Rect(WINDOW_SIZE // 4, WINDOW_SIZE // 2 + 100, 100, 50)
        self.medium_button = pg.Rect(WINDOW_SIZE // 2 - 50, WINDOW_SIZE // 2 + 100, 100, 50)
        self.hard_button = pg.Rect(3 * WINDOW_SIZE // 4 - 100, WINDOW_SIZE // 2 + 100, 100, 50)

        # Add transparency for buttons
        self.easy_alpha = 0
        self.medium_alpha = 255
        self.hard_alpha = 255

    def draw(self):
        self.game.screen.fill((255, 255, 255))
        self.game.screen.blit(self.background_image, (0, 0))
        self.game.screen.blit(self.text, self.text_rect)
        pg.draw.rect(self.game.screen, 'blue', self.x_button)
        pg.draw.rect(self.game.screen, 'red', self.o_button)

        pg.draw.rect(self.game.screen, (255, 255, self.easy_alpha), self.easy_button)
        pg.draw.rect(self.game.screen, (255, 255, self.medium_alpha), self.medium_button)
        pg.draw.rect(self.game.screen, (255, 255, self.hard_alpha), self.hard_button)
        
        self.game.screen.blit(self.font.render("X", True, 'black'), (self.x_button.x + 17, self.x_button.y + 15))
        self.game.screen.blit(self.font.render("O", True, 'black'), (self.o_button.x + 17, self.o_button.y + 15))
        self.game.screen.blit(self.font.render("Easy", True, 'black'), (self.easy_button.x + 20, self.easy_button.y + 15))
        self.game.screen.blit(self.font.render("Medium", True, 'black'), (self.medium_button.x + 8, self.medium_button.y + 15))
        self.game.screen.blit(self.font.render("Hard", True, 'black'), (self.hard_button.x + 20, self.hard_button.y + 15))

    def handle_events(self, event):
        # Check if the mouse is over a button and set the cursor accordingly
        if event.type == pg.MOUSEMOTION:
            if self.x_button.collidepoint(pg.mouse.get_pos()):
                pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
            elif self.o_button.collidepoint(pg.mouse.get_pos()):
                pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
            elif self.easy_button.collidepoint(pg.mouse.get_pos()):
                pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
            elif self.medium_button.collidepoint(pg.mouse.get_pos()):
                pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
            elif self.hard_button.collidepoint(pg.mouse.get_pos()):
                pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
            else:
                pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)

        
        if event.type == pg.MOUSEBUTTONUP:
            if self.x_button.collidepoint(pg.mouse.get_pos()):
                self.game.tictactoe.depth = 3
                self.game.tictactoe.player = 'X'
                self.game.tictactoe.bot = 'O'
                self.game.tictactoe.turn = self.game.tictactoe.player

            elif self.o_button.collidepoint(pg.mouse.get_pos()):
                self.game.tictactoe.depth = 2
                self.game.tictactoe.player = 'O'
                self.game.tictactoe.bot = 'X'
                self.game.tictactoe.turn = self.game.tictactoe.bot

            # Set the difficulty level   
            elif self.easy_button.collidepoint(pg.mouse.get_pos()):
                self.game.tictactoe.difficulty = 'easy'
                self.easy_alpha = 0
                self.medium_alpha = 255
                self.hard_alpha = 255

            elif self.medium_button.collidepoint(pg.mouse.get_pos()):
                self.game.tictactoe.difficulty = 'medium'
                self.medium_alpha = 0
                self.easy_alpha = 255
                self.hard_alpha = 255

            elif self.hard_button.collidepoint(pg.mouse.get_pos()):
                self.game.tictactoe.difficulty = 'hard'
                self.hard_alpha = 0
                self.medium_alpha = 255
                self.easy_alpha = 255

# TicTacToe class---------------:
class TicTacToe:
    def __init__(self, game):
        self.game = game
        self.game.screen.fill((255, 255, 255))  # Fill the screen with a white background
        self.gridImage = getScaledImage("./images/grid.webp", [WINDOW_SIZE]*2) #size must be a list (longueur et largeur)
        self.oImage = getScaledImage("./images/O3.png", [CELL_SIZE]*2)
        self.xImage = getScaledImage("./images/X3.png", [CELL_SIZE]*2)

        self.gameState = [[' ', ' ', ' '],
                          [' ', ' ', ' '],
                          [' ', ' ', ' ']]
        
        self.player = ' '
        self.bot = ''
        self.turn = ''
        self.winner = None
        self.depth = 3
        self.difficulty = 'easy'

    #draw the initial grid on the window
    def draw(self):
        self.game.screen.fill((255, 255, 255)) 
        self.game.screen.blit(self.gridImage, (0,0))
        self.draw_objects()

    def run_game_process(self):
        if self.turn == self.player:
            current_cell = vec2(pg.mouse.get_pos()) // CELL_SIZE
            col, row = map(int, current_cell)
            left_click = pg.mouse.get_pressed()[0]

            if left_click and self.gameState[row][col] == ' ' and self.winner is None:
                self.gameState[row][col] = self.player

                if checkWhichMarkWon(self.player, self.gameState):
                    self.winner = self.player
                
                elif isTerminalState(self.gameState):
                    self.winner = 'z'

                else: self.turn = self.bot

        elif self.turn == self.bot:
            if self.difficulty == 'hard':
                best_move = self.find_best_move(self.gameState)
            elif self.difficulty == 'easy':
                best_move = self.find_random_move(self.gameState)
            elif self.difficulty == 'medium':
                best_move = self.find_medium_move(self.gameState, 0)

            self.gameState[best_move[0]][best_move[1]] = self.bot
            if checkWhichMarkWon(self.bot, self.gameState):
                self.winner = self.bot

            elif isTerminalState(self.gameState):
                self.winner = 'z' #anything != 'X' or 'O' to draw the message on the screen
                
            self.turn = self.player

    def find_random_move(self, board):
        random_move = None
        i = random.randint(0,2)
        j = random.randint(0,2)
        while board[i][j] != ' ':
            i = random.randint(0,2)
            j = random.randint(0,2)

        random_move = (i,j)
        return random_move
    
    #use minimax algo to find the best move (bot)
    def find_best_move(self, board):
        best_score = -2
        best_move = None
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = self.bot
                    score = self.value(board, self.player, -inf, inf)
                    board[i][j] = ' '
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        return best_move
    
    def find_medium_move(self, board, current_depth):
        best_score = -inf
        best_move = None
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = self.bot
                    score = self.value_medium(board, self.player, current_depth+1, -inf, inf)
                    board[i][j] = ' '
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        return best_move
            
    #draw X or O on the cell clicked
    def draw_objects(self):
        for y, row in enumerate(self.gameState):
            for x, obj in enumerate(row):
                if obj == self.player:
                    if self.player == 'O' :
                        self.game.screen.blit(self.oImage, vec2(x, y) * CELL_SIZE)
                    else:
                        self.game.screen.blit(self.xImage, vec2(x, y) * CELL_SIZE)
                elif obj == self.bot:
                    if self.bot == 'O':
                        self.game.screen.blit(self.oImage, vec2(x, y) * CELL_SIZE)
                    else:
                        self.game.screen.blit(self.xImage, vec2(x, y) * CELL_SIZE)

    def run(self):
        self.draw()
        self.run_game_process()


    def value_medium(self, board, nextAgent, current_depth, alpha, beta):
        if current_depth < self.depth :
            if checkWhichMarkWon(self.bot, board):  # Bot wins
                return 1
            elif checkWhichMarkWon(self.player, board):  # Player wins
                return -1
            elif isTerminalState(board):  # Draw
                return 0
            
            if nextAgent == self.bot: 
                return self.max_value_medium(board, current_depth, alpha, beta)
            else:  
                return self.min_value_medium(board, current_depth, alpha, beta)
        
        else:
            if current_depth == self.depth:
                if self.turn == self.bot:
                    return checkAll(board, self.bot, self.player)
                else:
                    return checkAll(board, self.player, self.bot)
                
    def max_value_medium(self, board, current_depth, alpha, beta): # X for bot
        v = -2
        for i in range(0,3):
            for j in range(0,3):
                if board[i][j] == ' ':
                    board[i][j] = self.bot
                    v = max(v, self.value_medium(board, self.player, current_depth+1, alpha, beta))
                    board[i][j] = ' '  # Revert the move
                    if v > beta:
                        return v
                    alpha = max(alpha,v)
        return v

    def min_value_medium(self, board, current_depth, alpha, beta): # O for player
        v = 2
        for i in range(0,3):
            for j in range(0,3):
                if board[i][j] == ' ':
                    board[i][j] = self.player
                    v = min(v, self.value_medium(board, self.bot, current_depth+1, alpha, beta))
                    board[i][j] = ' '  # Revert the move
                    if v < alpha:
                        return v
                    beta = min(beta, v)
        return v

# Minimax implementation with Dispatch----------------------:
    def value(self, board, nextAgent, alpha, beta):
        if checkWhichMarkWon(self.bot, board):  # Bot wins
            return 1
        elif checkWhichMarkWon(self.player, board):  # Player wins
            return -1
        elif isTerminalState(board):  # Draw
            return 0
        
        if nextAgent == self.bot:  
            return self.max_value(board, alpha, beta)
        else:  
            return self.min_value(board, alpha, beta)
        


    def max_value(self, board, alpha, beta): # X for bot
        v = -2
        for i in range(0,3):
            for j in range(0,3):
                if board[i][j] == ' ':
                    board[i][j] = self.bot
                    v = max(v, self.value(board, self.player, alpha, beta))
                    board[i][j] = ' '  # Revert the move
                    if v > beta:
                        return v
                    alpha = max(alpha,v)
        return v

    def min_value(self, board, alpha, beta): # O for player
        v = 2
        for i in range(0,3):
            for j in range(0,3):
                if board[i][j] == ' ':
                    board[i][j] = self.player
                    v = min(v, self.value(board, self.bot, alpha, beta))
                    board[i][j] = ' '  # Revert the move
                    if v < alpha:
                        return v
                    beta = min(beta, v)
        return v

# Game class---------------:
class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode([WINDOW_SIZE]*2) 
        self.clock = pg.time.Clock()
        self.welcome = Welcome(self)
        self.tictactoe = TicTacToe(self)

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if self.tictactoe.player == ' ':  # Check if player's choice is not made
                self.welcome.handle_events(event)
            else:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        self.new_game()

    def new_game(self):
        self.welcome = Welcome(self)
        self.tictactoe = TicTacToe(self)

    def draw_winner_message(self):
        font = pg.font.Font(None, 56)
        if self.tictactoe.winner == self.tictactoe.player:
            text = font.render("You win! press space to restart", True, 'black', "white")
        elif self.tictactoe.winner == self.tictactoe.bot:
            text = font.render("Bot wins! press space to restart", True, 'black', "white")
        else:
            text = font.render("It's a draw! press space to restart", True, 'black', "white")

        text_rect = text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2))
        self.screen.blit(text, text_rect)

    def run(self):
        while True:
            if self.tictactoe.player == ' ':
                self.welcome.draw()
                self.check_events()  # Handle events for the Welcome screen
            else:
                self.tictactoe.run()
                self.check_events()
                if self.tictactoe.winner is not None: # Display the winner or draw message
                    self.draw_winner_message()
            pg.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()