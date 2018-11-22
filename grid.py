grid_width = 4
grid_height = 4


class Grid:
    #initializes 3 lists that contain values for all horizontal and vertical lines,
    #as well as initials for both the AI and the human 
    def __init__(self, save_game = 'NONE'):
        if save_game == 'NONE':
            self.horizontal_lines =   [0, 0, 0], \
                                      [0, 0, 0], \
                                      [0, 0, 0], \
                                      [0, 0, 0]
                    
            self.vertical_lines =   [0, 0, 0], \
                                    [0, 0, 0], \
                                    [0, 0, 0], \
                                    [0, 0, 0]

            self.initials =   [' ', ' ', ' '], \
                              [' ', ' ', ' '], \
                              [' ', ' ', ' ']

            self.computer_initial = 'C'

            self.player_initial = 'A'
        
        else: 
            self.horizontal_lines = []
            self.vertical_lines = []
            self.initials = []
            self.computer_initial = ''
            self.player_initial = ''
            
            reading_file = open(save_game , 'r')
            line = reading_file.readline()
            
            #Gets the horizontal lines list
            for counter in range (0,grid_height):
                line = line.strip("\n")
                line = line.split(',')
                line.pop(3)
                
                self.horizontal_lines.append(line)
                
                line = reading_file.readline()
            
            #Gets the vertical lines list
            for counter in range (0,grid_height):
                line = line.strip("\n")
                line = line.split(',')
                line.pop(3)
                
                self.vertical_lines.append(line)
                
                line = reading_file.readline()
            
            #Gets the initials list
            for counter in range (0,grid_height - 1): 
                line = line.strip("\n")
                line = line.split(',')
                line.pop(3)
                
                self.initials.append(line)
                
                line = reading_file.readline()
            
            #Gets the computers initial
            line = line.strip("\n")
            self.computer_initial = line
            
            #Gets the players initial
            line = reading_file.readline()
            line = line.strip("\n")
            self.player_initial = line
            
            reading_file.close()

    ######NOT USED
    #prints the game grid   
    def print_grid(self): 
        #top row
        print("    a   b   c   d")
        for down in range (0,grid_height):
            #prints the number for the row at the left side
            print(down + 1, end='')
            for right in range (0,grid_width):
                #if there is supposed to be a line there, it prints the line with a dot
                if right > 0 and right < 4 and self.horizontal_lines[down][right-1] == 1:
                   print("---.", end='')

                #if there is no line, then it just prints spaces with a dot
                else:
                   print("   .", end='')

            print()

            #so it only prints it 9 times
            if down < 3:
                for initialcounter in range (0,grid_width):
                   #prints spaces for the very first counter because it requires extra spaces.
                   if initialcounter == 0:
                      print("   ", end='')
                
                   #prints a line if the spot has been chosen
                   if self.vertical_lines[initialcounter][down] == 1:
                      print(" |", end='')
                      #the spacing for the initials is different if there is a line
                      if initialcounter < 3:
                         print(" " + self.initials[down][initialcounter], end='')
                   #prints the initial if there is no line
                   elif initialcounter < 3:
                      print("   " + self.initials[down][initialcounter], end='')
            #goes down one row		
            print()
    
        
    #finds the position of the line and changes the grid accordingly      
    def placing_line(self, row, column, direction):	      
        if direction == 'horizontal':
            self.horizontal_lines[row][column] = 1
        
        else:
            self.vertical_lines[column][row] = 1

    #checks for overlaps if the line is horizontal   
    def already_chosen_h(self, row, column): 
        if self.horizontal_lines[row][column] == 1 :
            return True
        else:
            return False    
        
    #checks for overlaps if the line is vertical      
    def already_chosen_v(self,row ,column): 
        if self.vertical_lines[column][row] == 1 :
            return True
        else:
            return False
      
    #places the initial of the player after checking if the box is complete
    def putting_initial(self, initial): 
        for down in range (0,3):
            for right in range (0,3):
                if self.horizontal_lines[down][right] == 1  and self.vertical_lines[right][down] == 1 and self.vertical_lines[right + 1][down] == 1 and self.horizontal_lines[down + 1][right] == 1:
                   if self.initials[down][right] == ' ':
                      self.initials[down][right] = initial

    #checks to see if the game is over by going through the initials list and if finding a space returns False   
    def game_end(self): 
        for down in range (0,3):
            for right in range (0,3):
                if self.initials[down][right] == ' ':
                   return False
        return True

    #calculates the score by scanning through the initial grid   
    def victory(self,): 
        ai_initial_counter = 0
        player_initial_counter = 0
        for down in range (0,3):
            for right in range (0,3):
                if self.initials[down][right] == self.player_initial:
                    player_initial_counter = player_initial_counter + 1
                else:
                    ai_initial_counter = ai_initial_counter + 1
        return player_initial_counter, ai_initial_counter
    
	 #Saves the game
    def save_game(self,name_of_file):
        outfile = open(name_of_file, 'w')
        
        #Writes horizontal lines
        for row in range (0, grid_height):
            for column in range (0, grid_width-1):
                outfile.write(str(self.horizontal_lines[row][column]))
                outfile.write(",")
            outfile.write("\n")
            
        #Writes vertical lines
        for row in range (0, grid_height):
            for column in range (0, grid_width-1):
                outfile.write(str(self.vertical_lines[row][column]))
                outfile.write(",")
            outfile.write("\n")   
        
        #Writes initials
        for row in range (0, grid_height - 1):
            for column in range (0, grid_width - 1):
                outfile.write(self.initials[row][column])
                outfile.write(",")
            outfile.write("\n")
            
        outfile.write(self.computer_initial)
        
        outfile.write("\n")
        
        outfile.write(self.player_initial)
            
        outfile.close()
        
                