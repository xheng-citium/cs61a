"""This module implements the core Scheme interpreter functions, including the
eval/apply mutual recurrence, environment model, and read-eval-print loop.
"""
import pdb
from scheme_primitives import *
from scheme_reader import *
from ucb import main, trace

# Notes: utility function summary
#   check_form(expr, min, max = None) checks expr as a list has required length
#   check_formals(formals) checks if it is a valid parameter list, i.e. a Scheme list of symbols
#   scheme_listp(expr) checks if expr is a well formed list
#   scheme_symbolp(symbol) check if it is a valid variable name

##############
# Eval/Apply #
##############

def scheme_eval(expr, env):
    """Evaluate Scheme expression EXPR in environment ENV.

    >>> expr = read_line("(+ 2 2)")
    >>> expr
    Pair('+', Pair(2, Pair(2, nil)))
    >>> scheme_eval(expr, create_global_frame())
    4
    """
    if expr is None:
        raise SchemeError("Cannot evaluate an undefined expression.")

    # Evaluate Atoms
    if scheme_symbolp(expr):
        return env.lookup(expr)
    elif scheme_atomp(expr) or scheme_stringp(expr) or expr is okay:
        return expr

    # All non-atomic expressions are lists.
    if not scheme_listp(expr):
        raise SchemeError("malformed list: {0}".format(str(expr)))
    first, rest = expr.first, expr.second

    # Evaluate Combinations
    if (scheme_symbolp(first) # first might be unhashable
        and first in LOGIC_FORMS):
        return scheme_eval(LOGIC_FORMS[first](rest, env), env)
    elif first == "lambda":
        return do_lambda_form(rest, env)
    elif first == "mu":
        return do_mu_form(rest)
    elif first == "define":
        return do_define_form(rest, env)
    elif first == "quote":
        return do_quote_form(rest)
    elif first == "let":
        expr, env = do_let_form(rest, env)
        return scheme_eval(expr, env)
    else:
        procedure = scheme_eval(first, env)
        args = rest.map(lambda operand: scheme_eval(operand, env))
        return scheme_apply(procedure, args, env)


def scheme_apply(procedure, args, env):
    """Apply Scheme PROCEDURE to argument values ARGS in environment ENV."""
    if isinstance(procedure, PrimitiveProcedure):
        return apply_primitive(procedure, args, env)

    elif isinstance(procedure, LambdaProcedure):
        "*** YOUR CODE HERE ***"
        new_env = procedure.env.make_call_frame(procedure.formals, args)
        return scheme_eval(procedure.body, new_env)
    
    elif isinstance(procedure, MuProcedure):
        "*** YOUR CODE HERE ***"
        new_env = env.make_call_frame(procedure.formals, args)
        return scheme_eval(procedure.body, new_env) # evaluat inside the parent frame

    else:
        raise SchemeError("Cannot call {0}".format(str(procedure)))

def apply_primitive(procedure, args, env):
    """Apply PrimitiveProcedure PROCEDURE to a Scheme list of ARGS in ENV.

    >>> env = create_global_frame()
    >>> plus = env.bindings["+"]
    >>> twos = Pair(2, Pair(2, nil))
    >>> apply_primitive(plus, twos, env)
    4
    """
    "*** YOUR CODE HERE ***"
    py_args = [ a for a in args] # convert a scheme list to a py list 
                                 # list comprehension still works
    if procedure.use_env: 
        py_args.append(env)
    try: 
        return procedure.fn(*py_args)
    except TypeError:
        raise SchemeError("Failed call of the function: %s" % str(procedure.fn))


################
# Environments #
################

