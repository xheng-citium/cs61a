#!/usr/bin/python3

import unittest, pdb
from scheme_reader import nil, Pair, scheme_read, read_line, read_tail
import scheme
from scheme_primitives import SchemeError, PrimitiveProcedure, scheme_add, scheme_oddp
from ucb import main, trace, interact
from scheme_tokens import tokenize_lines
from buffer import Buffer  

"""Notes
  More cases are in tests.scm
"""

class part_1(unittest.TestCase):
    def test_scheme_read(self):    
        lines = ["(+ 1 ", "(+ 23 4)) ("]
        src = Buffer(tokenize_lines(lines))
        self.assertEqual("(+ 1 (+ 23 4))", str(scheme_read(src)) ) # from doctest
        
        res = read_line("'hello")
        self.assertEqual(Pair('quote', Pair('hello', nil)), res)
        res = read_line("(car '(1 2))")
        self.assertEqual( "(car (quote (1 2)))", str(res))
        
        res = read_line("(a (b 'c))")
        self.assertEqual(Pair('a', Pair(Pair('b', Pair(Pair('quote', Pair('c', nil)), nil)), nil)), res)
        res = read_line("(a (b '(c d)))" )
        self.assertEqual(Pair('a', Pair(Pair('b', Pair(Pair('quote', Pair(Pair('c', Pair('d', nil)), nil)), nil)), nil)), res)
        self.assertRaises(SyntaxError, read_line, "')")
        
        self.assertEqual(1, read_line("1 . 2")); # no parenthesis should not raise Error at this stage 

    def test_read_tail(self):  
        res = read_tail(Buffer(tokenize_lines([")"])))
        self.assertEqual(nil, res)
        
        res = read_tail(Buffer(tokenize_lines(["2 3)"])))
        self.assertEqual(Pair(2, Pair(3, nil)), res)
        
        self.assertRaises(SyntaxError, read_tail, Buffer(tokenize_lines(["2 3"])) )

        res = read_tail(Buffer(tokenize_lines(["2 (3 4))"])))
        self.assertEqual( Pair(2, Pair(Pair(3, Pair(4, nil)), nil)), res)
 
        # testing dots
        self.assertRaises( SyntaxError, read_line, "(1 . )")

        self.assertEqual( Pair(1, 2), read_line("(1 . 2)"))
        self.assertEqual( Pair(1, 2), read_line(" ( 1  .  2 ) ")) # extra space is ok
        self.assertEqual( Pair(1, Pair(2, 3)), read_line("(1 2 . 3)"))
        self.assertRaises( SyntaxError, read_line, "(1 . 2 3)")

        res = scheme_read( Buffer(tokenize_lines(["(1", "2 .", "'(3 4))", "4"])))
        self.assertEqual( Pair(1, Pair(2, Pair('quote', Pair(Pair(3, Pair(4, nil)), nil)))), res)
        
        self.assertRaises( SyntaxError, read_line, "(2 . 3 4 . 5)")
        self.assertEqual( Pair(2, Pair(Pair(3, 4), Pair(5, nil))),read_line("(2 (3 . 4) 5)") )

        res = read_line("(hi there . (cs . (student)))")
        self.assertEqual( Pair('hi', Pair('there', Pair('cs', Pair('student', nil)))), res)
        self.assertEqual( Pair(1, Pair(Pair(9, Pair(8, nil)), 7)), read_line("(1 (9 8) . 7)"))
        

