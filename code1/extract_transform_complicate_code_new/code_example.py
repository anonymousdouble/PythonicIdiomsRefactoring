import ast
code='''
a=1
b=2
'''
for e in ast.walk(ast.parse(code)):
    if isinstance(e, ast.stmt):
        for ind,w in enumerate(ast.walk(e)):
            if ind and isinstance(w,ast.stmt):
                break
            print(w)