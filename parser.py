from syntaxTree import SyntaxTree

LPAREN = '('
RPAREN = ')'
STAR = '*'
PIPE = '|'
CONCAT = 'CONCAT'

def getPrecedence(ch: str) -> int:
    precedence = {
        LPAREN: 1,
        PIPE: 2,
        CONCAT: 3,
        STAR: 4
    }
    if ch in precedence:
        return precedence[ch]
    else:
        return 5

def infixToPostfix(tokens: list) -> list:
    tokens.append(RPAREN)
    stack = []
    stack.append(LPAREN)
    result = []
    for t in tokens:
        if t == LPAREN:
            stack.append(t)
        elif t == RPAREN:
            while stack[-1] != LPAREN:
                result.append(stack.pop())
            stack.pop()
        else:
            while len(stack) > 0:
                top = stack[-1]
                topPrecedence = getPrecedence(top)
                currentPrecedence = getPrecedence(t)

                if (topPrecedence < currentPrecedence):
                    break
                result.append(stack.pop())
            stack.append(t)

    while len(stack) > 0:
        result.append(stack.pop())
    
    return result

def tokenize(s: str) -> list:
    result = []
    operators = ['|', '*']
    binOperators = ['|']
    for i, ch in enumerate(s[:-1]):
        nextCh = s[i+1]
        result.append(ch)
        if ch != LPAREN and \
            nextCh != RPAREN and \
            not nextCh in operators and \
            not ch in binOperators:
            result.append(CONCAT)
    result.append(s[-1])

    return result

def syntaxTreeFromRPN(tokens: list) -> (SyntaxTree, dict, set):
    stack = []
    position = 1
    positions = {}
    for t in tokens:
        if t == PIPE:
            right = stack.pop()
            left = stack.pop()
            stack.append(SyntaxTree(
                t,
                0,
                left,
                right,
                left.nullable or right.nullable,
                left.firstpos.union(right.firstpos),
                left.lastpos.union(right.lastpos)
            ))
        elif t == CONCAT:
            right = stack.pop()
            left = stack.pop()
            stack.append(SyntaxTree(
                t,
                0,
                left,
                right,
                left.nullable and right.nullable,
                left.firstpos.union(right.firstpos) if left.nullable else left.firstpos,
                left.lastpos.union(right.lastpos) if right.nullable else right.lastpos
            ))
        elif t == STAR:
            left = stack.pop()
            stack.append(SyntaxTree(
                t,
                0,
                left,
                None,
                True,
                left.firstpos,
                left.lastpos
            ))
        else:
            stack.append(SyntaxTree(
                t,
                position,
                None,
                None,
                False,
                frozenset([position]),
                frozenset([position])
            ))
            positions[position] = t
            position += 1
    return stack.pop(), positions
