#!/usr/bin/env python3

from picture import Picture

class SeamCarver(Picture):
    ## TO-DO: fill in the methods below
    def energy(self, i: int, j: int) -> float:
        x_gradient = 0
        y_gradient = 0

        r_diff = self[self.safe_index(i + 1, 'w'), j][0] - self[self.safe_index(i - 1, 'w'), j][0]
        g_diff = self[self.safe_index(i + 1, 'w'), j][1] - self[self.safe_index(i - 1, 'w'), j][1]
        b_diff = self[self.safe_index(i + 1, 'w'), j][2] - self[self.safe_index(i - 1, 'w'), j][2]
        x_gradient = r_diff ** 2 + g_diff ** 2 + b_diff ** 2

        r_diff = self[i, self.safe_index(j + 1, 'h')][0] - self[i, self.safe_index(j - 1, 'h')][0]
        g_diff = self[i, self.safe_index(j + 1, 'h')][1] - self[i, self.safe_index(j - 1, 'h')][1]
        b_diff = self[i, self.safe_index(j + 1, 'h')][2] - self[i, self.safe_index(j - 1, 'h')][2]
        y_gradient = r_diff ** 2 + g_diff ** 2 + b_diff ** 2

        return x_gradient + y_gradient

    def safe_index(self, x, dim): #wraps index around to avoid having to write if statements for edge cases
        if dim == 'w':
            return x % self.width()
        elif dim == 'h':
            return x % self.height()
            

    def find_vertical_seam(self) -> list[int]:
        '''
        Return a sequence of indices representing the lowest-energy
        vertical seam
        '''
        
        M = [[0 for _ in range( self.width() )] for _ in range( self.height() )]

        #copying over topmost row of energy values to M
        for i in range(self.width()):
            M[0][i] = self.energy(i, 0)

        for j in range(1, self.height()):
            for i in range(self.width()):
                if i == 0: #left edge
                    #print("L!")
                    M[j][i] = self.energy(i, j) + min( M[j - 1][i], M[j - 1][i + 1] )
                elif i == self.width() - 1: #right edge
                    #print("R!") 
                    M[j][i] = self.energy(i, j) + min( M[j - 1][i - 1], M[j - 1][i] )
                else:
                    #print("O:")
                    M[j][i] = self.energy(i, j) + min( M[j - 1][i - 1], M[j - 1][i], M[j - 1][i + 1] )
                
        for row in M:
            print(row)
                
        raise NotImplementedError

    def find_horizontal_seam(self) -> list[int]:
        '''
        Return a sequence of indices representing the lowest-energy
        horizontal seam
        '''
        raise NotImplementedError

    def remove_vertical_seam(self, seam: list[int]):
        '''
        Remove a vertical seam from the picture
        '''
        raise NotImplementedError

    def remove_horizontal_seam(self, seam: list[int]):
        '''
        Remove a horizontal seam from the picture
        '''
        raise NotImplementedError

class SeamError(Exception):
    pass