class Frame:
    """An environment frame binds Scheme symbols to Scheme values."""

    def __init__(self, parent):
        """An empty frame with a PARENT frame (that may be None)."""
        self.bindings = {}
        self.parent = parent

    def __repr__(self):
        if self.parent is None:
            return "<Global Frame>"
        else:
            s = sorted('{0}: {1}'.format(k,v) for k,v in self.bindings.items())
            return "<{{{0}}} -> {1}>".format(', '.join(s), repr(self.parent))

    def lookup(self, symbol):
        """Return the value bound to SYMBOL.  Errors if SYMBOL is not found."""
        "*** YOUR CODE HERE ***"
        if symbol in self.bindings: 
            return self.bindings[symbol]
        elif self.parent:
            return self.parent.lookup(symbol)
        else:
            raise SchemeError("unknown identifier: {0}".format(str(symbol)))


    def global_frame(self):
        """The global environment at the root of the parent chain."""
        e = self
        while e.parent is not None:
            e = e.parent
        return e

    def make_call_frame(self, formals, vals):
        """Return a new local frame whose parent is SELF, in which the symbols
        in the Scheme formal parameter list FORMALS are bound to the Scheme
        values in the Scheme value list VALS. Raise an error if too many or too
        few arguments are given.

        >>> env = create_global_frame()
        >>> formals, vals = read_line("(a b c)"), read_line("(1 2 3)")
        >>> env.make_call_frame(formals, vals)
        <{a: 1, b: 2, c: 3} -> <Global Frame>>
        """
        "*** YOUR CODE HERE ***"
        # NB: no requirement of formals elements being unique, so do not use check_formals() here
        # First, check both validity and length of vals and formals
        check_form(vals, 0)
        N = len(vals)
        check_form(formals, N, N)
        
        # Second, bind argument and values
        frame = Frame(self) # self is parent of frame
        for sym, v in zip(formals, vals):
            if not scheme_symbolp(sym):
                raise SchemeError("%s is not a valid argument" % str(sym) )
            frame.define(sym, v)
        return frame


    def define(self, sym, val):
        """Define Scheme symbol SYM to have value VAL in SELF."""
        self.bindings[sym] = val


###################################
# LambdaProcedure and MuPorcedure
# They behave more like a struc that holds 
#   the parameters required for eval
####################################

class LambdaProcedure:
    """A procedure defined by a lambda expression or the complex define form."""

    def __init__(self, formals, body, env):
        """A procedure whose formal parameter list is FORMALS (a Scheme list),
        whose body is the single Scheme expression BODY, and whose parent
        environment is the Frame ENV.  A lambda expression containing multiple
        expressions, such as (lambda (x) (display x) (+ x 1)) can be handled by
        using (begin (display x) (+ x 1)) as the body."""
        self.formals = formals
        self.body = body
        self.env = env

    def __str__(self):
        return "(lambda {0} {1})".format(str(self.formals), str(self.body))

    def __repr__(self):
        args = (self.formals, self.body, self.env)
        return "LambdaProcedure({0}, {1}, {2})".format(*(repr(a) for a in args))

class MuProcedure:
    """A procedure defined by a mu expression, which has dynamic scope.
     _________________
    < Scheme is cool! >
     -----------------
            \   ^__^
             \  (oo)\_______
                (__)\       )\/\
                    ||----w |
                    ||     ||
    """

    def __init__(self, formals, body):
        """A procedure whose formal parameter list is FORMALS (a Scheme list),
        whose body is the single Scheme expression BODY.  A mu expression
        containing multiple expressions, such as (mu (x) (display x) (+ x 1))
        can be handled by using (begin (display x) (+ x 1)) as the body."""
        self.formals = formals
        self.body = body

    def __str__(self):
        return "(mu {0} {1})".format(str(self.formals), str(self.body))

    def __repr__(self):
        args = (self.formals, self.body)
        return "MuProcedure({0}, {1})".format(*(repr(a) for a in args))


#################
# Special forms #
#################

def do_lambda_form(vals, env):
    """Evaluate a lambda form with parameters VALS in environment ENV."""
    check_form(vals, 2)
    formals = vals[0] 
    check_formals(formals) # check formals is valid agrument list
    "*** YOUR CODE HERE ***"
    body = prep_body( vals.second )
    return LambdaProcedure(formals, body, env)
    
