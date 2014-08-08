"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors

Kaili Liu
August 7, 2014
Nini and Yeye's House
"""

import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods
    # PHASE ONE part I
    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        # replace with your code
        if self.get_number(target_row, target_col) != 0:
            return False
        
        for dummy_row in range(target_row + 1, self._height):
            for dummy_col in range(self._width):
                if self.get_number(dummy_row, dummy_col) != (dummy_col + self._width * dummy_row):
                    return False
        
        for dummy_col in range(target_col + 1, self._width):
            if self.get_number(target_row, dummy_col) != (dummy_col + self._width * target_row):
                return False                                        
        return True
    
    ###################
    #helper function
    def find_and_move(self, tile_row, tile_col, target_row, target_col):
        """
        Helper function:
        Helps generate and add commands to move string.
        """
        move_string = ""
        move_string += "u" * (target_row - tile_row) 
        
        # target tile is two or more rows above and to left
        if (target_row - tile_row) > 1 and target_col > tile_col:
            move_string += "l" * (target_col - tile_col)                
            move_string += "drrul" * (target_col - tile_col - 1)
            move_string += "dru"
            move_string += "lddru" * (target_row - tile_row - 1)
            move_string += "ld"
        
        # target tile is two or more rows above and to right
        elif (target_row - tile_row) > 1 and target_col < tile_col:	
            move_string += "r" * (tile_col - target_col)                            
            move_string += "dllur" * (tile_col - target_col - 1)           
            move_string += "dlu"            
            move_string += "lddru" * (target_row - tile_row - 1)
            move_string += "ld"
                        
        # target tile is two or more rows above
        elif (target_row - tile_row) > 1 and target_col == tile_col:
            move_string += "lddru" * (target_row - tile_row - 1)
            move_string += "ld"
            
        # target tile is in row zero, one row above, and to the right
        elif (target_row - tile_row) == 1 and tile_row == 0 and target_col < tile_col:
            move_string += "r" * (tile_col - target_col)            
            move_string += "dllur" * (tile_col - target_col - 1)
            move_string += "dlu"
            move_string += "ld"
        
        # target tile is one row above and to the right
        elif (target_row - tile_row) == 1 and target_col < tile_col:
            move_string += "r" * (tile_col - target_col)            
            move_string += "ulldr" * (tile_col - target_col - 1)
            move_string += "ul"
            move_string += "lddru"
            move_string += "ld"
            
        # target tile is in row zero, one row above, and to the left
        elif (target_row - tile_row) == 1 and tile_row == 0 and target_col > tile_col:
            move_string += "l" * (target_col - tile_col)           
            move_string += "drrul" * (target_col - tile_col - 1)
            move_string += "dru"
            move_string += "ld"
        
        # target tile is one row above and to the left
        elif (target_row - tile_row) == 1 and target_col > tile_col:    
            move_string += "l" * (target_col - tile_col) 
            move_string += "urrdl" * (target_col - tile_col - 1)
            move_string += "ur"  
            move_string += "lddru"
            move_string += "ld"
                                    
        # target tile is one row above
        elif (target_row - tile_row) == 1 and target_col == tile_col:
            move_string += "ld"
            
        # target tile is in the same row
        elif target_row == tile_row:
            move_string += "l" * (target_col - tile_col)
            move_string += "urrdl" * (target_col - tile_col - 1)
        
        return move_string
    
    ###################
    # PHASE ONE part II
    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        # replace with your code
        assert self.lower_row_invariant(target_row, target_col), "Something is wrong."       
        target_pos = self.current_position(target_row, target_col)                
        
        move_string = self.find_and_move(target_pos[0], target_pos[1], target_row, target_col)
        
        self.update_puzzle(move_string)
        assert self.lower_row_invariant(target_row, target_col - 1), "Something is wrong."        
        return move_string
    
    ###################
    # PHASE ONE part III
    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        # replace with your code        
        assert self.lower_row_invariant(target_row, 0), "Lower row invariant returned False."
        target_pos = self.current_position(target_row, 0)
        
        # target tile is one row above
        if target_pos == (target_row - 1, 0):
            move_string = "u"
            move_string += "r" * (self._width - 1)
            self.update_puzzle(move_string)            
            return move_string        
        # target tile is one row above and to right
        if target_pos == (target_row - 1, 1):
            move_string = "u"                    
        
        elif target_pos[0] == target_row - 1:
            move_string = "u"
            move_string += "r" * target_pos[1]
            move_string += "ulldr" * (target_pos[1] - 1)
            move_string += "l"
        
        else:
            move_string = "ur"
            move_string += self.find_and_move(target_pos[0], target_pos[1], target_row - 1, 1)
            
        move_string += "ruldrdlurdluurddlu"
        move_string += "r" * (self._width - 1)
        self.update_puzzle(move_string)
        assert self.lower_row_invariant(target_row - 1, self._width - 1), "Lower row invariant returned False."        
        return move_string

    #############################################################
    # Phase two methods
    # PHASE TWO part I
    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # replace with your code
        if self.get_number(0, target_col) != 0:
            return False      
        
        for dummy_row in range(2, self._height):
            for dummy_col in range(self._width):
                if self.get_number(dummy_row, dummy_col) != (dummy_col + self._width * dummy_row):
                    return False
                
        for dummy_col in range(target_col + 1, self._width):
            if self.get_number(0, dummy_col) != dummy_col:
                return False
            if self.get_number(1, dummy_col) != (self._width + dummy_col):
                return False
            if self.get_number(1, target_col) != (self._width + target_col):
                return False            
        return True
        
    ###################
    # PHASE TWO part II
    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # replace with your code
        if self.get_number(1, target_col) != 0:
            return False        
        for dummy_row in range(2, self._height):
            for dummy_col in range(self._width):
                if self.get_number(dummy_row, dummy_col) != (dummy_col + self._width * dummy_row):
                    return False
        for dummy_col in range(target_col + 1, self._width):
            if self.get_number(1, dummy_col) != self._width + dummy_col:
                return False
        return True
    
    ###################
    # PHASE TWO part III
    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        # replace with your code
        assert self.row0_invariant(target_col), "Row 0 invariant returned False."
        target_pos = self.current_position(0, target_col)
        
        if target_pos[0] == 0 and target_pos[1] == target_col - 1:
            move_string = "ld"
        
        elif target_pos[0] == 1 and target_pos[1] == target_col - 1:
            move_string = "lld"
            move_string += "urdlurrdluldrruld"
            
        else:
            move_string = "ld"
            move_string += self.find_and_move(target_pos[0], target_pos[1], 1, target_col - 1)
            move_string += "urdlurrdluldrruld"

        self.update_puzzle(move_string)
        assert self.row1_invariant(target_col - 1), "Row 1 invariant returned False." + str(target_col) 
        return move_string
    
    ###################
    # PHASE TWO part IV
    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        # replace with your code
        assert self.row1_invariant(target_col), "Row 1 invariant returned False."
        target_pos = self.current_position(1, target_col)
        
        # Same row, left side
        if target_pos[0] == 1 and target_col > target_pos[1]:
            move_string = "l" * (target_col - target_pos[1])
            move_string += "urrdl" * (target_col - target_pos[1] - 1)            
            move_string += "ur"
            
        # Top row, left side
        elif target_pos[0] == 0 and target_col > target_pos[1]:
            move_string = "u"
            move_string += "l" * (target_col - target_pos[1])
            move_string += "drrul" * (target_col - target_pos[1] - 1)
            move_string += "dru"
            
        # One row above
        elif target_pos[0] == 0 and target_col == target_pos[1]:
            move_string = "u"            
            
        self.update_puzzle(move_string)
        assert self.row0_invariant(target_col), "Row 0 invariant returned False."
        return move_string

    
    ###########################################################
    # Phase 3 methods
    # Helper function
    def check_2x2(self):
        """
        Helper function:
        Checks if the 2x2 part is solved.
        """
        if self.current_position(0, 0)  != (0, 0):
            return False
        if self.current_position(0, 1) != (0, 1):
            return False
        if self.current_position(1, 0) != (1, 0):
            return False
        if self.current_position(1, 1) != (1, 1):
            return False
        return True
       
        
    # PHASE THREE part I
    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        # replace with your code
        assert self.row1_invariant(1), "Row 1 invariant returned False."
        move_string = "lu"
        self.update_puzzle(move_string)
        
        while not self.check_2x2():
            move_string += "rdlu"
            self.update_puzzle("rdlu")
        
        return move_string
    
    ###################
    # PHASE THREE part II
    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        # replace with your code
        zero_pos = self.current_position(0, 0)
        solution_string = "d" * (self._height - zero_pos[0] - 1)
        solution_string += "r" * (self._width - zero_pos[1] - 1)
        self.update_puzzle(solution_string)

        for dummy_row in range(self._height - 1, 1, -1):
            for dummy_col in range(self._width - 1, 0, -1):
                solution_string += self.solve_interior_tile(dummy_row, dummy_col)
            solution_string += self.solve_col0_tile(dummy_row)
        
        for dummy_col in range(self._width - 1, 1, -1):    
            solution_string += self.solve_row1_tile(dummy_col)        
            solution_string += self.solve_row0_tile(dummy_col)

        solution_string += self.solve_2x2()
        return solution_string

# Start interactive simulation
#obj = Puzzle(3, 3, [[0, 1, 2], [3, 4, 5], [6, 7, 8]])

#obj = Puzzle(3, 3, [[8, 7, 6], [5, 4, 3], [2, 1, 0]])
#obj.solve_puzzle()
#poc_fifteen_gui.FifteenGUI(obj)
#poc_fifteen_gui.FifteenGUI(Puzzle(4, 4))