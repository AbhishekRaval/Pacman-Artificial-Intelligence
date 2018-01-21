Included, search.py & searchAgents.py

Estimated-Time-Spent-on-Homework :
38-40 Hours

Question-6 Heuristic:

 => Summary: In my CornersProblem class's state, I assigned pacman's current state and list of corners.
 	By looping  through the corners from problemstate, I appended manhattan distances to each corner
 	and returned the maximum manhattan distance from the list.

 	#Documentation of heuristics, and why I chose this heuristic:
 	#begin solving heuristic by tweaking manhattan distance and
    " Initiall  tried to solve by dividing, cartesian co-ordinate recursively, but it was returning under-efficient heuristic"
            #about 1654 nodes were expanded
    "and then tried to use min(heuristic ditance to corners), but it was very very low ball, and worse than UCS"
            #about 1967 nodes were expanded
    "and finally checked maximum(manhattan distance from current state to corners)"
            #about 1137 nodes were expanded

 Question-7 FoodHeuristic:

 	Summary: returned max(MazeDistance to first list element of grid,
 							 maximum of the Manhattandistance to each food co-ordinate)

 	 #Documentation of heuristics, and why I chose this heuristic:						 
     #attempt_1
    """ Had pacman's position and foodgrid's list, so begin solving by simply using maximum manhattan distance
        from the given food list.
        code:
        for food in food_grid_list:
        manhattan_temp = util.manhattanDistance(current_pacman_Position, food)
        temp_possible_distance = manhattan_temp
        maximum.append(temp_possible_distance)
        MAXX_possible_distance = max(maximum)
        output:
        Path found with total cost of 60 in 20.9 seconds
        Search nodes expanded: 9551"""
    #attempt_2
    """ Did the same thing I did above with mazedistance function, received  goalstate as startinggoalstate
        as the  given problem was in instance of foodsearch problem, so used it's starting state as state
        code: 
        same as above with following tweak:
        gameState = problem.startingGameState
        manhattan_temp = mazeDistance(current_pacman_Position, food,gameState)
        output:
        Path found with total cost of 60 in 60.7 seconds
        Search nodes expanded: 4137"""
    #node expansion decreased, but the time  cost for mazedistance calculation turned out to be way too high.
    # so I combined both mazedistance and manhattan distance
    """ I divided the problem into two parts:
        1) Checked Mazedistance from the 1st element of foodgridlist, as there will alway be some element in it.
           Assigned maxx to it.
        2)  looped the foodlist, and if there was a distance that was more than above assigned maxx, assigned at
         as new heuristic.
         output:
         Path found with total cost of 60 in 17.1 seconds
         Search nodes expanded: 6517"""
    #total nodes eexpanded were bit more, but the time-complexity decreased.	