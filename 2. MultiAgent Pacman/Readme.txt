Included, search.py & searchAgents.py

Estimated-Time-Spent-on-Homework :
20-25 Hours

Question-1 evaluationfunction:

 => Summary: Evaluated the score on the basis of manhattan distance to foodpostion, ghostlocation && it's state, whether it is in scarystate or activestate, and length of the foodlist.

 """
    This was what I did, while improving the evaluationFunction:
    1. So First of All I extracted all the requirements, it was required to create a evaluation function.
       Evaluation funnction was supposed to return the score, that was explicit and the computation should be on the 
       basis of some factor.
    2. CurrentPacmanposition, foodlist, and ghosts were alrerady pre-existing. Stored Ghost locations and it's 
       scaretime in Ghosts_manhattandist_scaredtimer multidimensional list, where each node's first element is location
       of ghost and second element is it's scarytime.
       so Ghosts_manhattandist_scaredtimer= [(ghostlocation,scaredtime)...n] for all items.
    3. My  evaluation function works by taking 4 factors into consideration.
        -> Inversed Manhattan distance from current location of pacman to food
        -> Distance from ghost and whether the ghost is in scarystate, i.e whether ghosts are eatable or
           they'll end the game and computed score on the basis of that. +1000 when the ghost is eatable, since that 
           leads to the maximum score and -100 when the ghosts are near, and since that situation can end the game,
           negated it's score. 
        -> length of the foodlist (empirical analysis of adding this component made the code more efficient)
        -> Succescorscore, my total addition was summation of all the above components.
    4. Achieved some of the values, by empirical testing of evaluationfunction.
    """

 Question-5 betterevaluationfunction:

 	Summary: Evaluated the score on the basis of weighted manhattan distance to foodpostion, ghostlocation && it's state, whether it is in scarystate or activestate, and length of the foodlist.

    """
    This was what I did, while improving the evaluationFunction in making betterevaluationfunction:
    Used the majority of logic same, as it was in above evaluation function, with following tweaks:
    1. Ghost function was same, in foodheuristic, I tried dividing tempmanhattandistance, but the function worsened
      so multiplied, the tempmanhattandistance with itself and it improved the algorithm.
    2.     Food_ghost_Scores_Total = Total_ghost_score*0.5  + Total_food_score*0.5 + foodlength*2
            totalevaluation = successorscore*0.2 + Food_ghost_Scores_Total*0.8 
      This was the major change in code, where I gave weightage to each compnents, on the basis of empirical analysis,
      by trying multiple combinations, this led to best optimal solution, where totalevaluation is based majorly on successorscore
      and distance total for manhattan,food and twice food length. 
      Weightage of system:
        successorscore = 20% of the overall weightage score.
        Food_ghost_Scores_Total = 80% of the overall weightage score.
         where,
            Total_ghost_score & Total_food_score = 33.33% of weightage of Food_ghost_Scores_Total
            Foodlist's length = 66.66% of weightage of Food_ghost_Scores_Total      
    
    """