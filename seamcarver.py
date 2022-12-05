#!/usr/bin/env python3

from picture import Picture

class SeamCarver(Picture):
    ## TO-DO: fill in the methods below
    def energy(self, i: int, j: int) -> float:
        if i < 0 or i >= self.width() or j < 0 or j >= self.height():
            raise IndexError
        
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
        
        M = [[0 for _ in range( self.width() )] for _ in range( self.height() )]

        for i in range(self.width()):
            M[0][i] = self.energy(i, 0)

        for j in range(1, self.height()):
            for i in range(self.width()):
                if i == 0: #left edge
                    #print("L")
                    M[j][i] = self.energy(i, j) + min( M[j - 1][i], M[j - 1][i + 1] )
                elif i == self.width() - 1: #right edge
                    #print("R") 
                    M[j][i] = self.energy(i, j) + min( M[j - 1][i - 1], M[j - 1][i] )
                else:
                    #print(i)
                    M[j][i] = self.energy(i, j) + min( M[j - 1][i - 1], M[j - 1][i], M[j - 1][i + 1] )

        #print(M)

        min_bottom = min(M[j - self.height()]) #identify the potential seam endings with the lowest values
        seam_indices = []
        for i in range(self.width()):
            if M[j - self.height()][i] == min_bottom:
                seam_indices.append([i]) #append index of a minimum bottom value in a list

        #print(seam_indices) #seam_indices contains the path of the seam along the minimum values from bottom to top

        for potential_seam in seam_indices:
            for j in range(self.height() - 1, 0, -1): #work back up the array along the minimum values, starts at the bottom row and ends at row 1 (second from top)
                current = potential_seam[-1] #current index of "head" of the seam working up the minimals
                if current == 0: #left edge
                    if M[j - 1][current] <= M[j - 1][current + 1]:
                        potential_seam.append(current)
                    else:
                        potential_seam.append(current + 1)
                        
                elif current == self.width() - 1: #right edge
                    if M[j - 1][current] <= M[j - 1][current - 1]:
                        potential_seam.append(current)
                    else:
                        potential_seam.append(current - 1)
                
                else:
                    if M[j - 1][current] <= M[j - 1][current - 1] and M[j - 1][current] <= M[j - 1][current + 1]: #if c <= l and c <= r
                        potential_seam.append(current) #then have the next index up be c since it's the minimum out of the 3
                    elif M[j - 1][current - 1] <= M[j - 1][current] and M[j - 1][current - 1] <= M[j - 1][current + 1]: #if 1 <= c and l <= r
                        potential_seam.append(current - 1) #then have the next index up be l since it's the minimum out of the 3
                    elif M[j - 1][current + 1] <= M[j - 1][current] and M[j - 1][current + 1] <= M[j - 1][current - 1]: #if r <= c and r <= l
                        potential_seam.append(current + 1) #then have the next index up be l since it's the minimum out of the 3

        min_seam_total = 1e100
        for seam in seam_indices: #find min total valued seam out of all seams
            if sum(seam) < min_seam_total:
                min_seam_total = sum(seam)
                final_seam = seam

        final_seam.reverse()
        #print(final_seam)
        return final_seam


    def transpose(self): #essentially flips rows and cols
        new = {}
        
        for j in range(self.height()):
            for i in range(self.width()):
                new[j, i] = self[i, j]

        #print(new)
        #for key in new:
            #print(key)

        temp = self.width() #swap the height and width of the image
        self._width = self._height
        self._height = temp

        self.clear()
        for key in new:
            self[key] = new[key]

        #print(self)


    def find_horizontal_seam(self) -> list[int]:
        self.transpose()
        result = self.find_vertical_seam()
        self.transpose()
        return result
        

    def remove_vertical_seam(self, seam: list[int]):
        if self.width() == 1 or len(seam) != self.height():
            raise SeamError
        
        for j in range(self.height()): #deleting each pixel on seam
            #print(f"Removing pixel ({seam[j]}, {j})")
            del self[seam[j], j]

        for j in range(self.height()): #shift each pixel to the right of seam 1 pixel left
            for i in range(seam[j] + 1, self.width()):
                #print(f"Shifting pixel ({i}, {j}) to ({i - 1}, {j})")
                self[i - 1, j] = self[i, j]
                del self[i, j]

        self._width -= 1 #shrink width by 1 since a seam is removed

        raise SeamError(Exception)


    def remove_horizontal_seam(self, seam: list[int]):
        if self.height() == 1 or len(seam) != self.width():
            raise SeamError
        self.transpose()
        self.remove_vertical_seam(seam)
        self.transpose()

        raise SeamError(Exception)
        

class SeamError(Exception):
    pass
