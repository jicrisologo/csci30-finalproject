#!/usr/bin/env python3

from picture import Picture

class SeamCarver(Picture):
    ## TO-DO: fill in the methods below
    def energy(self, i: int, j: int) -> float:
        x_gradient = 0
        y_gradient = 0

        r_diff = self[(i + 1) % self.width(), j][0] - self[(i - 1) % self.width(), j][0]
        g_diff = self[(i + 1) % self.width(), j][1] - self[(i - 1) % self.width(), j][1]
        b_diff = self[(i + 1) % self.width(), j][2] - self[(i - 1) % self.width(), j][2]
        x_gradient = r_diff ** 2 + g_diff ** 2 + b_diff ** 2

        r_diff = self[i, (j + 1) % self.height()][0] - self[i, (j - 1) % self.height()][0]
        g_diff = self[i, (j + 1) % self.height()][1] - self[i, (j - 1) % self.height()][1]
        b_diff = self[i, (j + 1) % self.height()][2] - self[i, (j - 1) % self.height()][2]
        y_gradient = r_diff ** 2 + g_diff ** 2 + b_diff ** 2

        return x_gradient + y_gradient

    def find_vertical_seam(self) -> list[int]:
        '''
        Return a sequence of indices representing the lowest-energy
        vertical seam
        '''
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
