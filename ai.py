import random, grid  

#The AI is very smart about 95% of the time. Other times it fails to make the smart move due to how the lines might be set up due to the if 
#statements that check if its possible for it to be smart. However, besides this minor bug, the ai will make the game quite enjoyable and challenging.
      
#checks to see if there is a point in the grid with 3 lines in a box shape and completes it
def ai_input (row, column, game_grid):        
    while row < 3:
        while column < 3:
            if game_grid.horizontal_lines[row][column] == 1:
                #Checking for overlaps
                overlap = game_grid.already_chosen_h(row + 1, column)
                 
                #checks for situation where a line on bottom would score a point:		
                if not overlap and game_grid.vertical_lines[column][row] == 1 and game_grid.vertical_lines[column+1][row] == 1:
                    row = row + 1
                    column = column
                    direction = 'horizontal'
                    return row, column, direction	
                 
                #Checking for overlaps
                overlap = game_grid.already_chosen_v(row, column + 1)
                 
                #checks for situation where a line on right would score a point
                if not overlap and game_grid.horizontal_lines[row+1][column] == 1 and game_grid.vertical_lines[column][row] == 1:
                    row = row
                    column = column + 1
                    direction = 'vertical'
                    return row, column, direction 
                 
                #Checking for overlaps
                overlap = game_grid.already_chosen_v(row,column)
                 
                #checks for situation where a line on left would score a point	
                if not overlap and game_grid.horizontal_lines[row+1][column] == 1 and game_grid.vertical_lines[column + 1][row] == 1:	
                    row = row 
                    column = column
                    direction = 'vertical'
                    return row, column, direction  
                 
                if column == 2:
                    return ai_input(row+1,0,game_grid)
                else:
                    return ai_input(row,column+1,game_grid)

            if game_grid.vertical_lines[column][row] == 1:
                #A line at the bottom
                overlap = game_grid.already_chosen_h(row + 1, column)
                if not overlap and game_grid.vertical_lines[column+1][row] == 1 and game_grid.horizontal_lines[row][column] == 1:
                    row = row + 1
                    column = column
                    direction = 'horizontal'
                    return row, column, direction
                 
                #A line at the top
                overlap = game_grid.already_chosen_h(row, column)
                if not overlap and game_grid.vertical_lines[column+1][row] == 1 and game_grid.horizontal_lines[row+1][column] == 1:
                    row = row
                    column = column
                    direction = 'horizontal'
                    return row, column, direction
                      
                #A line at the right
                overlap = game_grid.already_chosen_v(row, column+1)
                if not overlap and game_grid.horizontal_lines[row][column] == 1 and game_grid.horizontal_lines[row+1][column] == 1:
                    row = row + 1
                    column = column
                    direction = 'vertical'
                    return row, column, direction
                 

                if column == 2:
                    return ai_input(row+1,0,game_grid)
                else:
                    return ai_input(row,column+1,game_grid)
                 
            if column == 2:
                return ai_input(row+1,0,game_grid)
            else:
                return ai_input(row,column+1,game_grid)
                
          
     #random
    row, column, direction = random_input(game_grid)
    return row, column, direction
     
     
     
#gets the input for a line from the ai by first seeing if it can be smart. If it can't its a random line
def random_input(game_grid): 
    #random position for top_left_point
    row = random.randrange(0,grid.grid_height)
    column = random.randrange(0,grid.grid_width)
    direction = random.randint(0,1)
    
    #0 = horizontal, 1 = vertical. 	
    if direction == 0:
        direction = 'horizontal'
    else:
        direction = 'vertical'

    #makes sure the line fits on the grid. if not it will start over   
    if direction == 'horizontal' and column == 3:
        return random_input(game_grid)
    elif direction == 'vertical' and row == 3: 
        return random_input(game_grid)
    
    #checks overlap with another line
    if direction == 'horizontal':
        overlap = game_grid.already_chosen_h(row, column)
    else:
        overlap = game_grid.already_chosen_v(row, column)
                
    #if there is an overlap, it will start over 
    if overlap:
        return random_input(game_grid) 
    
    #Checks to see if it's possible to make a smart move
    being_smart_possible = smart_positioning_possible(game_grid)
    
    #If it's possible to be smart, it will be smart
    if being_smart_possible:   
        row, column, direction = smart_positioning(row, column, direction, game_grid)
        
    #Else, it will just be a random position
    else: 
        return row, column, direction
    
    #If it was a bad random for being able to position the line smartly, and it is possible to position a line smartly
    if row == -1:
        return random_input(game_grid)
        
    #Returns the smart position of the line
    else:
        return row, column, direction
            



