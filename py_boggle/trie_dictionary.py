import typing
from typing import Optional, Dict
from collections.abc import Iterator

from py_boggle.boggle_dictionary import BoggleDictionary


class TrieNode:
    """
    Our TrieNode class. Feel free to add new properties/functions, but 
    DO NOT edit the names of the given properties (children and is_word).
    """
    def __init__(self):
        self.children : Dict[str, TrieNode] = {} # maps a child letter to its TrieNode class
        self.is_word = False # whether or not this Node is a valid word ending




class TrieDictionary(BoggleDictionary):
    """
    Your implementation of BoggleDictionary.
    Several functions have been filled in for you from our solution, but you are free to change their implementations.
    Do NOT change the name of self.root, as our autograder will manually traverse using self.root
    """

    def __init__(self):
        self.root : TrieNode = TrieNode()

    def load_dictionary(self, filename: str) -> None:
        # Remember to add every word to the trie, not just the words over some length.
        with open(filename) as wordsfile:
            for line in wordsfile:
                word = line.strip().lower()
                # Do something with word
                current_node = self.root
                for letter in word:
                    if letter not in current_node.children:
                        current_node.children[letter] = TrieNode()
                    current_node = current_node.children[letter]
                current_node.is_word = True


        return None


        raise NotImplementedError("method load_dictionary") # TODO: implement your code here

    def traverse(self, prefix: str) -> Optional[TrieNode]:
        """
        Traverse will traverse the Trie down a given path of letters `prefix`.
        If there is ever a missing child node, then returns None.
        Otherwise, returns the TrieNode referenced by `prefix`.
        """

        current_node = self.root
        for letter in prefix:
            if letter not in current_node.children:
                return None
            current_node = current_node.children[letter]
        return current_node



        raise NotImplementedError("method traverse") # TODO: implement your code here

    def is_prefix(self, prefix: str) -> bool:
        current_node = self.traverse(prefix)
        if current_node is not None:
            return True
        else:
            return False

        raise NotImplementedError("method is_prefix") # TODO: implement your code here

    def contains(self, word: str) -> bool:
        current_node = self.traverse(word)
        if current_node is not None and current_node.is_word:
            return True
        else:
            return False

        raise NotImplementedError("method contains") # TODO: implement your code here

    def __iter__(self) -> typing.Iterator[str]:


        raise NotImplementedError("method __iter__") # TODO: implement your code here

dic = TrieDictionary()
dic.load_dictionary("C:/Users/sangmin/Desktop/assignment/DSA/boggle-dorororong-main/words.txt")
# print(dic.root.children['a'].children['a'].children['b'].is_word)