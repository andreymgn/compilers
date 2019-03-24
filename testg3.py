import unittest

from g3 import Parser, ParserException

class TestG3(unittest.TestCase):
    def testSuccess(self):
        testCase = 'programs/success.txt'
        s = ''
        with open(testCase) as f:
            s = f.read()
        p = Parser(s)
        p.run()

    def testFail(self):
        prefix = 'programs/fail_'
        ext = '.txt'
        testCases = ['missing_close_bracket',
                     'missing_open_bracket',
                     'missing_close_parenthesis',
                     'missing_open_parenthesis',
                     'missing_semi',
                     'no_arith_expr',
                     'no_condition']
        testCases = [prefix + test + ext for test in testCases]

        for test in testCases:
            s = ''
            with open(test) as f:
                s = f.read()
            p = Parser(s)
            self.assertRaises(ParserException, p.run)
