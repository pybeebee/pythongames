"""
Clone of 2048 game.
June 14, 2014
Kaili Liu
"""

import poc_2048_gui        
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.    
OFFSETS = {UP: (1, 0), 
           DOWN: (-1, 0), 
           LEFT: (0, 1), 
           RIGHT: (0, -1)} 
   
def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    if len(line) <= 1:
        return line
    else: 
        result_list = []
        for item in line:
            if item != 0:        
                result_list.append(item)           
        while len(result_list) < len(line):
            result_list.append(0)        
        if result_list[0] == result_list[1]:
                result_list[0] += result_list[1]
                result_list.remove(result_list[1])
                
        count = 1
        while count < (len(result_list)-1):
            if result_list[count] == result_list[(count + 1)]:
                result_list[count] += result_list[count + 1]
                result_list.pop(count + 1)
                result_list.append(0)
            count += 1   
                
        while len(result_list) < len(line):
            result_list.append(0) 
        return result_list        


class TwentyFortyEight:
    """
    Class to run the game logic.
    """
    def __init__(self, grid_height, grid_width):
        self.rows = grid_height
        self.cols = grid_width
        self.grid_list = []
        self.reset()
        self.length_limits = {UP: self.rows, DOWN: self.rows, LEFT: self.cols, RIGHT: self.cols}
        self.indices_list = {UP: [[0, w] for w in range(self.cols)],
                             DOWN: [[self.rows - 1, x] for x in range(self.cols)],
                             LEFT: [[y, 0] for y in range(self.rows)],
                             RIGHT: [[z, self.cols - 1] for z in range(self.rows)]}
        
    #Reset the game so the grid is empty
    def reset(self):
        """
        Reset the game so the grid is empty.
        """
        self.grid_list = []
        while len(self.grid_list) < (self.rows * self.cols):
            self.grid_list.append(0)
    
   
    def __str__(self):  
        """
        Return a string representation of the grid for debugging.
        """
        grid_string = ""
        for row in range(self.rows):
            for col in range(self.cols):
                grid_string += str(self.grid_list[row * self.cols + col])
                grid_string += ' '
            grid_string += '\n'
        return grid_string
        

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self.rows

   
    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self.cols
    
    
    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        base = self.indices_list[direction]        
        the_offset = OFFSETS[direction]
        tile_moved = False
        
        for num in base:
            list_one = []
            temp_list = list(list_one)
            
            for numtwo in range(self.length_limits[direction]):
                list_one.append(self.get_tile(num[0] + numtwo*the_offset[0], num[1] + numtwo*the_offset[1]))
            temp_list = merge(list_one)			          
            
            for numthree in range(self.length_limits[direction]):                
                self.set_tile(num[0] + (numthree * the_offset[0]), num[1] + (numthree * the_offset[1]), temp_list[numthree])            
                tile_moved = tile_moved or (temp_list[numthree] != list_one[numthree])
                
        if tile_moved:
            self.new_tile()
                
                                    
        
    
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty 
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        tile_choices = [2, 2, 2, 2, 2, 2, 2, 2, 2, 4]
        tile_choice_num = random.choice(tile_choices)
        the_row = random.randrange(0, self.rows)
        the_col = random.randrange(0, self.cols) 
        while self.grid_list[(the_row* self.cols) + the_col] != 0:
            the_row = random.randrange(0, self.rows)
            the_col = random.randrange(0, self.cols)               
        if self.grid_list[(the_row* self.cols) + the_col] == 0:
            self.grid_list[(the_row* self.cols) + the_col] = tile_choice_num
          
   
    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """  
        self.this_row = row
        self.this_col = col        
        self.value = value
        self.grid_list[(self.this_row * self.cols) + self.this_col] = self.value

        

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """  
        self.row = row
        self.col = col        
        tile_val = self.grid_list[(self.row * self.cols) + self.col]
        return tile_val
    
poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
