from sly import Lexer
from sly import Parser
import math

class CalcLexer(Lexer):
    
    #error handling
    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1
    # Set of token names.   This is always required
    #add LPAREN and RPAREN in the future
    tokens = { SHOWLN, QUOTE, COUNT, TYPE, INSTANCE, MIEQ, TIEQ, DIEQ, ROUNDUP, ROUNDDOWN, PLEQ, FIND, ASK, FLOAT, NAME, IF, ELF, ELSE, FUN, CLASS, TRUE, FALSE, WHILE, SHOW, FOR, TO, NUMBER, PLUS, MINUS, TIMES,
               DIVIDE, MOD, EQ, ASSIGN, LE, LT, GE, GT, NE, OR, AND, ARROW, NAME, STRING, THEN }

    # String containing ignored characters between tokens
    ignore = ' \t'
    ignore_comment = r'\@.*'


    literals = {'(', ')', ',', ';', '{', '}', ':', '[', ']', '^'}

    # Regular expression rules for tokens
    SHOWLN = r'showln'
    COUNT = r'count'
    TYPE = r'type'
    ROUNDUP = r'roundUp'
    ROUNDDOWN = r'roundDown'
    FIND = r'.find'
    ASK = r'ask' #input
    IF = r'if'
    ELF = r'elf'
    ELSE = r'else'
    FUN = r'fun'
    WHILE = r'while'
    SHOW = r'show' #print
    FOR = r'for'
    TO = r'to'
    CLASS = r'class'
    ARROW = r'->'
    THEN = r'then'
    TRUE = r'true'
    FALSE = r'false'
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    STRING = r'\'.*?\''
    
    PLEQ = r'\+='
    MIEQ = r'-='
    TIEQ = r'\*='
    DIEQ = r'/='
    QUOTE = r'\"'
    

    
    
    FLOAT = r'[+-]?[0-9]+\.[0-9]+'
    NUMBER  = r'\d+'
    
    PLUS    = r'\+'
    MINUS   = r'-'
    TIMES   = r'\*'
    DIVIDE  = r'/'
    MOD = r'%'

    EQ = r'==' 
    ASSIGN  = r'='
    #LPAREN  = r'\('
    #RPAREN  = r'\)'

    
    INSTANCE = r'inst'
    LE = r'<='
    LT = r'<'
    GE = r'>='
    GT = r'>'
    NE = r'!='
    ID['and'] = AND
    ID['or'] = OR

   

    @_(r'[+-]?[0-9]+\.[0-9]+')
    def FLOAT(self, t):
        t.value = float(t.value)   # Convert to a numeric value
        return t
    
    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)   # Convert to a numeric value
        return t

    

    @_(r'@.*')
    def COMMENT(self, t):
        pass

    



