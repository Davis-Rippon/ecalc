from . import pager
from .functions import FUNCTIONS_TABLE
from .pager import pager

ALPHABET = "ABCDEFGHIKLMNOPQRSTUVWXYZabcdefghiklmnopqrstuvwxyz"

class Lexer:
    UNIT_PREFIXES = { 
            "G": 10**9,    # giga
            "M": 10**6,    # mega
            "k": 10**3,    # kilo
            "h": 10**2,    # hecto
            "da": 10**1,   # deka

            "": "e0",     # no prefix (base unit)

            "d": 10**-1,   # deci
            "c": 10**-2,   # centi
            "m": 10**-3,   # milli
            "µ": 10**-6,   # micro (unicode mu symbol)
            "u": 10**-6,   # micro (alternative)
            "n": 10**-9,   # nano
    }

    def __init__(self, expr: str):
        self.char_idx = 0
        self.expr_string = expr
        self.tokenised_string = []

    def pfloat(self):
        # number
        output = ""
        ch = self.expr_string[self.char_idx]

        while ch.isdigit() or ch == '.':
            try:
                output += ch
                self.char_idx += 1
                ch = self.expr_string[self.char_idx]

            except IndexError:
                return float(output)

        output = float(output)

        if ch in Lexer.UNIT_PREFIXES:
            self.char_idx += 1
            output *= Lexer.UNIT_PREFIXES[ch]

        while ch == " ":
            self.char_idx += 1
            ch = self.expr_string[self.char_idx]
            if ch in Lexer.UNIT_PREFIXES:
                self.char_idx += 1
                output *= Lexer.UNIT_PREFIXES[ch]

        return output # is it better to return outputs or add them to class' list?

    def pfunc(self):
        output = ""
        ch = self.expr_string[self.char_idx]
        
        while ch in ALPHABET:
            try:
                output += ch
                self.char_idx += 1
                ch = self.expr_string[self.char_idx]

            except IndexError:
                for name, _ in FUNCTIONS_TABLE:
                    if output == name:
                        return name

                out = pager.find(output)
                if out is not None:

                    self.tokenised_string.append('(')
                    self.tokenised_string.append(float(out.real))

                    if out.imag != 0:
                        self.tokenised_string.append('+')
                        self.tokenised_string.append(float(out.imag))
                        self.tokenised_string.append('j')

                    return ')'
                return None

        for name, _ in FUNCTIONS_TABLE:
            if output == name:
                return name

        print(output)
        out = pager.find(output)

        if out is not None:

            self.tokenised_string.append('(')
            self.tokenised_string.append(float(out.real))

            if out.imag != 0:
                self.tokenised_string.append('+')
                self.tokenised_string.append(float(out.imag))
                self.tokenised_string.append('j')

            return ')'

        return None
            


    def parse(self) -> list[str]:

        while True:
            try:
                ch = self.expr_string[self.char_idx]
                out = None
                match ch:
                    case digit if digit.isdigit():
                        out = self.pfloat()

                    case function if function in ALPHABET:
                        out = self.pfunc()

                    case Op if Op in "-+/|*":
                        out = Op
                        self.char_idx += 1


                        # special case where negative means -1*
                        if (Op == '-'):
                            if self.tokenised_string[-1] in "(,-+/|*":
                                # self.tokenised_string.append('(')
                                self.tokenised_string.append(float(-1))
                                # self.tokenised_string.append(')')
                                out = '*'

                    case X if X == 'j':
                        out = X
                        self.char_idx += 1

                    case ',':
                        out = ','
                        self.char_idx +=1 

                    case Bracket if Bracket == '(' or Bracket == ')':
                        out = Bracket
                        self.char_idx += 1

                    case _:
                        self.char_idx += 1
                        continue


                if out is not None: self.tokenised_string.append(out)

            except IndexError:
                return self.tokenised_string

            


def parse_input(expr):
    p = Lexer(expr)
    return p.parse()


