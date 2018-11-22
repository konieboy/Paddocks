import tkinter
import tkinter.messagebox
import grid
from grid import Grid
from grid import grid_height
from grid import grid_width
import ai
import random
try:
	import winsound
except ImportError:
	print ('Oh dear. Your system does not suport winsound :(')
	
#import winsound

#These are for going through the list of buttons because of the way our game grid is created
ODD_NUMBER = 0.5
VERTICAL_CONSTANT = 1

class PaddocksGUI():
    def __init__(self):
	
	    #adds rules window
		#click to close
        self.rules_window = tkinter.Tk() 
        img = tkinter.PhotoImage(file="Media/img.gif",width=638, height=524) 
        self.rules_close = tkinter.Button(self.rules_window, image=img, command = self.rules_window.destroy)
        self.rules_close.grid(row = 0, column = 0) 
		  
        tkinter.mainloop()

        #Creates another main window as soon as the image is clicked
        self.main_window = tkinter.Tk()
        
        #Default background colour
        self.default_background_colour = self.main_window.cget("bg")
        
        #Creates a game grid
        self.game_grid = Grid()
        
        #Adds the save, load, quit, and reset buttons
        save_load_quit_reset_menu = self.create_menu()
        
        #Title, You and Opponent texts on the screen
        game_label = tkinter.Label(self.main_window, text = "-=Welcome to Paddocks=- \n *************************************", font=('Impact',28))
        player_initial_label = tkinter.Label(self.main_window, text = " You " , font=('Comic Sans MS',20), fg='blue')
        computer_initial_label = tkinter.Label(self.main_window, text = "Opponent" , font=('Comic Sans MS',19), fg='red')
        
        #Creates a game frame
        self.game_frame = self.create_grid()
        
        #Puts the labels and the grids in the appropriate positions
        game_label.grid(row = 0, column = 1)
        save_load_quit_reset_menu.grid(row=4, column=1)
        player_initial_label.grid(row=3, column=0)
        computer_initial_label.grid(row=3, column=2)
        self.game_frame.grid(row= 3, column = 1)
        
        #Decides who starts first 
        self.starts_first()
        
        #Graphics loop
        tkinter.mainloop()

    #Randomly choose who starts first
    def starts_first(self):
        first = random.randint(0,1)
        #if 0, ai goes first. if 1, the player goes first
        if first==0:
            self.button_clicked()
  
    #Creates the game grid          
    def create_grid(self):
        frame = tkinter.Frame(self.main_window)
        
        #Two lists for the vertical/horizontal buttons and initials
        buttons = []
        self.initial_buttons = []
        grid = Grid()
        
        #Creates the grid
        for row in range(0,grid_height*2 - 1):
            row_list = []
            initial_row_list = []
            for column in range(0,grid_width*2 - 1):
                if(row%2 == 0):
                    self.dot = tkinter.Label(frame, text = ' . ', font = ('Helvetica', 30)) #Initializes the dot
                    
                    #Dots
                    if (column%2 == 0):
                        self.dot.grid(row = row, column = column)
                        
                    #Horizontal buttons
                    else:
                        button = tkinter.Button(frame, width = 9,height = 1, padx = 10, bg = 'ghost white', command = lambda \
                                                    brow = int(row/2), bcolumn = int(column/2 - ODD_NUMBER): 
                                                    self.h_button_clicked(brow, bcolumn))
                        button.grid(row = row, column = column)
                        
                        #Append the button into a list
                        row_list.append(button)
                else:
                    #Vertical buttons
                    if(column%2 == 0):
                        button = tkinter.Button(frame, width = 2, height = 5, bg = 'ghost white', command = lambda \
                                                    brow = int(row/2 - ODD_NUMBER), bcolumn = int(column/2): \
                                                    self.v_button_clicked(brow, bcolumn))
                        button.grid(row = row,column = column)
                        
                        #Append the button into a list
                        row_list.append(button)
                    else:
                        button = tkinter.Button(frame, state = 'disabled', width = 10, height = 5)
                        button.grid(row = row, column = column)
                        
                        #append the button into a list
                        initial_row_list.append(button)
                        
            #Appends the buttons in a row into a list
            buttons.append(row_list)
            
            #Appends the initial buttons only if it actually created some.
            if row % 2 == 1:
                self.initial_buttons.append(initial_row_list)         
            
        self.buttons = buttons
        self.game_grid = grid
        return frame

    #Creates the Save, Load, Quit buttons and adds their functions
    def create_menu(self) :
        #Creates new frame
        frame = tkinter.Frame(self.main_window)
        
        #Save button
        self.save_button = tkinter.Button(frame, width = 10, height = 2, \
                                         text='Save', \
                                         command = self.save)
                                         
        #Load button
        self.load_button = tkinter.Button(frame, width = 10, height = 2, \
                                         text='Load', \
                                         command = self.load)
                                         
        #Quit button
        quit_button = tkinter.Button(frame, \
                                         text='Quit', width = 10, height = 2, \
                                         command = self.main_window.destroy)
                                         
        #Reset button
        reset_button = tkinter.Button(frame, \
                                         text='Reset', width = 10, height = 2, \
                                         command = self.reset)
        
        #Puts them on the main window
        self.save_button.grid(row=0,column=0)
        self.load_button.grid(row=0,column=1)
        reset_button.grid(row=0,column=2)
        quit_button.grid(row=0,column=3)
        
        return frame
        
    #Function behind the save button.
    def save(self):
        #Opens a new window which asks for the filename
        self.save_main = tkinter.Tk()
        
        #Text appearing on the screen
        self.instruct = tkinter.Label(self.save_main, text ='Write the name of the file you wish to save: ')
        self.instruct.grid(row=0, column = 0)
        
        #White space to get input for user
        self.entry = tkinter.Entry(self.save_main)
        self.entry.grid(row = 1, column = 0)
              
        #Function behind the save and quit buttons
        b = tkinter.Button(self.save_main, text = 'Save', command=self.save_file)
        b2 = tkinter.Button(self.save_main, text = 'Quit', command=self.save_main.destroy)
 
        #Places the buttons in the proper place
        b.grid(row = 1, column = 1)
        b2.grid(row = 1, column = 2)
     
    #Function behind the save button in the save button window
    def save_file(self):
        #Gets the text inputed by the user
        text = self.entry.get()
        
        #Saves the game with the file name specified
        self.game_grid.save_game(text)
        
        #Destroys the window
        self.save_main.destroy()
     
    #Function behind the load button.
    def load(self):
        #Opens a new window which asks for the filename
        self.load_main = tkinter.Tk()
        
        #Instructions
        self.instruct = tkinter.Label(self.load_main, text = 'Write the name of the file you wish to load: ')
        self.instruct.grid(row = 0, column =0)
        
        #White space to get input from the user
        self.file_load = tkinter.Entry(self.load_main)
        self.file_load.grid(row = 1, column = 0)

        
        #Function behind the load and quit buttons
        b = tkinter.Button(self.load_main, text = 'Load', command=self.load_file)
        b2 = tkinter.Button(self.load_main, text = 'Quit', command=self.load_main.destroy)

        #Places the buttons in the proper place
        b.grid(row = 1, column = 1)
        b2.grid(row = 1, column = 2)
      
    #Function behind the load button in the load button window
    def load_file(self):
        #Gets the input of the user
        text = self.file_load.get()
        
        #Loads the grid if it exists
        try:
            self.game_grid = Grid(text)
        except:
           tkinter.messagebox.showinfo('Load Error', 'There is no file named ' + text + '. Please try again.')
           self.load_main.destroy()
           self.load()
           return()
        
        #Destroys the window
        self.load_main.destroy()
        
        #Changes the strings to ints
        for row in range (0,grid_height):
            for column in range (0,grid_width - 1):
                self.game_grid.horizontal_lines[row][column] = int(self.game_grid.horizontal_lines[row][column])
                self.game_grid.vertical_lines[row][column] = int(self.game_grid.vertical_lines[row][column])
                
        #Changes the horizontal buttons accordingly
        for row in range (0,grid_height):
            for column in range (0,grid_width - 1):
                button = self.buttons[row*2][column]
                if self.game_grid.horizontal_lines[row][column] == 1:
                    button['bg'] = 'Black'
                    button['state'] = 'disabled'
                else:
                    button['bg'] = 'ghost white'
                    button['state'] = 'active'
                    
        #Changes the vertical buttons accordingly
        for column in range (0,grid_height):
            for row in range (0,grid_width - 1):
                button = self.buttons[row*2 + VERTICAL_CONSTANT][column]
                if self.game_grid.vertical_lines[column][row] == 1:
                    button['bg'] = 'Black'
                    button['state'] = 'disabled'
                else:
                    button['bg'] = 'ghost white'
                    button['state'] = 'active'
                    
        #Changes the initial/colour boxes
        for row in range (0,grid_height - 1):
            for column in range (0,grid_width - 1):
                button = self.initial_buttons[row][column]
                if self.game_grid.initials[row][column] == 'A':
                    button['bg'] = 'Blue'
                elif self.game_grid.initials[row][column] == 'C':
                    button['bg'] = 'Red'
                else:
                    button['bg'] = self.default_background_colour
	
	#resets the entire grid
    def reset(self):
        #Resets horizontal lines
        for row in range (0,grid_height):
            for column in range (0,grid_width - 1):
                button = self.buttons[row*2][column]
                button['bg'] = 'ghost white'
                button['state'] = 'active'
                self.game_grid.horizontal_lines[row][column] = 0 # this resets the actual number grid
                
        #Resets the vertical buttons accordingly
        for column in range (0,grid_height):
            for row in range (0,grid_width - 1):
                button = self.buttons[row*2 + VERTICAL_CONSTANT][column]
                button['bg'] = 'ghost white'
                button['state'] = 'active'
                self.game_grid.vertical_lines[column][row] = 0
                
        #Resets the initial/colour boxes
        for row in range (0,grid_height - 1):
            for column in range (0,grid_width - 1):
                button = self.initial_buttons[row][column]
                button['bg'] = self.default_background_colour    
                self.game_grid.initials[row][column] = " " 
        #enables the save button
        self.save_button['state'] = 'active'    
        
        #Randomly chooses who goes first
        self.starts_first()
        
    #Plays sound
    def sound(self,filename):
        try:
            winsound.PlaySound(filename, winsound.SND_ALIAS |winsound.SND_ASYNC ) 
        except:
            print("Music is not supported")											
													
    #If a horizontal button is clicked
    def h_button_clicked(self, row, column):
		#sound when you click a horizontal button
        self.sound("Media/click.wav") 	
        
        #Finds the position of the line clicked in the horizontal list
        self.game_grid.placing_line(row, column, 'horizontal')
        
        #Changes the text of the button and disables it.
        button = self.buttons[row*2][column]
        button['bg'] = 'Black'
        button['state'] = 'disabled'
        
        #Sets the initials and checks to see if you can go again
        go_again = self.setting_initial(self.game_grid.player_initial)
        
        #Ai's turn if the game is not over
        if not go_again:
            self.button_clicked()
            
        elif self.game_over():
            self.announce_winner()
      
    #If a vertical button is clicked
    def v_button_clicked(self,row,column):
		#sound when you click a vertical button
        self.sound("Media/click.wav")
			
        #Finds the position of the line clicked in the vertical list
        self.game_grid.placing_line(row, column, 'vertical')
        
        #Changes the text of the button and disables it
        button = self.buttons[row* 2 + VERTICAL_CONSTANT][column]
        button['bg'] = 'Black'
        button['state'] = 'disabled'
        
        #Sets the initials and checks to see if you can go again
        go_again = self.setting_initial(self.game_grid.player_initial)
        
        #Ai's turn if the game is not over
        if not go_again:
            self.button_clicked()
            
        elif self.game_over():
            self.announce_winner()

    #sets the colours of the boxes and checks to see if you can go again.
    def setting_initial(self,initial):
        self.game_grid.putting_initial(initial)

        #For going again if you complete a box
        go_again = False
        
        #Goes through the grid and changes the colour of the squares who have been completed
        for row_index in range (0,grid.grid_height - 1):
            for column_index in range (0,grid.grid_width - 1):
                ini = self.game_grid.initials[row_index][column_index]
                button = self.initial_buttons[row_index][column_index]
                if ini == 'A' and button['bg'] != 'Blue': #Changes colour to blue, makes a sound and you get to go again
                    button['bg'] = 'Blue'
                    self.sound("Media/score.wav") #Makes a sound when you finish a box
                    go_again = True #You can go again
                elif ini == 'C' and button['bg'] != 'Red': #Changes colour to red and the ai get's to go again
                    button['bg'] = 'Red'
                    go_again = True #Ai can go again
        return go_again
        
    #If either of button types is clicked, it goes to this. Triggers the ai's turn.
    def button_clicked(self):
        #If the game is over, it will display the score.
        if self.game_over():
            self.announce_winner()     
            
        else:
            #Get's ai's input and changes the correct list associated with the line
            self.ai_turn()
    
    #Ai's turn
    def ai_turn(self):
        row, column, direction = ai.ai_input(0,0,self.game_grid)
        
        self.game_grid.placing_line(row, column, direction)

        #If direction is horizontal, it will change a horizontal button
        if direction == 'horizontal':
            button = self.buttons[row*2][column]
            button['bg'] = 'Black'
            button['state'] = 'disabled'
        
        #If direction is vertical, it will change a vertical button
        else:
            button = self.buttons[row*2 + VERTICAL_CONSTANT][column]
            button['bg'] = 'Black'
            button['state'] = 'disabled'
       
        go_again = self.setting_initial(self.game_grid.computer_initial)
        
        #Going again for the ai if it finishes a square
        while go_again:
            #It will go again unless the game is over
            if self.game_over():
                self.announce_winner()
                go_again = False
                
            else:
                go_again = False
                self.ai_turn()        

    #Checks to see if game is over
    def game_over(self):
        return self.game_grid.game_end()
    
    #Announces the winner
    def announce_winner(self):
        player_score, ai_score = self.game_grid.victory() #Counts the score of each player
        self.save_button['state'] = 'disabled' #Disables the save button
        
        #Plays ending music
        if player_score > ai_score:
           self.sound("Media/win.wav")
           winner = "You win!"
        else:
           self.sound("Media/lose.wav")
           winner = "You lose!"
     
        tkinter.messagebox.showinfo('Game Over!' , (winner + "\n\nYour score: " + str(player_score) + \
                                                    "\nComputer's score: " + str(ai_score))) #Shows score
        

               
gui = PaddocksGUI()