class CalcParser(Parser):
    
    #condition if if (condition), while (condition), etc.
    #expression is y = 3, or something with assigning 
    #statement = 2 + 3 or something that has motion and isnt assigning or checking
    
    tokens = CalcLexer.tokens

    precedence = (
          ('nonassoc', LT, GT, GE, LE, NE),  # Nonassociative operators
          ('left', PLUS, MINUS),
          ('left', TIMES, DIVIDE, MOD),
          ('right', UMINUS),            # Unary minus operator
    )

    def __init__(self):
        self.names = { }


    @_('')
    def statement(self, p):
        pass

    @_('QUOTE STRING QUOTE')
    def statement(self, p):
        pass


    @_('TYPE "(" expr ")" ')
    def expr(self, p):
        return type(p.expr)
    
    @_('FLOAT')
    def expr(self, p):
        return p.FLOAT

    
    @_('NUMBER')
    def expr(self, p):
        return p.NUMBER

    @_('STRING')
    def expr(self, p):
        return p.STRING[1:-1]

    @_('COUNT "(" expr ")" ')
    def expr(self, p):
        return len(p.expr)

    
    @_('TRUE')
    def expr(self, p):
        return True

    @_('FALSE')
    def expr(self, p):
        return False

    @_('TRUE')
    def condition(self, p):
        return True

    @_('FALSE')
    def condition(self, p):
        return False
    
    
    @_('expr EQ expr')
    def condition(self, p):
        return (p.expr0 == p.expr1)

    @_('expr EQ expr')
    def expr(self, p):
        return (p.expr0 == p.expr1)


    @_('IF "(" condition ")" "{" statement "}" ELSE "{" statement "}"')
    def statement(self, p):
        return ('if_stmt', p.condition, ('branch', p.statement0, p.statement1))

    @_('IF "(" condition ")" "{" statement "}" ')
    def statement(self, p):
        return ('if_stmt', p.condition, ('branch', p.statement))
    
    @_('WHILE "(" condition ")" "{" statement "}" ')
    def condition(self, p):
        pass 

    @_('ROUNDUP "(" expr ")" ')
    def expr(self, p):
        return math.ceil(p.expr)

    @_('ROUNDDOWN "(" expr ")" ')
    def expr(self, p):
        return math.floor(p.expr)

    @_('expr')
    def statement(self, p):
        print(p.expr)

    @_('NAME PLEQ expr')
    def expr(self, p):
        self.names[p.NAME] = self.names[p.NAME] + p.expr

    @_('NAME MIEQ expr')
    def expr(self, p):
        self.names[p.NAME] = self.names[p.NAME] - p.expr

    @_('NAME TIEQ expr')
    def expr(self, p):
        self.names[p.NAME] = self.names[p.NAME] * p.expr

    @_('NAME DIEQ expr')
    def expr(self, p):
        self.names[p.NAME] = self.names[p.NAME] / p.expr

    @_('NAME ASSIGN expr')
    def statement(self, p):
        self.names[p.NAME] = p.expr
        
        
    @_('expr PLUS expr')
    def expr(self, p):
        return p.expr0 + p.expr1

    @_('expr MINUS expr')
    def expr(self, p):
        return p.expr0 - p.expr1

    @_('expr TIMES expr')
    def expr(self, p):
        return p.expr0 * p.expr1

    @_('expr DIVIDE expr')
    def expr(self, p):
        return math.floor(p.expr0 / p.expr1)

    @_('expr MOD expr')
    def expr(self, p):
        return p.expr0 % p.expr1

    
    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return -p.expr

    @_('"(" expr ")"')
    def expr(self, p):
        return p.expr

    @_('FUN NAME "(" ")" "{" statement "}"')
    def statement(self, p):
        return ('fun_def', p.NAME, p.statement)

    @_('ASK')
    def expr(self, p):
        return input()

    @_('ASK')
    def statement(self, p):
        return input()

    @_('expr LT expr')
    def expr(self, p):
        return p.expr0 < p.expr1

    @_('expr GT expr')
    def expr(self, p):
        return p.expr0 > p.expr1

    @_('expr LE expr')
    def expr(self, p):
        return p.expr0 <= p.expr1

    @_('expr NE expr')
    def expr(self, p):
        return p.expr0 != p.expr1

    @_('expr GE expr')
    def expr(self, p):
        return p.expr0 >= p.expr1

    @_('expr OR expr')
    def expr(self, p):
        return p.expr0 or p.expr1

    @_('expr AND expr')
    def expr(self, p):
        return p.expr0 and p.expr1
    

    @_('expr LT expr')
    def condition(self, p):
        return p.expr0 < p.expr1

    @_('expr GT expr')
    def condition(self, p):
        return p.expr0 > p.expr1

    @_('expr LE expr')
    def condition(self, p):
        return p.expr0 <= p.expr1

    @_('expr NE expr')
    def condition(self, p):
        return p.expr0 != p.expr1

    @_('expr GE expr')
    def condition(self, p):
        return p.expr0 >= p.expr1

    @_('expr OR expr')
    def condition(self, p):
        return p.expr0 or p.expr1

    @_('expr AND expr')
    def condition(self, p):
        return p.expr0 and p.expr1

    @_('expr "[" expr ":" expr "]"')
    def statement(self, p):
        o = ''
        one = p.expr1
        two = p.expr2
        n = p.expr0  
        for i in range(one, two):
            o += n[i]
        print(o)    

    @_('CLASS NAME ":" statement')
    def statement(self, p):
        return p.NAME

    
    @_('SHOW "(" STRING ")" ')
    def statement(self, p):
        print(p.STRING[1:-1])

    @_('SHOW "(" NAME ")" ')
    def statement(self, p):
        try:
            print( self.names[p.NAME] )
            return
        except LookupError:
            print("Undefined name '%s'" % p.NAME)
            return 0

    @_('SHOWLN "(" STRING ")" ')
    def expr(self, p):
        return p.STRING[1:-1] + '\n'

    

    @_('SHOWLN "(" NAME ")" ')
    def expr(self, p):
        try:
            print( "{} \n".format(self.names[p.NAME]) )
            return
        except LookupError:
            print("Undefined name '%s'" % p.NAME)
            return 0

    @_('SHOWLN "(" statement ")" ')
    def expr(self, p):
        return "{} \n".format(p.statement)

    @_('expr FIND "(" expr ")" ')
    def statement(self, p):
        o = p.expr0[1:-1].find(p.expr1[1:-1])
        print(o)

    @_('SHOW "(" statement ")" ')
    def statement(self, p):
        print(p.statement)


    @_('expr "[" expr "]" ')
    def statement(self, p):
        o = p.expr0
        print(o[p.expr1])
        return o

    @_('expr "^" expr')
    def expr(self, p):
        o = p.expr0 ** p.expr1
        return o

    @_('NAME')
    def expr(self, p):
        try:
            return self.names[p.NAME]
        except LookupError:
            print("Undefined name '%s'" % p.NAME)
            return 0

       

if __name__ == '__main__':
    lexer = CalcLexer()
    parser = CalcParser()
    while True:
        try:
            text = input('>>> ')
        except EOFError:
            break
        if text:
            parser.parse(lexer.tokenize(text))
