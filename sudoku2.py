import copy, pygame, sys
pygame.init()


board_grid =[
    [7, 8, 0, 4, 0, 0, 1, 2, 0] ,
    [6, 0, 0, 0, 7, 5, 0, 0, 9] ,
    [0, 0, 0, 6, 0, 1, 0, 7, 8] ,
    [0, 0, 7, 0, 4, 0, 2, 6, 0] ,
    [0, 0, 1, 0, 5, 0, 9, 3, 0] ,
    [9, 0, 4, 0, 6, 0, 0, 0, 5] ,
    [0, 7, 0, 3, 0, 0, 0, 1, 2] ,
    [1, 2, 0, 0, 0, 7, 4, 0, 0] ,
    [0, 4, 9, 2, 0, 6, 0, 0, 7] ,
    ]
#-----------
# SETTINGS
#------------

# selected_board can be board_easy or board_hard
selected_board = board_grid

screen = 'play'

WIDTH, HEIGHT = 500, 555

class Square:
    def __init__(self, y, x):
        self.y = y
        self.x = x
        self.alpha = 0

class Board:
    def __init__ (self, board):
        self.open = []
        self.squares = []
        self.current = 0
        self.active = False
        self.value = False
        self.display = ''
        self.board = copy.deepcopy(board)
        for x in range(9):
            for y in range(9):
                square = Square(y, x)
                self.squares.append(square)
                if self.board[y][x] == 0: self.open.append(square)

    def check_square(y, x, num, board):
        if num == 0: return True
        for i in range(9):
            if board[y][i] == num and i != x: return False
            if board[i][x] == num and i != y: return False
        for dy in range(3):
            for dx in range(3):
                box_x, box_y = (x // 3 * 3) + dx, (y // 3 * 3) + dy
                if board[box_y][box_x] == num and box_y != y and box_x != x:
                    return False
        return True

    def solve(self, step):
        while self.current < len(self.open):
            square = self.open[self.current]
            y, x = square.y, square.x
            found = False
            for num in range(self.board[y][x] + 1, 10):
                if Board.check_square(y, x, num, self.board):
                    found = True
                    self.current += 1
                    square.alpha = 0
                    self.board[y][x] = num ; break
            if not found:
                self.board[y][x] = 0
                self.current -= 1
                square.alpha = 128
            if step: break

    def print_board(self):
        for cnt, row in enumerate(self.board):
            if cnt in [3, 6]:
                print('-' * 11)
            for cnt, num in enumerate(row):
                print(num, end = '')
                if cnt in [2, 5]:
                    print('|', end = '')
            print('')
        print('')

    def blit(self):
        #active square
        if self.active:
            active_surf = pygame.Surface((int(SEC), int(SEC)))
            active_rect = active_surf.get_rect(center = (SEC * self.active.y + SEC/2, SEC * self.active.x + SEC/2))
            pygame.draw.rect(WIN, (100, 100, 100), active_rect)

        for square in self.squares:
            #red
            red_surf = pygame.Surface((SEC, SEC))
            red_surf.set_alpha(square.alpha)
            red_surf.fill((255,0,0))
            red_rect = red_surf.get_rect(center = (SEC * square.y + SEC/2, SEC * square.x + SEC/2))
            WIN.blit(red_surf, red_rect)

            #nums
            if square in self.open:
                color = 'green' if board.board == solved_board.board else 'white'
            else: color = 'red'
            num = '' if self.board[square.y][square.x] == 0 else str(self.board[square.y][square.x])
            num_surf = FONT.render(num, 1, color)
            num_rect = num_surf.get_rect(center = (SEC * square.y + SEC/2, SEC * square.x + SEC/2))
            WIN.blit(num_surf, num_rect)

        #red border
        for square in self.open:
            if not Board.check_square(square.y, square.x, self.board[square.y][square.x], self.board):
                pygame.draw.rect(WIN, (255, 0, 0), (SEC * square.y + GAP/2, SEC * square.x + GAP/2, SEC - GAP, SEC - GAP), width = 1, border_radius = 2)

        #line
        for i in range(int(SEC)):
            width = 3 if i in [3,6] else 1
            pygame.draw.line(WIN, 'white',  (SEC * i, 0), (SEC * i, WIDTH), width = width)
            pygame.draw.line(WIN, 'white', (0, SEC * i,), (WIDTH, SEC * i), width = width)

        #solve button
        pygame.draw.rect(WIN, 'red', solve_rect)
        WIN.blit(solve_text, solve_rect)

    def mouse_down(self):
        clicked = False
        for square in self.open:
            rect = pygame.Rect(SEC * square.y, SEC * square.x, SEC, SEC)
            if rect.collidepoint(mouse_pos):
                self.active = square
                self.value = self.board[square.y][square.x]
                self.display = '' if self.value == 0 else str(self.value)
                clicked = True ; break
        if not clicked and self.active:
            self.board[self.active.y][self.active.x] = 0 if self.display == '' else int(self.display)
            self.active = False


    def key_down(self):
        if self.active != False:
            if event.key == pygame.K_BACKSPACE:
                self.display = ''
            elif event.unicode in [str(x) for x in range(10)]:
                self.display = str(event.unicode)
            self.board[self.active.y][self.active.x] = 0 if self.display == '' else int(self.display)



SIZE = (WIDTH, HEIGHT)
SEC = (WIDTH - 1) / 9
pygame.font.init()
FONT = pygame.font.SysFont('arial', 30)
WIN = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
board = Board(selected_board)
solved_board = Board(selected_board)
solved_board.solve(step = False)
GAP = 10

solve_text = FONT.render('Solve', 1, 'white')
solve_rect = solve_text.get_rect(center = (WIDTH/2, HEIGHT - SEC/2))

while True:
    mouse_pos = pygame.mouse.get_pos()
    pygame.display.update()
    WIN.fill('black')
    board.blit()

    if screen == 'play':
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                board.mouse_down()

                if solve_rect.collidepoint(mouse_pos):
                    screen = 'solve'
                    board = Board(selected_board)

            if event.type == pygame.KEYDOWN:
                board.key_down()

    if screen == 'solve':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        board.solve(step = True)
