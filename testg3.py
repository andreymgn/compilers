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
        testCases = []

        for test in testCases:
            s = ''
            with open(test) as f:
                s = f.read()
            p = Parser(s)
            self.assertRaises(ParserException, p.run)
