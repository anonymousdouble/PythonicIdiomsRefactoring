import ast,re
import traceback

code='''
formatted_string = "My name is %s, and I am %d years old." % (name, age)
'''
tree=ast.parse(code)
for node in ast.walk(tree):
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mod):
        if isinstance(node.left, ast.Constant) and isinstance(node.left.value, str):
            if isinstance(node.right, ast.Tuple):
                vars = [ast.unparse(e) for e in node.right.elts]
            else:
                vars = [ast.unparse(node.right)]
            left_string = node.left.value
            # print(">>>>: ",ast.unparse(node))
            # print("vars: ",vars)

            # # formatting_syntax = re.findall(r'%[0-9]*(\.[0-9]+)?[a-zA-Z]', input_string)
            # "[0-9]*\.?[0-9]*[diouxXeEfFgGcrs%]"
            matches = re.findall(r'%[0-9]*\.?[0-9]*[diouxXeEfFgGcrs%]', left_string)
            # print("matches: ", matches)
            if len(vars) != len(matches):
                break
            # print("len: ", len(vars),len(matches))
            for ind_match, old_str in enumerate(matches):
                left_string = left_string.replace(old_str, '{' + vars[ind_match] + '}')
            # new_string='f'+"'"+left_string+"'"
            try:
                new_string = 'f"' + left_string + '"'
                fstring_node=ast.JoinedStr()

            except:
                traceback.print_exc()