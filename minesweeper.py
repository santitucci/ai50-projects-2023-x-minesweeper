import itertools
import random



class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if self.count == len(self.cells):
          return self.cells

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
          return self.cells
        
    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
       
        The mark_mine function should first check to see if cell is one of the cells included in 
        the sentence.
        If cell is in the sentence, the function should update the sentence so that cell is no   
        longer in the sentence, but still represents a logically correct sentence given that cell 
        is known to be a mine.
        
        If cell is not in the sentence, then no action is necessary.
        
        """
        if cell in self.cells:
          self.cells.remove(cell)
          self.count -= 1


    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that a cell is known to be safe.
        """

        if cell in self.cells:
          self.cells.remove(cell)

          #print("Marking safe", self)

          

class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def cells_arround(self, cell):
        """
        list all cells arround a marked cell
        """
        (i,j) = cell
        surroundings = []
        a = b = c = d = 0

        if i == 0: 
          a = 1
        elif i == self.height-1:
          b = -1
        if j == 0:
          c = 1
        elif j == self.width-1:
          d = -1

        for row in range((i-1+a), i+2+b):
            for col in range((j-1+c), j+2+d):
                if (row,col) != (cell[0], cell[1]):
                    surroundings.append((row,col))


        return surroundings
        
    
        
    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        
        1.the function should mark the cell as one of the moves made in the game.
        """
        self.moves_made.add(cell)
        
        """
        2. The function should mark the cell as a safe cell, updating any sentences that contain the cell as well.
        """
        self.mark_safe(cell)
        """

      
        3. The function should add a new sentence to the AI’s knowledge base, based on the value of cell and count, to indicate that count of the cell’s neighbors are mines. Be sure to only include cells whose state is still undetermined in the sentence.
        """
        # create a list of relevant surrounings
      
        surroundings = self.cells_arround(cell)
        for i in surroundings:
          if i in self.moves_made or i in self.mines or i in self.safes:
            surroundings.remove(i)

        new_sentence = Sentence(surroundings, count)
        if len(surroundings)>0:
          self.knowledge.append(new_sentence)

#        for n in range(len(self.knowledge)):
#          print("knowledge",n, self.knowledge[n])

        """
        4 If, based on any of the sentences in self.knowledge, new cells can be marked as safe or as mines, then the function should do so
        """
        for sentence in self.knowledge:   
          if sentence.known_mines() is not None:
            if len(sentence.known_mines()) > 0:
              copy_mines = sentence.known_mines().copy()
              for cell in copy_mines:
                self.mark_mine(cell)
              self.knowledge.remove(sentence)
          if sentence.known_safes() is not None:
            if len(sentence.known_safes()) > 0:
              copy_safes = sentence.known_safes().copy()
              
              for cell in copy_safes:
                self.mark_safe(cell)
              self.knowledge.remove(sentence)   
        
        for i in self.safes:
          self.mark_safe(i)

        for i in self.mines:
          self.mark_mine(i)
            
        """
        5.If, based on any of the sentences in self.knowledge, new sentences can be inferred (using the subset method described in the Background), then those sentences should be added to the knowledge 
base as well.
        """
    

        
        new_know_bool = True 
        new_knowledge = Sentence( set() ,0)
        rang = len(self.knowledge)
        while new_know_bool: 
          new_know_bool = False 
          new_set_of_cells = set()
          
          for know_i in (self.knowledge):
            
            
            for know_j in (self.knowledge):
              
             
                
                
              if (know_i.cells).issubset(know_j.cells) and know_i.cells != set() and know_i.cells != know_j.cells:
                'check if new knowledge can be infered from existing knowledge'
                new_count = know_j.count - know_i.count
                new_set_of_cells = know_j.cells.difference(know_i.cells)
                print("new set i,j",know_i, know_j, new_set_of_cells)
                new_knowledge = Sentence(new_set_of_cells ,new_count)
                new_know_bool = True 
                self.knowledge.append(new_knowledge)
                if know_i in self.knowledge:
                  self.knowledge.remove(know_i)
                if know_j in self.knowledge:
                  self.knowledge.remove(know_j)
               
                for n in range(len(self.knowledge)):
                  print("Know", n , self.knowledge[n])
                print("new inference", new_knowledge)
              elif (know_j.cells).issubset(know_i.cells) and know_j.cells !=set() and know_i.cells != know_j.cells:
                new_count = know_i.count - know_j.count
                new_set_of_cells = know_i.cells.difference(know_j.cells)
                print("new set j, i",know_j,know_i, new_set_of_cells)
                  
                new_knowledge = Sentence(new_set_of_cells ,new_count)
                new_know_bool = True 
                self.knowledge.append(new_knowledge)
                if know_i in self.knowledge:
                  self.knowledge.remove(know_i)
                if know_j in self.knowledge:
                  self.knowledge.remove(know_j)
                print("new inference", new_knowledge)
            
        for n in range(len(self.knowledge)):
          print("Know", n , self.knowledge[n])
      
        
        
        print("safes", self.safes)
        print("mines", self.mines)
        print("made", self.moves_made)  
            
    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        
        for cell in self.safes:
          if cell not in self.moves_made:
            return cell
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """

        for row in range(self.height):
          for col in range(self.width):
            random_row = random.randrange(self.height-1)
            random_col = random.randrange(self.width-1)
            if (random_row, random_col) not in self.moves_made and (random_row, random_col) not in self.mines and (random_row, random_col) not in self.safes:
              return (random_row, random_col)
        return None

