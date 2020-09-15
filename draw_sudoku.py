import pygame

import sys

class draw:
    def __init__(self, filename = 'sudoku'):
        self.BLACK = (25,25,25)
        self.WHITE = (250, 250, 250)
        self.BLUE=(0,0,255)
        self.WINDOW_HEIGHT = 400
        self.WINDOW_WIDTH = self.WINDOW_HEIGHT
        self.SCREEN = None
        self.CLOCK = None
        
        self.filename = filename+'.jpg'
        


    def draw(self, solution):

        pygame.init()
        self.SCREEN = pygame.display.set_mode((self.WINDOW_HEIGHT, self.WINDOW_WIDTH))
        self.CLOCK = pygame.time.Clock()
        self.SCREEN.fill(self.BLACK)
        while(True):
            self.drawGrid(solution)
            rect = pygame.Rect(0, 0, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
            sub = self.SCREEN.subsurface(rect)
            pygame.image.save(sub, self.filename)
            # sys.exit()
            break


    def drawGrid(self,solution):
        n_rows = 9
        # solution = clauses1
        font1 = pygame.font.SysFont("comicsans", 40) 
        # blockSize = 20 #Set the size of the grid block
        blockSize = self.WINDOW_WIDTH/n_rows
        
        
        solution_pos = [int(i/10)   for i in solution]
        solution_only = [i%10 for i in solution]
        # print(solution_pos)
        for x in range(self.WINDOW_WIDTH):
            for y in range(self.WINDOW_HEIGHT):
                rect = pygame.Rect(x*blockSize, y*blockSize,
                                blockSize, blockSize)
                text_x = x*blockSize + 15
                text_y = y*blockSize + 15
                pos = (y+1)*10 + (x+1)
                text = ''
                
                
                if pos in solution_pos:
                    idx = solution_pos.index(pos)
                    text = solution_only[idx]
                pygame.draw.rect(self.SCREEN, self.WHITE, rect, 1)
                text1 = font1.render(str(text), 1, (255, 255, 255)) 
                self.SCREEN.blit(text1, (text_x, text_y )) 

        vertical_lines_y = [i*self.WINDOW_HEIGHT/3 for i in range(3)] + [self.WINDOW_HEIGHT-1]
        vertical_lines_x = [[0,self.WINDOW_HEIGHT] for i in range(3)]
        for x,y in zip(vertical_lines_x, vertical_lines_y):
            pygame.draw.line(self.SCREEN, self.BLUE, (x[0], y), (x[1],y),  5)

        horizontal_lines_x = [i*self.WINDOW_WIDTH/3 for i in range(3)] + [self.WINDOW_WIDTH-1]
        horizontal_lines_y = [[0,self.WINDOW_WIDTH] for i in range(3)]
        for x,y in zip(horizontal_lines_x, horizontal_lines_y):
            pygame.draw.line(self.SCREEN, self.BLUE, (x, y[0]), (x,y[1]),  5)