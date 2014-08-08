"""
Student portion of Zombie Apocalypse mini-project
July 16, 2014
Kaili Liu
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = "obstacle"
HUMAN = "human"
ZOMBIE = "zombie"


class Zombie(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """
    # phase one
    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._human_list = []
        self._zombie_list = []        
        
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        location = (row, col)
        self._zombie_list.append(location)
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)       
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        # replace with an actual generator
        for dummy_zombie in self._zombie_list:
            yield dummy_zombie
        

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        location = (row, col)
        self._human_list.append(location)
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        # replace with an actual generator
        for dummy_human in self._human_list:
            yield dummy_human

                                   
# phase two
    def compute_distance_field(self, entity_type):
        """
        Function computes a 2D distance field
        Distance at member of entity_queue is zero
        Shortest paths avoid obstacles and use distance_type distances
        """
        grid_height = self.get_grid_height()
        grid_width = self.get_grid_width()
        visited = poc_grid.Grid(grid_height, grid_width)
        
        distance_field = [[self.get_grid_height() * self.get_grid_width() for dummy_col in range(self._grid_width)] 
                       for dummy_row in range(self._grid_height)]
        boundary = poc_queue.Queue()
        
        if entity_type == HUMAN:
            for dummy_index in range(self.num_humans()):
                boundary.enqueue(self._human_list[dummy_index])                
                distance_field[self._human_list[dummy_index][0]][self._human_list[dummy_index][1]] = 0
        
        if entity_type == ZOMBIE:
            for dummy_index in range(self.num_zombies()):
                boundary.enqueue(self._zombie_list[dummy_index])
                distance_field[self._zombie_list[dummy_index][0]][self._zombie_list[dummy_index][1]] = 0
        
        for dummy_item in boundary:
            visited.set_full(dummy_item[0], dummy_item[1])
            distance_field[dummy_item[0]][dummy_item[1]] = 0
                
        while len(boundary) > 0:            
            current_cell = boundary.dequeue()
            neighbors = visited.four_neighbors(current_cell[0], current_cell[1])
            for neighbor in neighbors:                
                if visited.is_empty(neighbor[0], neighbor[1]) and self.is_empty(neighbor[0], neighbor[1]):
                    visited.set_full(neighbor[0], neighbor[1])
                    boundary.enqueue(neighbor)
                    distance_field[neighbor[0]][neighbor[1]] = min(distance_field[neighbor[0]][neighbor[1]], distance_field[current_cell[0]][current_cell[1]] + 1)
        return distance_field                
        
# phase three        
    def move_humans(self, zombie_distance):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        maxdist_squares = []
        temp_humanlist = []
        for human in self._human_list:
            poss_squares = self.eight_neighbors(human[0], human[1])
            max_distance = 0
            for square in poss_squares:
                distance = zombie_distance[square[0]][square[1]]
                if distance > max_distance:
                    max_distance = distance
                    maxdist_squares = []
                    maxdist_squares.append(square)
                elif distance == max_distance:
                    maxdist_squares.append(square)
            if len(maxdist_squares) == 1:
                temp_humanlist.append(maxdist_squares[0])
            elif len(maxdist_squares) > 1:
                choice = random.choice(maxdist_squares)
                temp_humanlist.append(choice)
        self._human_list = temp_humanlist
                
                
                        
    def move_zombies(self, human_distance):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """        
        temp_zombielist = []
        for zombie in self._zombie_list:
            mindist_squares = [zombie]
            poss_squares = self.four_neighbors(zombie[0], zombie[1])
            min_distance = human_distance[zombie[0]][zombie[1]]
            for square in poss_squares:
                distance = human_distance[square[0]][square[1]]
                if distance < min_distance:
                    min_distance = distance
                    mindist_squares = []
                    mindist_squares.append(square)
                elif distance == min_distance:
                    mindist_squares.append(square)

            if len(mindist_squares) == 1:
                temp_zombielist.append(mindist_squares[0])
            elif len(mindist_squares) > 1:
                choice = random.choice(mindist_squares)
                temp_zombielist.append(choice)
            
        self._zombie_list = temp_zombielist
        
                

# Start up gui for simulation - You will need to write some code above
# before this will work without errors

poc_zombie_gui.run_gui(Zombie(30, 40))
