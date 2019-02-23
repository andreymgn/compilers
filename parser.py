from syntaxTree import SyntaxTree

LPAREN = '('
RPAREN = ')'
STAR = '*'
PIPE = '|'
CONCAT = 'CONCAT'

def infixToPostfix(tokens: list) -> list:
    tokens.append(RPAREN)
    stack = []
    stack.append(LPAREN)
    result = []
    for t in tokens:
        if t == PIPE or t == CONCAT:
            if stack[-1] == LPAREN:
                stack.append(t)
            else:
                v = stack.pop()
                while v == PIPE or v == STAR or v == CONCAT:
                    result.append(v)
                    v = stack.pop()
                stack.append(v)
                stack.append(t)
        elif t == STAR:
            result.append(t)
        elif t == LPAREN:
            stack.append(t)
        elif t == RPAREN:
            v = stack.pop()
            while v != LPAREN:
                result.append(v)
                v = stack.pop()
        else:
            result.append(t)
    
    return result

def tokenize(s: str) -> list:
    result = []
    addConcat = False
    for ch in s:
        if ch == RPAREN or ch == STAR:
            addConcat = True
        elif ch == LPAREN or ch == PIPE:
            addConcat = False
        elif addConcat:
            result.append(CONCAT)
        result.append(ch)

    return result

def syntaxTreeFromRPN(tokens: list) -> (SyntaxTree, dict):
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
