"""
Cookie Clicker Simulator
June 24, 2014
Kaili Liu
"""

import simpleplot
import math

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0


class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._current_cookies = 0.0
        self._total_cookies = 0.0
        
        self._current_time = 0.0
        self._current_cookies_per_second = 1.0
        
        self._just_bought_upgrade = None
        self._now_upgrade_cost = 0.0
        self._orig_upgrade_cost = 0.0
        
        self._history_list = [(0.0, None, 0.0, 0.0)]


    def __str__(self):
        """
        Return human readable state
        """
        game_state = ""        
        game_state += '\n'
        game_state += '\n'
        
        game_state += "Time: "
        game_state += str(self._current_time)         
        game_state += '\n'
        
        game_state += "Current Cookies: "
        game_state += str(self._current_cookies) 
        game_state += '\n'
         
        game_state += "CPS: "
        game_state += str(self._current_cookies_per_second) 
        game_state += '\n'
                      
        game_state += "Total Cookies: "
        game_state += str(self._total_cookies) 
        game_state += '\n'
        
        game_state += "History: "
        game_state += str(self._history_list) 
        game_state += '\n'
        game_state += str(len(self._history_list))
        return game_state
    
    
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._current_cookies
    
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """        
        return self._current_cookies_per_second
    
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._current_time


    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: (0.0, None, 0.0, 0.0)
        """        
        return self._history_list


    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if self._current_cookies > cookies:
            return 0.0
        else:
            seconds_until = math.ceil((cookies - self._current_cookies)/ self._current_cookies_per_second)
            return seconds_until


    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0
        """ 
        if time <= 0:
            return  
        else:            
            self._current_cookies += (self._current_cookies_per_second * time)
            self._total_cookies += (self._current_cookies_per_second * time)
            self._current_time += time


    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """  
        if self._current_cookies < cost:
            return
        else:
            self._current_cookies -= cost               
            self._history_list.append((self._current_time, item_name, cost, self._total_cookies))
            self._current_cookies_per_second += additional_cps                         


def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to game.
    """

    # Replace with your code
    game = ClickerState()
    the_clone = build_info.clone()

    while game.get_time() <= duration:
        item_name = strategy(game.get_cookies(), game.get_cps(), duration - game.get_time(), the_clone)
        if (item_name == None):
            break
        item_cost = the_clone.get_cost(item_name)
        item_cps = the_clone.get_cps(item_name)
        item_wait_time = game.time_until(item_cost)
        time_left = duration - game.get_time()        
        if item_wait_time > time_left:
            break
        game.wait(item_wait_time)
        game.buy_item(item_name, item_cost, item_cps)
        the_clone.update_item(item_name)

    if game.get_time() < duration:
        game.wait(duration - game.get_time()) 

    if item_name != None:
        while game.get_cookies() > the_clone.get_cost(item_name):
            game.buy_item(item_name, the_clone.get_cost(item_name), the_clone.get_cps(item_name))
            the_clone.update_item(item_name)

    return game


def strategy_cursor(cookies, cps, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic strategy does not properly check whether
    it can actually buy a Cursor in the time left.  Your strategy
    functions must do this and return None rather than an item you
    can't buy in the time left.
    """
    return "Cursor"


def strategy_none(cookies, cps, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that you can use to help debug
    your simulate_clicker function.
    """    
    return None


def strategy_cheap(cookies, cps, time_left, build_info):
    """
    Always select the cheapest item that you can afford in the time left.
    """
    cheapest_item = None
    cheapest_item_cost = 99999999999999999999999.0
    for item in build_info.build_items():
        item_cost = build_info.get_cost(item)
        if (item_cost <= cookies + cps * time_left) and (item_cost < cheapest_item_cost):
            cheapest_item = item            
            cheapest_item_cost = item_cost    
    return cheapest_item


def strategy_expensive(cookies, cps, time_left, build_info):
    """
    Always select the most expensive item you can afford in the time left.
    """
    most_expensive_item = None
    highest_price = 0.0
    for item in build_info.build_items():
        item_cost = build_info.get_cost(item)
        if (item_cost <= cookies + cps * time_left) and (item_cost > highest_price):
            most_expensive_item = item
            highest_price = item_cost    
    return most_expensive_item


def strategy_best(cookies, cps, time_left, build_info):
    """
    Best possible strategy that I can think of. 
    """
    best_item = None
    best_cps = 0.0
    for item in build_info.build_items():
        item_cost = build_info.get_cost(item)
        item_cps = build_info.get_cps(item)
        if (item_cost <= cookies + cps * time_left) and (item_cps/item_cost > best_cps):
            best_item = item
            best_cps = item_cps/item_cost
            
    return best_item 


def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation with one strategy
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    # history = state.get_history()
    # history = [(item[0], item[3]) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

    
def run():
    """
    Run the simulator.
    """    
    #run_strategy("Cursor", SIM_TIME, strategy_cursor)

    # Add calls to run_strategy to run additional strategies
    #run_strategy("Cheap", SIM_TIME, strategy_cheap)
    run_strategy("Expensive", SIM_TIME, strategy_expensive)
    #run_strategy("Best", SIM_TIME, strategy_best)
    
    
#run()
    