def do_mu_form(vals):
    """Evaluate a mu form with parameters VALS."""
    check_form(vals, 2)
    formals = vals[0]
    check_formals(formals)
    "*** YOUR CODE HERE ***"
    body = prep_body( vals.second )
    return MuProcedure( formals, body) # env is not needed anymore

def prep_body(rest):
    """helper function for lambda and mu form: prepare BODY expression 
    formals is Pair.first part, rest is Pair.second. Hints from lambda and mu procedures' constructors """
    return rest.first if len(rest) == 1 else Pair("begin", rest)

################################

def do_define_form(vals, env):
    """Evaluate a define form with parameters VALS in environment ENV.
    vals is a Pair object """
    check_form(vals, 2)
    target = vals[0]
    if scheme_symbolp(target):
        check_form(vals, 2, 2) 
        "*** YOUR CODE HERE ***"
        expr = scheme_eval(vals[1], env)

    elif isinstance(target, Pair) and scheme_symbolp(target.first):
        "*** YOUR CODE HERE ***"
        # Use lambda expr to convert "define (fn x y)" to fn lambda (x y) ...
        # Goal is to form an argument list that can be passed to do_lambda_form
        target, formals = target.first, target.second
        arg_list = Pair(formals, vals.second)
        expr = do_lambda_form(arg_list, env)
    else:
        raise SchemeError("bad argument to define")
    
    env.define(target, expr) # bind target and its related expression
    return target

def do_quote_form(vals):
    """Evaluate a quote form with parameters VALS.
    vals is a Pairs object"""
    check_form(vals, 1, 1)
    "*** YOUR CODE HERE ***"
    return vals.first


def do_let_form(vals, env):
    """Evaluate a let form with parameters VALS in environment ENV."""
    check_form(vals, 2)
    bindings = vals[0]
    exprs = vals.second
    if not scheme_listp(bindings):
        raise SchemeError("bad bindings list in let form")

    # Add a frame containing bindings
    names, values = nil, nil
    "*** YOUR CODE HERE ***"
    # Per make_call_frame(), need to make a list of names and a list of values
    for pair in bindings:
        check_form(pair, 2, 2)
        if not scheme_symbolp(pair.first): 
            raise SchemeError("{0} is not a valid argument name".format(str(pair.first)))
        names  = Pair( pair[0], names)
        values = Pair( scheme_eval(pair[1], env), values)
    check_formals(names) # per STk, repeats in let is an error
    new_env = env.make_call_frame(names, values)

    # Evaluate all but the last expression after bindings, and return the last
    # NB the below logic is identical to do_begin_form(); not sure why not using it?  
    last = len(exprs)-1
    for i in range(0, last):
        scheme_eval(exprs[i], new_env) # evaluate in this new (local) environment
    return exprs[last], new_env


#########################
# Logical Special Forms #
#########################

def do_if_form(vals, env):
    """Evaluate if form with parameters VALS in environment ENV."""
    check_form(vals, 2, 3)
    "*** YOUR CODE HERE ***"
    predicate = scheme_eval(vals[0], env)
    if scheme_true(predicate): 
        return vals[1]
    return vals[2] if len(vals) == 3 else okay

def do_and_form(vals, env):
    """Evaluate short-circuited and with parameters VALS in environment ENV."""
    "*** YOUR CODE HERE ***"
    if vals == nil:
        return True
    for i, v in enumerate(vals):
        if i < len(vals) - 1: 
            result = scheme_eval(v, env)
            if scheme_false(result): 
            	return False
        else: # last element
            return v # return last sub-expression regardless of True or False  


def quote(value):
    """Return a Scheme expression quoting the Scheme VALUE.

    >>> s = quote('hello')
    >>> print(s)
    (quote hello)
    >>> scheme_eval(s, Frame(None))  # "hello" is undefined in this frame.
    'hello'
    """
    return Pair("quote", Pair(value, nil))

