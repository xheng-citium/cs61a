#!/usr/bin/python3

import unittest, pdb
from scheme_reader import nil, Pair, scheme_read, read_line
from ucb import main, trace, interact
from scheme_tokens import tokenize_lines, DELIMITERS
from buffer import Buffer, InputReader, LineReader

class scheme_reader(unittest.TestCase):
    def test_scheme_read(self):    
        lines = ["(+ 1 ", "(+ 23 4)) ("]
        src = Buffer(tokenize_lines(lines))
        self.assertEqual( str(scheme_read(src)), "(+ 1 (+ 23 4))")
        
        line = read_line("'hello")
        self.assertEqual(repr(line), "Pair('quote', Pair('hello', nil))")
        
        line = read_line("(car '(1 2))")
        self.assertEqual( str(line), "(car (quote (1 2)))")
        


if __name__ == "__main__":
    unittest.main()
