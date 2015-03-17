#!/usr/bin/python3

import unittest, pdb
from scheme_reader import nil, Pair, scheme_read, read_line, read_tail
from ucb import main, trace, interact
from scheme_tokens import tokenize_lines, DELIMITERS
from buffer import Buffer, InputReader, LineReader

class scheme_reader(unittest.TestCase):
    def test_scheme_read(self):    
        lines = ["(+ 1 ", "(+ 23 4)) ("]
        src = Buffer(tokenize_lines(lines))
        self.assertEqual( str(scheme_read(src)), "(+ 1 (+ 23 4))")
        
        lst = read_line("'hello")
        self.assertEqual(lst, Pair('quote', Pair('hello', nil)))
        lst = read_line("(car '(1 2))")
        self.assertEqual( str(lst), "(car (quote (1 2)))")
        
        lst = read_line("(a (b 'c))")
        self.assertEqual(lst, Pair('a', Pair(Pair('b', Pair(Pair('quote', Pair('c', nil)), nil)), nil)))
        lst = read_line("(a (b '(c d)))" )
        self.assertEqual(lst, Pair('a', Pair(Pair('b', Pair(Pair('quote', Pair(Pair('c', Pair('d', nil)), nil)), nil)), nil)))
        self.assertRaises(SyntaxError, read_line, "')")

    def test_read_tail(self):  
        lst = read_tail(Buffer(tokenize_lines([")"])))
        self.assertEqual(repr(lst), "nil")
        lst = read_tail(Buffer(tokenize_lines(["2 3)"])))
        self.assertEqual(lst, Pair(2, Pair(3, nil)))
        lst = read_tail(Buffer(tokenize_lines(["2 (3 4))"])))
        self.assertEqual(lst, Pair(2, Pair(Pair(3, Pair(4, nil)), nil)))
        self.assertEqual(read_line("(1 . 2)"), Pair(1, 2))
        self.assertEqual(read_line("(1 2 . 3)"), Pair(1, Pair(2, 3)))
        
        # testing dots
        self.assertRaises(SyntaxError, read_line, "(1 . 2 3)")
        lst = scheme_read(Buffer(tokenize_lines(["(1", "2 .", "'(3 4))", "4"])))
        self.assertEqual(lst, Pair(1, Pair(2, Pair('quote', Pair(Pair(3, Pair(4, nil)), nil)))))

        


if __name__ == "__main__":
    unittest.main()