class part_2(unittest.TestCase):
    def test_apply_primitive(self):     
        env = scheme.create_global_frame()
        four = Pair(4, nil)
        proc = PrimitiveProcedure(scheme.scheme_eval, True)
        self.assertTrue(proc.use_env)
        self.assertEqual(4, scheme.scheme_apply(proc, four, env))
 
        env = scheme.create_global_frame()
        proc = PrimitiveProcedure(scheme.scheme_eval, False)
        self.assertFalse(proc.use_env)
        self.assertRaises(SchemeError, scheme.scheme_apply,proc, four, env) # scheme.eval needs use_env = True

        env = scheme.create_global_frame()
        plus = env.bindings["+"]
        twos = Pair(2, Pair(2, nil))
        self.assertEqual(4, scheme.apply_primitive(plus, twos, env))        
        
        env = scheme.create_global_frame()
        plus = PrimitiveProcedure(scheme_add) 
        self.assertEqual(4, scheme.scheme_apply(plus, twos, env))
        
        env = scheme.create_global_frame()
        oddp = PrimitiveProcedure(scheme_oddp) # odd? procedure
        self.assertRaises(SchemeError, scheme.scheme_apply, oddp, twos, env) # twos is not a scalar
    
    def test_lookup(self):        
        first_frame = scheme.create_global_frame()
        first_frame.define("x", 3)
        second_frame = scheme.Frame(first_frame)
        second_frame.define("y", 4)
        self.assertEqual(first_frame, second_frame.parent)
        self.assertEqual(4, second_frame.lookup("y"))
        self.assertEqual(3, second_frame.lookup("x"))
        self.assertRaises(SchemeError, second_frame.lookup, "z") # z does not exist

        first_frame.define("x", 5) # change x value, parent bindings dict is updated
        self.assertEqual(5, second_frame.lookup("x"))

        second_frame.define("x", 6) # x in parent bindings is masked by x in second_frame
        self.assertEqual(6, second_frame.lookup("x"))
        self.assertEqual(5, first_frame.lookup("x"))
    
    def test_do_define_form(self):
        # first phase of do_define_form 
        vals = Pair('size', Pair(2, nil))
        env = scheme.create_global_frame()
        self.assertEqual( "size", scheme.do_define_form(vals, env))
        self.assertEqual( 2, env.lookup("size"))
        
    def test_do_quote_form(self):
        self.assertEqual( "x", scheme.do_quote_form(Pair("x", nil)) )
        self.assertEqual( "(1 . 2)", scheme.do_quote_form(Pair("(1 . 2)", nil)) )

        line = "(1 (2 three . (4 . 5)))"
        self.assertEqual( line, scheme.do_quote_form( Pair(line, nil)) )
        self.assertRaises( SchemeError, scheme.do_quote_form, Pair(line, Pair(2, nil)) )
        
        self.assertRaises( SchemeError, scheme.do_quote_form, Pair(2, 2) ) # invalid scheme list

    def test_do_begin_form(self):  
        #eval("(begin 30 'hello)")
        #'hello'
        #eval("(begin (define x 3) (cons x '(y z)))")
        #Pair(3, Pair('y', Pair('z', nil)))
        return

    def test_do_lambda_form(self):
        return

    def test_make_call_frame(self):  
        global_frame = scheme.create_global_frame()
        formals, vals = read_line("(a b c)"), read_line("(1 2 3)")
        frame = global_frame.make_call_frame(formals, vals)
        self.assertEqual(repr(frame), "<{a: 1, b: 2, c: 3} -> <Global Frame>>")
        self.assertEqual(repr(frame.parent), "<Global Frame>") # frame's parent is global_frame 
        
        formals, vals = read_line("(a b c)"), read_line("(1 2 3 4)")
        self.assertRaises(SchemeError, global_frame.make_call_frame, formals, vals)
        formals, vals = read_line("(a b c)"), read_line("(1 2)")
        self.assertRaises(SchemeError, global_frame.make_call_frame, formals, vals)
    
    def test_check_formals(self):
        scheme.check_formals(read_line("(a b c)")) # run successfully 
        formals = ("(x #t z)")
        self.assertRaises(SchemeError, scheme.check_formals, formals) # #t is not valid symbol

        formals = read_line("(a b c b)")
        self.assertRaises( SchemeError, scheme.check_formals,formals)
        formals = read_line("(a . b)")
        self.assertRaises( SchemeError, scheme.check_formals,formals)

    def test_do_and_or_forms(self):

        # do_and_form: return the last sub expr regardless of True or False
        global_frame = scheme.create_global_frame()
        val = scheme.do_and_form(read_line("(4 5 6)"), global_frame)
        self.assertEqual(val, 6 )
        val = scheme.do_and_form(read_line("(4 5 (= 2 3))"), global_frame)
        self.assertEqual(val, Pair("=", Pair(2, Pair(3, nil))))
        
        # do_or_form: return the last sub expr regardless True or False
        global_frame = scheme.create_global_frame()
        val = scheme.do_or_form(read_line("(#f (> 2 3) (= 2 2))"), global_frame)
        self.assertEqual(val, Pair("=", Pair(2, Pair(2, nil))))
        val = scheme.do_or_form(read_line("(#f #f (> 2 3))"), global_frame)
        self.assertEqual(val, Pair(">", Pair(2, Pair(3, nil))))
        
        # short circuiting and must be preceded by "quote"
        val = scheme.do_or_form(read_line("(5 2 1)"), global_frame)
        self.assertEqual(str(val), "(quote 5)")
        val = scheme.do_or_form(read_line("(#t 2 1)"), global_frame)
        self.assertEqual(str(val), "(quote True)")

    def test_do_let_form(self):
        env = scheme.create_global_frame()
        result = scheme.scheme_eval(read_line("(let ((x 42) (y (* 5 10))) (list x y)) "), env)
        self.assertEqual(str(result), "(42 50)")
        result = scheme.scheme_eval(read_line("(let ((a 1) (b a)) b)"), env)
        self.assertEqual(result, 1)
        
        # SchemeError: too many operands, too few operands, invalid symbol, unknown symbol
        self.assertRaises(SchemeError, scheme.scheme_eval, read_line("(let ((a 1 1)) a)"), env)
        self.assertRaises(SchemeError, scheme.scheme_eval, read_line("(let ((a 1) (b)) a)"), env)
        self.assertRaises(SchemeError, scheme.scheme_eval, read_line("(let ((a 1) (2 2)) a)"), env) 
        self.assertRaises(SchemeError, scheme.scheme_eval, read_line("(let ((a 1) (b 2)) c)"), env) 
        

if __name__ == "__main__":
    unittest.main()


