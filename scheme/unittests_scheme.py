#!/usr/bin/python3

import unittest, pdb
from scheme_reader import nil, Pair, scheme_read, read_line, read_tail
import scheme
from scheme_primitives import SchemeError, PrimitiveProcedure, scheme_add, scheme_oddp
from ucb import main, trace, interact
from scheme_tokens import tokenize_lines
from buffer import Buffer

class part_1(unittest.TestCase):
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
        self.assertEqual(lst, nil)
        lst = read_tail(Buffer(tokenize_lines(["2 3)"])))
        self.assertEqual(lst, Pair(2, Pair(3, nil)))
        lst = read_tail(Buffer(tokenize_lines(["2 (3 4))"])))
        self.assertEqual(lst, Pair(2, Pair(Pair(3, Pair(4, nil)), nil)))
        self.assertRaises(SyntaxError, read_line, "(1 2")
        SyntaxError
 
        # testing dots
        self.assertEqual( read_line("(1 . 2)"), Pair(1, 2))
        self.assertEqual( read_line("(1 2 . 3)"), Pair(1, Pair(2, 3)))
        self.assertRaises( SyntaxError, read_line, "(1 . 2 3)")
        lst = scheme_read( Buffer(tokenize_lines(["(1", "2 .", "'(3 4))", "4"])))
        self.assertEqual( lst, Pair(1, Pair(2, Pair('quote', Pair(Pair(3, Pair(4, nil)), nil)))))
        
        self.assertRaises( SyntaxError, read_line, "(2 . 3 4 . 5)")
        self.assertEqual( read_line("(2 (3 . 4) 5)"), Pair(2, Pair(Pair(3, 4), Pair(5, nil))))
        lst = read_line("(hi there . (cs . (student)))")
        self.assertEqual( lst, Pair('hi', Pair('there', Pair('cs', Pair('student', nil)))))
        self.assertEqual( read_line("(1 (9 8) . 7)"), Pair(1, Pair(Pair(9, Pair(8, nil)), 7)))
        
        # NB I have also successfully run scheme_read tests at the end of part 1. Some are included above

class phase_2(unittest.TestCase):
    def test_apply_primitive(self):
        env = scheme.create_global_frame()
        plus = env.bindings["+"]
        twos = Pair(2, Pair(2, nil))
        self.assertEqual( scheme.apply_primitive(plus, twos, env), 4)        
        
        env = scheme.create_global_frame()
        plus = PrimitiveProcedure(scheme_add) 
        self.assertEqual( scheme.scheme_apply(plus, twos, env), 4)
        
        env = scheme.create_global_frame()
        oddp = PrimitiveProcedure(scheme_oddp) # odd? procedure
        self.assertRaises(SchemeError, scheme.scheme_apply, oddp, twos, env) # twos is not a scalar
    
    def test_lookup(self):        
        first_frame = scheme.create_global_frame()
        first_frame.define("x", 3)
        second_frame = scheme.Frame(first_frame)
        second_frame.define("y", 4)
        self.assertEqual(second_frame.parent, first_frame)
        self.assertEqual(second_frame.lookup("y"), 4)
        self.assertEqual(second_frame.lookup("x"), 3)
        self.assertRaises(SchemeError, second_frame.lookup, "z") # z does not exist

        first_frame.define("x", 5) # change x value, parent bindings dict is updated
        self.assertEqual(second_frame.lookup("x"), 5)
        second_frame.define("x", 6) # x in parent bindings is masked by x in second_frame
        self.assertEqual(second_frame.lookup("x"), 6)
    
    def test_do_define_form(self):
        expr = read_line("(+ 2 (- 3) )")
        self.assertEqual( scheme.scheme_eval(expr, scheme.create_global_frame()), -1)      
        
        #result = eval('''(define pi 3.14159)
        #(define radius 10)
        #(* pi (* radius radius)) ''')
        #self.assertEqual(result, 314.159)
        #self.assertRaises(SchemeError, eval, "(define 0 1)")
        
        vals = Pair('size', Pair(2, nil))
        env = scheme.create_global_frame()
        self.assertEqual( scheme.do_define_form(vals, env), "size")
        self.assertEqual( env.lookup("size"), 2)

    def test_do_quote_form(self):
        self.assertEqual(scheme.do_quote_form(Pair("x", nil)), "x")
        self.assertEqual(scheme.do_quote_form(Pair("(1 . 2)", nil)), "(1 . 2)")
        line = "(1 (2 three . (4 . 5)))"
        self.assertEqual( scheme.do_quote_form( Pair(line, nil)), line)

    def test_do_begin_form(self):  
        #eval("(begin 30 'hello)")
        #'hello'
        #eval("(begin (define x 3) (cons x '(y z)))")
        #Pair(3, Pair('y', Pair('z', nil)))
        return

    def test_do_lambda_form(self):
        return


if __name__ == "__main__":
    unittest.main()