#The ai plays smart and doesn't give out free boxes by checking the lines placed around the line it is going to place
def smart_positioning(row, column, direction, game_grid):
    if direction == 'horizontal':
        #First horizontal row
        if row == 0 and not ((game_grid.vertical_lines[column][row] == 1 and game_grid.vertical_lines[column+1][row] == 1) or \
                            (game_grid.vertical_lines[column][row] == 1 and game_grid.horizontal_lines[row+1][column] == 1) or \
                            (game_grid.vertical_lines[column+1][row] == 1 and game_grid.horizontal_lines[row+1][column] == 1)):
            return row, column, direction
            
        #Between the first and last row
        elif (row > 0 and row < 3) and not ( (game_grid.vertical_lines[column][row] == 1 and game_grid.vertical_lines[column+1][row] == 1) or \
                            (game_grid.vertical_lines[column][row] == 1 and game_grid.horizontal_lines[row+1][column] == 1) or \
                            (game_grid.vertical_lines[column+1][row] == 1 and game_grid.horizontal_lines[row+1][column] == 1) ) and \
                            not ( (game_grid.vertical_lines[column][row-1] == 1 and game_grid.vertical_lines[column+1][row-1] == 1) or \
                            (game_grid.vertical_lines[column][row-1] == 1 and game_grid.horizontal_lines[row-1][column] == 1) or \
                            (game_grid.horizontal_lines[row-1][column] == 1 and game_grid.vertical_lines[column+1][row-1] == 1) ):
            return row, column, direction
         
        #Last row
        elif row == 3 and not ( (game_grid.vertical_lines[column][row-1] == 1 and game_grid.vertical_lines[column+1][row-1] == 1) or \
                            (game_grid.vertical_lines[column][row-1] == 1 and game_grid.horizontal_lines[row-1][column] == 1) or \
                            (game_grid.horizontal_lines[row-1][column] == 1 and game_grid.vertical_lines[column+1][row-1] == 1) ):
            return row, column, direction
        
        #If it's a bad line that will give away free boxes
        else:
            return -1, -1, -1
                
    else:
        #First vertical column
        if column == 0 and not ((game_grid.vertical_lines[column+1][row] == 1 and game_grid.horizontal_lines[row][column] == 1) or \
                            (game_grid.horizontal_lines[row][column] == 1 and game_grid.horizontal_lines[row+1][column] == 1) or \
                            (game_grid.horizontal_lines[row+1][column] == 1 and game_grid.vertical_lines[column+1][row] == 1)):
            return row, column, direction
        
        #Between the first and last column
        elif (column > 0 and column < 3) and not ((game_grid.vertical_lines[column+1][row] == 1 and game_grid.horizontal_lines[row][column] == 1) or \
                            (game_grid.horizontal_lines[row][column] == 1 and game_grid.horizontal_lines[row+1][column] == 1) or \
                            (game_grid.horizontal_lines[row+1][column] == 1 and game_grid.vertical_lines[column+1][row] == 1)) and \
                            not ((game_grid.vertical_lines[column-1][row] == 1 and game_grid.horizontal_lines[row][column-1] == 1) or \
                            (game_grid.horizontal_lines[row][column-1] == 1 and game_grid.horizontal_lines[row+1][column-1] == 1) or \
                            (game_grid.horizontal_lines[row+1][column-1] == 1 and game_grid.vertical_lines[column-1][row] == 1)):
            return row, column, direction
        
        #Last vertical column
        elif column == 3 and not ((game_grid.vertical_lines[column-1][row] == 1 and game_grid.horizontal_lines[row][column-1] == 1) or \
                            (game_grid.horizontal_lines[row][column-1] == 1 and game_grid.horizontal_lines[row+1][column-1] == 1) or \
                            (game_grid.horizontal_lines[row+1][column-1] == 1 and game_grid.vertical_lines[column-1][row] == 1)):
            return row, column, direction
        
        #If it's a bad line that will give away free boxes
        else:
            return -1, -1, -1
    

