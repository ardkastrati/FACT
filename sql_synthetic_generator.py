from re import S
from synthetic.generate import Generator
from synthetic.compound import Add, Sub, Mult, Pow
from synthetic.number import Const, NConst, Var
from synthetic.trigonometric import Sin, Cos
from synthetic.prime import Prime
from synthetic.modulo import Modulo
from synthetic.periodic import Periodic
from synthetic.finite import Finite


exp = 500000
trigo = 500000
modulo = 500000


def generate_synthetic():
    ### POLYNOMIALS
    terminals = [Var(), Const()]
    non_terminals = [Add(), Sub(), Mult(), NConst(positive=True), Pow()]
    Add.terminals = terminals
    Add.non_terminals = non_terminals
    Sub.terminals = terminals
    Sub.non_terminals = non_terminals
    Mult.terminals = terminals
    Mult.non_terminals = non_terminals
    Pow.terminals_base = terminals
    Pow.non_terminals_base = non_terminals
    Pow.terminals_exponent = [Const()]
    Pow.non_terminals_exponent = [NConst(positive=True)]


    group = 10000000

    poly = 500000
    length = 0
    size = 20
    current = 0
    for i in range(1,poly + 1):
        if current > size:
            size *= 2
            length += 1
            current = 0
        current += 1
        
        invalid = True
        poly = None
        values = None

        while invalid:
            g = Generator(length=length)
            poly = g.generate(terminals=terminals, non_terminals=non_terminals)
            values = []
            for j in range(500):
                next = poly.evaluate(j)
                if abs(next) > 999999999999999:
                    break
                values.append(next)
            if len(values) == 500:
                invalid = False
        
        entry = (
        -i, 
        "S PO G " + str(i), 
        str(values)[1:-1], 
        "Polynomial of length " + str(poly.get_length()) + " and node length " + str(length + 1), 
        """ terminals = [Var(), Const()]
            non_terminals = [Add(), Sub(), Mult(), NConst(positive=True), Pow()]
            Add.terminals = terminals
            Add.non_terminals = non_terminals
            Sub.terminals = terminals
            Sub.non_terminals = non_terminals
            Mult.terminals = terminals
            Mult.non_terminals = non_terminals
            Pow.terminals_base = terminals
            Pow.non_terminals_base = non_terminals
            Pow.terminals_exponent = [Const()]
            Pow.non_terminals_exponent = [NConst(positive=True)]""",
        "",
        "",
        poly.to_string(),
        "",
        "",
        "",
        poly.to_string(),
        "",
        "synthetic,polynomial",
        0,
        0,
        "Ard Kastrati",
        "")

        yield entry
    for i in range(1000):
        yield "END"


def generate_synthetic_trigonometric():
    #### TRIGONOMETRIC
    #------- SET CONTEXT-FREE GRAMMAR -------#
    terminals = [Var(), Const()]
    non_terminals = [Add(), Sub(), Mult(), NConst(positive=True), Pow(), Sin(), Cos()]
    Add.terminals = terminals
    Add.non_terminals = non_terminals
    Sub.terminals = terminals
    Sub.non_terminals = non_terminals
    Mult.terminals = terminals
    Mult.non_terminals = non_terminals
    Pow.terminals_base = terminals
    Pow.non_terminals_base = non_terminals
    Pow.terminals_exponent = [Const()]
    Pow.non_terminals_exponent = [NConst(positive=True)]
    Sin.terminals = terminals
    Sin.non_terminals = non_terminals
    Cos.terminals = terminals
    Cos.non_terminals = non_terminals


    group = 10000000

    trigo = 500000
    length = 1
    size = 10
    current = 0
    for i in range(1, trigo + 1):
        if current > size:
            size *= 2
            length += 1
            current = 0
        current += 1
        
        invalid = True
        trigo = None
        values = None

        while invalid:
            g = Generator(length=length)
            trigo = g.generate(terminals=terminals, non_terminals=non_terminals)
            values = []
            if trigo.to_string().find("math") != -1:
                for j in range(500):
                    next = trigo.evaluate(j)
                    if abs(next) > 999999999999999:
                        break
                    values.append(next)
            if len(values) == 500:
                invalid = False
        
        entry = (
        - group - i, 
        "S TR B " + str(i), 
        str(values)[1:-1], 
        "Trigonometric of length " + str(trigo.get_length()) + " and node length " + str(length + 1), 
        """ terminals = [Var(), Const()]
            non_terminals = [Add(), Sub(), Mult(), NConst(positive=True), Pow(), Sin(), Cos()]
            Add.terminals = terminals
            Add.non_terminals = non_terminals
            Sub.terminals = terminals
            Sub.non_terminals = non_terminals
            Mult.terminals = terminals
            Mult.non_terminals = non_terminals
            Pow.terminals_base = terminals
            Pow.non_terminals_base = non_terminals
            Pow.terminals_exponent = [Const()]
            Pow.non_terminals_exponent = [NConst(positive=True)]
            Sin.terminals = terminals
            Sin.non_terminals = non_terminals
            Cos.terminals = terminals
            Cos.non_terminals = non_terminals""",
        "",
        "",
        trigo.to_string(),
        "",
        "",
        "",
        trigo.to_string(),
        "",
        "synthetic,trigonometric",
        0,
        0,
        "Ard Kastrati",
        "")

        yield entry
    for i in range(1000):
        yield "END"


