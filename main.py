from g3 import Parser

s = ''
with open('programs/success.txt') as f:
    s = f.read()
print(s)
p = Parser(s)

print(p.run())
