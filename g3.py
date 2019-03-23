class ParserException(Exception):
    pass

class Parser:
    def __init__(self, s):
        self.input = s.strip()
        self.col = 1
        self.row = 1
        self.i = 0

    def next_char(self, i):
        ws = set([' ', '\n'])
        while True:
            if i >= len(self.input):
                return len(self.input)
            if self.input[i] == ' ':
                self.col += 1
            elif self.input[i] == '\n':
                self.col = 1
                self.row +=1
            else:
                self.col += 1
                return i
            i += 1

    def accept(self, symbol):
        oldCol = self.col
        oldRow = self.row
        i = self.i
        for ch in symbol:
            i = self.next_char(i)
            if i >= len(self.input):
                return False
            if ch != self.input[i]:
                self.col = oldCol
                self.row = oldRow
                return False
            i += 1
        self.i = i
        return True

    def mul_op(self):
        ops = ['*', '/', '%']
        for op in ops:
            if self.accept(op):
                return True, ('mul_op', op)
        return False, ()

    def add_op(self):
        ops = ['+', '-']
        for op in ops:
            if self.accept(op):
                return True, ('add_op', op)
        return False, ()

    def comparison_op(self):
        ops = ['<', '<=', '==', '!=', '>', '>=']
        for op in ops:
            if self.accept(op):
                return True, ('comparison_op', op)
        return False, ()

    def primary_expr(self):
        if self.accept('123'):
            return True, ('primary_expr', '123')
        if self.accept('abc'):
            return True, ('primary_expr', 'abc')
        if self.accept('('):
            success, val = self.arith_expr()
            if not success:
                raise ParserException('arithmetic expression expected at ({}, {})'.format(self.row, self.col))
            if not self.accept(')'):
                raise ParserException('closing parenthesis expected at ({}, {})'.format(self.row, self.col))
            return True, ('primary_expr', val)
        return False, ()

    def exponent(self):
        success, val1 = self.primary_expr()
        if not success:
            return False, ()
        success, val2 = self.exponent1()
        if not success:
            return False, ()
        return True, ('exponent', val1, val2)

    def exponent1(self):
        if self.accept('^'):
            success, val1 = self.primary_expr()
            if not success:
                raise ParserException('primary expression expected at ({}, {})'.format(self.row, self.col))
            _, val2 = self.exponent1()
            return True, ('exponent1', '^', val1, val2)
        return True, ('exponent1')

    def term(self):
        success, val1 = self.exponent()
        if not success:
            return False, ()
        success, val2 = self.term1()
        if not success:
            return False, ()
        return True, ('term', val1, val2)

    def term1(self):
        success, val1 = self.mul_op()
        if success:
            success, val2 = self.exponent()
            if not success:
                return False, ()
            _, val3 = self.term1()
            return True, ('term1', val1, val2, val3)
        return True, ('term1')

    def arith_expr(self):
        success, val1 = self.term()
        if success:
            success, val2 = self.arith_expr1()
            if not success:
                return False, ()
            return True, ('arith_expr', val1, val2)
        success, val1 = self.add_op()
        if success:
            success, val2 = self.term()
            if not success:
                return False, ()
            success, val3 = self.arith_expr1()
            if not success:
                return False, ()
            return True, ('arith_expr', val1, val2, val3)
        raise ParserException('arithmetic expression expected at ({}, {})'.format(self.row, self.col))

    def arith_expr1(self):
        success, val1 = self.add_op()
        if success:
            success, val2 = self.term()
            if not success:
                return False, ()
            _, val3 = self.arith_expr1()
            return True, ('arith_expr1', val1, val2, val3)
        return True, ('arith_expr1')

    def expr(self):
        success, val1 = self.arith_expr()
        if not success:
            return False, ()
        success, val2 = self.comparison_op()
        if not success:
            raise ParserException('expected comparison operator at ({}, {})'.format(self.row, self.col))
        success, val3 = self.arith_expr()
        if not success:
            return False, ()
        return True, ('expr', val1, val2, val3)

    def program(self):
        success, val = self.unit()
        if not success:
            raise ParserException('program failed at ({}, {})'.format(self.row, self.col))
        return True, ('program', val)

    def unit(self):
        if not self.accept('{'):
            return False, ()
        success, val = self.operator_list()
        if not success:
            return False, ()
        if not self.accept('}'):
            raise ParserException('expected closing curly brace at ({}, {})'.format(self.row, self.col))
        return True, ('unit', val)

    def operator_list(self):
        success, val1 = self.operator()
        if not success:
            return False, ()
        success, val2 = self.operator_tail()
        if not success:
            return False, ()
        return True, ('operator_list', val1, val2)

    def operator_tail(self):
        if self.accept(';'):
            success, val1 = self.operator()
            if not success:
                raise ParserException('expected operator after semicolon at ({}, {})'.format(self.row, self.col))
            _, val2 = self.operator_tail()
            return True, ('operator_tail', val1, val2)
        return True, ('operator_tail')
    
    def operator(self):
        if self.accept('abc') and self.accept('='):
            success, val = self.expr()
            if not success:
                return False, ()
            return True, ('operator', 'abc', val)
        success, val = self.unit()
        if not success:
            return False, ()
        return True, ('operator', 'abc', val)

    def run(self):
        _, val = self.program()
        return self.i == len(self.input), val