def do_or_form(vals, env):
    """Evaluate short-circuited or with parameters VALS in environment ENV."""
    "*** YOUR CODE HERE ***"
    if vals == nil: 
    	return False
    for i, v in enumerate(vals):
        if i < len(vals) - 1:
            result = scheme_eval(v, env)
            if scheme_true(result): 
            	return quote(result)
        else: 
            return v

def do_cond_form(vals, env):
    """Evaluate cond form with parameters VALS in environment ENV."""
    num_clauses = len(vals)
    for i, clause in enumerate(vals):
        check_form(clause, 1)
        if clause.first == "else":
            if i < num_clauses-1:
                raise SchemeError("else must be last")
            test = True
            if clause.second is nil:
                raise SchemeError("badly formed else clause")
        else:
            test = scheme_eval(clause.first, env)
        
        if scheme_true(test):
            "*** YOUR CODE HERE ***"
            if clause.second == nil: # body of cond case is empty
                return quote(test)
            else:
                return do_begin_form(clause.second, env)
    return okay


def do_begin_form(vals, env):
    """Evaluate begin form with parameters VALS in environment ENV."""
    check_form(vals, 1)
    "*** YOUR CODE HERE ***"
    N = len(vals)
    for i, v in enumerate(vals):
        if i ==  N - 1:
            return v # return the last v, not scheme_eval(v)
        scheme_eval(v, env)


LOGIC_FORMS = {
        "and": do_and_form,
        "or": do_or_form,
        "if": do_if_form,
        "cond": do_cond_form,
        "begin": do_begin_form,
        }

# Utility methods for checking the structure of Scheme programs

def check_form(expr, min, max = None):
    """Check EXPR (default SELF.expr) is a proper list whose length is
    at least MIN and no more than MAX (default: no maximum). Raises
    a SchemeError if this is not the case."""
    if not scheme_listp(expr):
        raise SchemeError("badly formed expression: " + str(expr))
    length = len(expr)
    if length < min:
        raise SchemeError("too few operands in form")
    elif max is not None and length > max:
        raise SchemeError("too many operands in form")

def check_formals(formals):
    """Check that FORMALS is a valid parameter list, a Scheme list of symbols
    in which each symbol is distinct. Raise a SchemeError if the list of formals
    is not a well-formed list of symbols or if any symbol is repeated.

    >>> check_formals(read_line("(a b c)"))
    """
    "*** YOUR CODE HERE ***"
    if not scheme_listp(formals):
        raise SchemeError("formals is a not a well-formed list:{0}".format(str(formals)))

    uniq_symbols = {}     
    for sym in formals: 
        if not scheme_symbolp(sym):
            raise SchemeError( str(sym) + " is not a valid symbol")
        if sym in uniq_symbols:            
            raise SchemeError( str(sym) + " appears more than once")
        uniq_symbols[sym] = 0 # saving sym as dict keys achieves O(1) in search


##################
# Tail Recursion #
##################

def scheme_optimized_eval(expr, env):
    """Evaluate Scheme expression EXPR in environment ENV."""
    while True:
        if expr is None:
            raise SchemeError("Cannot evaluate an undefined expression.")

        # Evaluate Atoms
        if scheme_symbolp(expr):
            return env.lookup(expr)
        elif scheme_atomp(expr) or scheme_stringp(expr) or expr is okay:
            return expr

        # All non-atomic expressions are lists.
        if not scheme_listp(expr):
            raise SchemeError("malformed list: {0}".format(str(expr)))
        first, rest = expr.first, expr.second

        # Evaluate Combinations
        if (scheme_symbolp(first) # first might be unhashable
            and first in LOGIC_FORMS):
            "*** YOUR CODE HERE ***"
            expr = LOGIC_FORMS[first](rest, env)
        elif first == "lambda":
            return do_lambda_form(rest, env)
        elif first == "mu":
            return do_mu_form(rest)
        elif first == "define":
            return do_define_form(rest, env)
        elif first == "quote":
            return do_quote_form(rest)
        elif first == "let":
            "*** YOUR CODE HERE ***"
            expr, env = do_let_form(rest, env)
        else:
            "*** YOUR CODE HERE ***"
            procedure = scheme_eval(first, env)
            args = rest.map(lambda operand: scheme_eval(operand, env))

            # Goal is to replace expr and env with different expressions and environments in the user-define procedure
            # expr and env are identical to scheme_apply(), but don't evaludate. Instead, pass them on iteratively
            if isinstance(procedure, PrimitiveProcedure):
                return apply_primitive(procedure, args, env)
            elif isinstance(procedure, LambdaProcedure):
                env  = procedure.env.make_call_frame(procedure.formals, args)
            elif isinstance(procedure, MuProcedure):
                env  = env.make_call_frame(procedure.formals, args) # don't create a new frane
            else:
                raise SchemeError("Failed to evaludate %s" %(str(expr)) )
            
            expr = procedure.body


