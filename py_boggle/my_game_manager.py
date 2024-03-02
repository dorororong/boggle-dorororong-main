import copy
import random
from typing import List, Optional, Set, Tuple

from py_boggle.boggle_dictionary import BoggleDictionary
from py_boggle.boggle_game import BoggleGame

"""
************** READ THIS ***************
************** READ THIS ***************
************** READ THIS ***************
************** READ THIS ***************
************** READ THIS ***************

If you worked in a group on this project, please type the EIDs of your groupmates below (do not include yourself).
Leave it as TODO otherwise.
Groupmate 1: TODO
Groupmate 2: TODO
"""

SHORT = 3
CUBE_SIDES = 6

class MyGameManager(BoggleGame):
    """Your implementation of `BoggleGame`
    """

    def __init__(self):
        """Constructs an empty Boggle Game.

        A newly-constructed game is unplayable.
        The `new_game` method will be called to initialize a playable game.
        Do not call `new_game` here.

        This method is provided for you, but feel free to change it.
        """

        self.board: List[List[str]] # current game board
        self.size: int # board size
        self.words: List[str] # player's current words
        self.dictionary: BoggleDictionary # the dictionary to use
        self.last_added_word: Optional[List[Tuple[int, int]]] # the position of the last added word, or None

    def new_game(self, size: int, cubefile: str, dictionary: BoggleDictionary) -> None:
        """This method is provided for you, but feel free to change it.
        """
        with open(cubefile, 'r') as infile:
            faces = [line.strip() for line in infile]
        cubes = [f.lower() for f in faces if len(f) == CUBE_SIDES]
        if size < 2 or len(cubes) < size*size:
            raise ValueError('ERROR: Invalid Dimensions (size, cubes)')
        random.shuffle(cubes)
        # Set all of the game parameters
        self.board =[[random.choice(cubes[r*size + c]) 
                    for r in range(size)] for c in range(size)]
        self.size = size
        self.words = []
        self.dictionary = dictionary
        self.last_added_word = None


    def get_board(self) -> List[List[str]]:
        """This method is provided for you, but feel free to change it.
        """
        return self.board

    def eight_way_search(self,used, word, coords):
        size = self.size
        if not word:
            return coords
        start_r, start_c = coords[-1]
        next_letter = word[0]
        for r in range(start_r - 1, start_r + 2):
            for c in range(start_c - 1, start_c + 2):
                if (r >= 0 and r < size and c >= 0 and c < size):
                    if self.board[r][c] == next_letter and (r, c) not in used:
                        new_used = used + [(r, c)]
                        new_coords = coords + [(r, c)]
                        if len(word) == 1:
                            return new_coords
                        else:
                            result = self.eight_way_search(new_used, word[1:], new_coords)
                            if result:
                                return result

        return None

    def find_word_in_board(self, word: str) -> Optional[List[Tuple[int, int]]]:
        """Helper method called by add_word()
        Expected behavior:
        Returns an ordered list of coordinates of a word on the board in the same format as get_last_added_word()
        (see documentation in boggle_game.py).
        If `word` is not present on the board, return None.
        """

        size = self.size

        word = word.lower()
        initial_coords = []

        for r in range(size):
            for c in range(size):
                if self.board[r][c] == word[0]:
                    initial_coords.append((r, c))

        for initial_coord in initial_coords:
            answer = self.eight_way_search([initial_coord], word[1:], [initial_coord])
            if answer:
                return answer
        else:
            return None


        # raise NotImplementedError("method find_word_in_board") # TODO: implement your code here


    def add_word(self, word: str) -> int:
        """This method is provided for you, but feel free to change it.
        """
        word = word.lower()
        if (len(word) > SHORT and word not in self.words and self.dictionary.contains(word)):
            location = self.find_word_in_board(word)
            if location is not None:
                self.last_added_word = location
                self.words.append(word)
                return len(word) - SHORT
        return 0

    def get_last_added_word(self) -> Optional[List[Tuple[int, int]]]:
        """This method is provided for you, but feel free to change it.
        """
        return self.last_added_word

    def set_game(self, board: List[List[str]]) -> None:
        """This method is provided for you, but feel free to change it.
        """
        self.board = [[c.lower() for c in row] for row in board]

    def get_score(self) -> int:
        """This method is provided for you, but feel free to change it.
        """
        return sum([len(word) - SHORT for word in self.words])

    def dictionary_driven_search(self) -> Set[str]:
        """Find all words using a dictionary-driven search.

        The dictionary-driven search attempts to find every word in the
        dictionary on the board.

        Returns:
            A set containing all words found on the board.
        """
        dict_iterator = self.dictionary.__iter__()

        dict_iterator = self.dictionary.__iter__()
        words = []

        for word in dict_iterator:
            if self.find_word_in_board(word):
                words.append(word)

        return set(words)
        
        raise NotImplementedError("method dictionary_driven_search") # TODO: implement your code here

    def board_driven_search(self) -> Set[str]:
        """Find all words using a board-driven search.

        The board-driven search constructs a string using every path on
        the board and checks whether each string is a valid word in the
        dictionary.

        Returns:
            A set containing all words found on the board.
        """

        words = []
        def possible_words_after_word(base_r, base_c, used, word):
            size = self.size
            possible_words = []
            for r in range(base_r - 1, base_r + 2):
                for c in range( base_c - 1,  base_c + 2):
                    if (r >= 0 and r < size and c >= 0 and c < size):
                        if (r, c) not in used and self.dictionary.is_prefix(word + self.board[r][c]):
                            new_word = word + self.board[r][c]
                            possible_words.append([r,c,used+[(r,c)],new_word])
                            if self.dictionary.contains(new_word) and len(new_word)>3:
                                words.append(new_word)
            return possible_words


        for i in range(self.size):
            for j in range(self.size):
                prefixes = possible_words_after_word(i, j, [(i,j)], self.board[i][j])
                if prefixes:
                    while True:
                        prefix = prefixes.pop(0)
                        next = possible_words_after_word(prefix[0], prefix[1], prefix[2], prefix[3])
                        if next:
                            prefixes = prefixes + next
                        if not prefixes:
                            break

        words = set(words)
        return words
        
        # raise NotImplementedError("method board_driven_search") # TODO: implement your code here