def thread_evaluate(exp, j, answer):
    s = exp.evaluate(j)
    #print(s)
    answer[0] = s
    #print(answer[0])

def generate_synthetic_exponential(counter, length):
    #### Exponential
    #------- SET CONTEXT-FREE GRAMMAR -------#
    terminals = [Var(), Const()]
    non_terminals = [Add(), Sub(), Mult(), NConst(positive=True), Pow()]
    Add.terminals = terminals
    Add.non_terminals = non_terminals
    Sub.terminals = terminals
    Sub.non_terminals = non_terminals
    Mult.terminals = terminals
    Mult.non_terminals = non_terminals
    Pow.terminals_base = terminals
    Pow.non_terminals_base = non_terminals
    Pow.terminals_exponent = terminals
    Pow.non_terminals_exponent = non_terminals

    group = 20000000
        
    invalid = True
    exp = None
    values = None

    while invalid:
        g = Generator(length=length)
        exp = g.generate(terminals=terminals, non_terminals=non_terminals)
        #print(exp.to_string())
        values = []
        #print("Trying poly: ", exp.to_string())
        if exp.to_string().find("**(") != -1:
            for j in range(50):
                import multiprocessing
                import time
                manager = multiprocessing.Manager()
                answer = manager.dict()
                    
                p = multiprocessing.Process(target=thread_evaluate, args=(exp, j, answer))
                p.start()
                p.join(1)
                if p.is_alive():
                    print("running... let's kill it...")
                    p.kill()
                    break
                else:
                    #print(answer.values())
                    next = answer[0]
                    #print(next)
                    if not isinstance(next, int) or abs(next) > 999999999999999:
                        break
                    values.append(next)
        if len(values) > 10:
            invalid = False
        
    entry = (
    - group - counter, 
    "S EX G " + str(counter), 
    str(values)[1:-1], 
    "Exponential of length " + str(exp.get_length()) + " and node length " + str(length + 1), 
    """ terminals = [Var(), Const()]
        non_terminals = [Add(), Sub(), Mult(), NConst(positive=True), Pow()]
        Add.terminals = terminals
        Add.non_terminals = non_terminals
        Sub.terminals = terminals
        Sub.non_terminals = non_terminals
        Mult.terminals = terminals
        Mult.non_terminals = non_terminals
        Pow.terminals_base = terminals
        Pow.non_terminals_base = non_terminals
        Pow.terminals_exponent = terminals
        Pow.non_terminals_exponent = non_terminals""",
    "",
    "",
    exp.to_string(),
    "",
    "",
    "",
    exp.to_string(),
    "",
    "synthetic,exponential",
    0,
    0,
    "Ard Kastrati",
    "")
    return entry