################################################################
# Uncomment the following line to apply tail call optimization #
################################################################
# scheme_eval = scheme_optimized_eval


################
# Input/Output #
################

def read_eval_print_loop(next_line, env, quiet=False, startup=False,
                         interactive=False, load_files=()):
    """Read and evaluate input until an end of file or keyboard interrupt."""
    if startup:
        for filename in load_files:
            scheme_load(filename, True, env)
    while True:
        try:
            src = next_line()
            while src.more_on_line:
                expression = scheme_read(src)
                result = scheme_eval(expression, env)
                if not quiet and result is not None:
                    print(result)
        except (SchemeError, SyntaxError, ValueError, RuntimeError) as err:
            if (isinstance(err, RuntimeError) and
                'maximum recursion depth exceeded' not in err.args[0]):
                raise
            print("Error:", err)
        except KeyboardInterrupt:  # <Control>-C
            if not startup:
                raise
            print("\nKeyboardInterrupt")
            if not interactive:
                return
        except EOFError:  # <Control>-D, etc.
            return


def scheme_load(*args):
    """Load a Scheme source file. ARGS should be of the form (SYM, ENV) or (SYM,
    QUIET, ENV). The file named SYM is loaded in environment ENV, with verbosity
    determined by QUIET (default true)."""
    if not (2 <= len(args) <= 3):
        vals = args[:-1]
        raise SchemeError("wrong number of arguments to load: {0}".format(vals))
    sym = args[0]
    quiet = args[1] if len(args) > 2 else True
    env = args[-1]
    if (scheme_stringp(sym)):
        sym = eval(sym)
    check_type(sym, scheme_symbolp, 0, "load")
    with scheme_open(sym) as infile:
        lines = infile.readlines()
    args = (lines, None) if quiet else (lines,)
    def next_line():
        return buffer_lines(*args)
    read_eval_print_loop(next_line, env.global_frame(), quiet=quiet)
    return okay

def scheme_open(filename):
    """If either FILENAME or FILENAME.scm is the name of a valid file,
    return a Python file opened to it. Otherwise, raise an error."""
    try:
        return open(filename)
    except IOError as exc:
        if filename.endswith('.scm'):
            raise SchemeError(str(exc))
    try:
        return open(filename + '.scm')
    except IOError as exc:
        raise SchemeError(str(exc))

def create_global_frame():
    """Initialize and return a single-frame environment with built-in names."""
    env = Frame(None)
    env.define("eval", PrimitiveProcedure(scheme_eval, True))
    env.define("apply", PrimitiveProcedure(scheme_apply, True))
    env.define("load", PrimitiveProcedure(scheme_load, True))
    add_primitives(env)
    return env

@main
def run(*argv):
    next_line = buffer_input
    interactive = True
    load_files = ()
    if argv:
        try:
            filename = argv[0]
            if filename == '-load':
                load_files = argv[1:]
            else:
                input_file = open(argv[0])
                lines = input_file.readlines()
                def next_line():
                    return buffer_lines(lines)
                interactive = False
        except IOError as err:
            print(err)
            sys.exit(1)
    read_eval_print_loop(next_line, create_global_frame(), startup=True,
                         interactive=interactive, load_files=load_files)
    tscheme_exitonclick()