#Checks to see if it's possible to make a smart line or if the computer has to just randomly place a line
def smart_positioning_possible(game_grid):
    its_possible_h = False
    its_possible_v = False
    #Horizontal check
    for row in range (0, grid.grid_height - 1):
        for column in range (0, grid.grid_width - 1):
            #If it's in the middle of the three horizontal lines and the line is placed
            if column == 1 and row > 0 and row < 3 and game_grid.horizontal_lines[row][column] == 1 and \
                            not (game_grid.horizontal_lines[row+1][column] == 1 or game_grid.vertical_lines[column][row] == 1 or \
                            game_grid.vertical_lines[column+1][row] == 1) and \
                            not (game_grid.horizontal_lines[row-1][column] == 1 or game_grid.vertical_lines[column][row-1] == 1 or \
                            game_grid.vertical_lines[column+1][row-1] == 1):
                its_possible_h = True
            
            #If it's in the middle of the three horizontal lines and the line is not placed
            if column == 1 and row > 0 and row < 3 and not game_grid.horizontal_lines[row][column] == 1 and \
                            not ((game_grid.vertical_lines[column][row] == 1 and game_grid.vertical_lines[column+1][row] == 1) or \
                            (game_grid.vertical_lines[column][row] == 1 and game_grid.horizontal_lines[row+1][column] == 1) or \
                            (game_grid.vertical_lines[column+1][row] == 1 and game_grid.horizontal_lines[row+1][column] == 1)) and \
                            not ((game_grid.horizontal_lines[row-1][column] == 1 and game_grid.vertical_lines[column][row-1] == 1) or \
                            (game_grid.horizontal_lines[row-1][column] == 1 and game_grid.vertical_lines[column+1][row-1] == 1) or \
                            (game_grid.vertical_lines[column][row-1] == 1 and game_grid.vertical_lines[column+1][row-1] == 1)):
                its_possible_h = True
            
            #If the position it's checking has a line, it will only need 1 more line to not be able to make a smart move
            if row == 0 and game_grid.horizontal_lines[row][column] == 1 and \
                            not (game_grid.horizontal_lines[row+1][column] == 1 or game_grid.vertical_lines[column][row] == 1 or \
                            game_grid.vertical_lines[column+1][row] == 1):
                its_possible_h = True
                
            #If there is no line at the position, then it will need 2 other lines to not be able to make a smart move	
            if row == 0 and not game_grid.horizontal_lines[row][column] == 1 and \
                            not ((game_grid.vertical_lines[column][row] == 1 and game_grid.vertical_lines[column+1][row] == 1) or \
                            (game_grid.vertical_lines[column][row] == 1 and game_grid.horizontal_lines[row+1][column] == 1) or \
                            (game_grid.vertical_lines[column+1][row] == 1 and game_grid.horizontal_lines[row+1][column] == 1)):
                its_possible_h = True
            
            #Rows 1 and 2 the 2 side lines, when the line is placed
            if not column == 1 and row > 0 and row < 3 and game_grid.horizontal_lines[row][column] == 1 and \
                            not (game_grid.horizontal_lines[row+1][column] == 1 or game_grid.vertical_lines[column][row] == 1 or \
                            game_grid.vertical_lines[column+1][row] == 1) and \
                            not (game_grid.horizontal_lines[row-1][column] == 1 or game_grid.vertical_lines[column][row-1] == 1 or \
                            game_grid.vertical_lines[column+1][row-1] == 1):	
                its_possible_h = True
                
            #Rows 1 and 2 the 2 side lines, when the line is not placed
            if not column == 1 and row > 0 and row < 3 and not game_grid.horizontal_lines[row][column] == 1 and \
                            not ( (game_grid.vertical_lines[column][row] == 1 and game_grid.vertical_lines[column+1][row] == 1) \
                            or (game_grid.vertical_lines[column][row] == 1 and game_grid.horizontal_lines[row+1][column] == 1) \
                            or (game_grid.vertical_lines[column+1][row] == 1 and game_grid.horizontal_lines[row+1][column] == 1) ) and \
                            not ( (game_grid.vertical_lines[column][row-1] == 1 and game_grid.vertical_lines[column+1][row-1] == 1) or \
                            (game_grid.vertical_lines[column][row-1] == 1 and game_grid.horizontal_lines[row-1][column] == 1) or \
                            (game_grid.horizontal_lines[row-1][column] == 1 and game_grid.vertical_lines[column+1][row-1] == 1) ):
                its_possible_h = True
            
    #Vertical check
    for column in range (0, grid.grid_height - 1):
        for row in range (0, grid.grid_width - 1):
            #If it's in the middle of the three vertical lines and the line is placed
            if row == 1 and column > 0 and column < 3 and game_grid.vertical_lines[row][column] == 1 and \
                            not (game_grid.horizontal_lines[row][column] == 1 or game_grid.horizontal_lines[row+1][column] == 1 or \
                            game_grid.vertical_lines[column+1][row] == 1) and \
                            not (game_grid.horizontal_lines[row][column-1] == 1 or game_grid.horizontal_lines[row+1][column-1] == 1 or \
                            game_grid.vertical_lines[column-1][row] == 1):
                its_possible_v = True
            
            #If it's in the middle of the three vertical lines and the line is not placed
            if row == 1 and column > 0 and column < 3 and not game_grid.vertical_lines[row][column] == 1 and \
                            not ((game_grid.vertical_lines[column+1][row] == 1 and game_grid.horizontal_lines[row][column] == 1) or \
                            (game_grid.horizontal_lines[row][column] == 1 and game_grid.horizontal_lines[row+1][column] == 1) or \
                            (game_grid.horizontal_lines[row+1][column] == 1 and game_grid.vertical_lines[column+1][row] == 1)) and \
                            not ((game_grid.horizontal_lines[row][column-1] == 1 and game_grid.horizontal_lines[row+1][column-1] == 1) or \
                            (game_grid.horizontal_lines[row][column-1] == 1 and game_grid.vertical_lines[column-1][row] == 1) or \
                            (game_grid.horizontal_lines[row+1][column-1] == 1 and game_grid.vertical_lines[column-1][row] == 1)) :
                its_possible_v = True
            
            #If the position it's checking has a line, it will only need 1 more line to not be able to make a smart move
            if column == 0 and game_grid.vertical_lines[column][row] == 1 and \
                            not (game_grid.horizontal_lines[row][column] == 1 or game_grid.horizontal_lines[row+1][column] == 1 or \
                            game_grid.vertical_lines[column+1][row] == 1):
                its_possible_v = True
                
            #If there is no line at the position, then it will need 2 other lines to not be able to make a smart move	
            if column == 0 and not game_grid.vertical_lines[column][row] == 1 and \
                            not ((game_grid.vertical_lines[column+1][row] == 1 and game_grid.horizontal_lines[row][column] == 1) or \
                            (game_grid.horizontal_lines[row][column] == 1 and game_grid.horizontal_lines[row+1][column] == 1) or \
                            (game_grid.horizontal_lines[row+1][column] == 1 and game_grid.vertical_lines[column+1][row] == 1)):
                its_possible_v = True
            
            #Columns 1 and 2 the 2 side lines, when the line is placed
            if not row == 1 and column > 0 and column < 3 and game_grid.vertical_lines[column][row] == 1 and \
                            not (game_grid.horizontal_lines[row][column] == 1 or game_grid.horizontal_lines[row+1][column] == 1 or \
                            game_grid.vertical_lines[column+1][row] == 1) and \
                            not (game_grid.vertical_lines[column-1][row] == 1 or game_grid.horizontal_lines[row][column-1] == 1 or \
                            game_grid.horizontal_lines[row+1][column-1] == 1):
                its_possible_v = True
            
            #Columns 1 and 2 the 2 side lines, when the line is not placed
            if not row == 1 and column > 0 and column < 3 and not game_grid.vertical_lines[column][row] == 1 and \
                            not ((game_grid.vertical_lines[column+1][row] == 1 and game_grid.horizontal_lines[row][column] == 1) or \
                            (game_grid.horizontal_lines[row][column] == 1 and game_grid.horizontal_lines[row+1][column] == 1) or \
                            (game_grid.horizontal_lines[row+1][column] == 1 and game_grid.vertical_lines[column+1][row] == 1)) and \
                            not ((game_grid.vertical_lines[column-1][row] == 1 and game_grid.horizontal_lines[row][column-1] == 1) or \
                            (game_grid.horizontal_lines[row][column-1] == 1 and game_grid.horizontal_lines[row+1][column-1] == 1) or \
                            (game_grid.horizontal_lines[row+1][column-1] == 1 and game_grid.vertical_lines[column-1][row] == 1)):
                its_possible_v = True
    
    #If checking from both sides is successful, ai can make a smart move, else it can't
    if its_possible_v and its_possible_h:
        return True
    else:
        return False
            

































