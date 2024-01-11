Keywords=["False",      "await",      "else",       "import",     "pass",
"None",       "break",      "except",     "in",         "raise",
"True",       "class",      "finally",    "is",         "return",
"and",        "continue",   "for",        "lambda",     "try",
"as",         "def",        "from",       "nonlocal",   "while",
"assert",     "del",       "global",     "not",        "with",
"async",      "elif",       "if",         "or",         "yield"]
Operators=["+",       "-",       "*",       "**",      "/",       "//",      "%",     "@",
"<<",      ">>",      "&",       "|",       "^",       "~",       ":=",
"<",       ">",       "<=",      ">=",      "==",      "!="]
Delimiters=["(",       ")",       "[",       "]",       "{",       "}",
",",       ":",       ".",       ";",       "@",       "=",       "->",
"+=",      "-=",      "*=",      "/=",      "//=",     "%=",     "@=",
"&=",      "|=",      "^=",      ">>=",     "<<=v",     "**="]
Primitive_types=['int','float','str','complex']
Sequence_types=['set','frozenset','list', 'tuple', 'range','dict']
Byte_types=['bytes', 'bytearray', 'memoryview']
builtins_types = [
"int", "float", "complex", "bool", "list", "tuple", "range", "str",
    "bytes", "bytearray", "memoryview", "set", "frozenset",
    "dict", "dict_keys", "dict_values", "dict_items", "None",
    "type","method"
]

import ast
from tokenize import tokenize, untokenize, NUMBER, STRING, NAME, OP
from io import BytesIO
def get_features_chain_compare(node_list=None):

    # node_list=[ast.parse(content)]
    dict_feature = {'num_Eq': 0,'num_NotEq': 0,'num_Lt': 0,'num_LtE': 0,'num_Gt': 0,'num_GtE': 0,
             'num_Is': 0, 'num_IsNot': 0,'num_In': 0,'num_NotIn': 0,
             'num_cmpop': 0}
    for ast_node in node_list:

        for node in ast.walk(ast_node):

            if isinstance(node, (ast.Eq)):
                dict_feature["num_Eq"] += 1
            elif isinstance(node, (ast.NotEq)):
                dict_feature["num_NotEq"] += 1
            elif isinstance(node, (ast.Lt)):
                dict_feature["num_Lt"] += 1
            elif isinstance(node, (ast.LtE)):
                dict_feature["num_LtE"] += 1
            elif isinstance(node, (ast.Gt)):
                dict_feature["num_Gt"] += 1
            elif isinstance(node, (ast.GtE)):
                dict_feature["num_GtE"] += 1
            elif isinstance(node, (ast.Is)):
                dict_feature["num_Is"] += 1
            elif isinstance(node, (ast.IsNot)):
                dict_feature["num_IsNot"] += 1
            elif isinstance(node, (ast.In)):
                dict_feature["num_In"] += 1
            elif isinstance(node, (ast.NotIn)):
                dict_feature["num_NotIn"] += 1
            if isinstance(node, (ast.Compare)):
                dict_feature["num_cmpop"] += 1


    return dict_feature
def get_features_list_comprehension(node_list=None):
    content='''
self.c().d()
class A:
 pass
def f(a):
    c=1
a[1];b[1]
a[1:2][2]
c(*a,**args)
self.a.b
{1:2}
{1,2}

timed_out = []
for seq_num in self.frag_map:
    if t_now - self.frag_map[seq_num]['t_last'] > self.timeout:
        timed_out.append(seq_num)

'''
    # node_list=[ast.parse(content)]
    dict_feature = {"num_loop": 0, "num_if": 0, "num_if_else": 0}
    num_call_with_name=0
    for ast_node in node_list:

        for node in ast.walk(ast_node):

            if isinstance(node, (ast.For,ast.While)):
                dict_feature["num_loop"] += 1
            elif isinstance(node, ast.If):
                if node.orelse:
                    dict_feature["num_if_else"] += 1
                else:
                    dict_feature["num_if"] += 1

    return dict_feature
def get_features(node_list=None):
    content='''
self.c().d()
class A:
 pass
def f(a):
    c=1
a[1];b[1]
a[1:2][2]
c(*a,**args)
self.a.b
{1:2}
{1,2}

timed_out = []
for seq_num in self.frag_map:
    if t_now - self.frag_map[seq_num]['t_last'] > self.timeout:
        timed_out.append(seq_num)

'''
    # node_list=[ast.parse(content)]
    dict_feature = {"num_loop": 0, "num_if": 0, "num_if_else": 0,
                    "num_func_call": 0, "num_param": 0,
                    "num_var": 0, "num_List": 0, "num_Dict": 0, "num_Set": 0, "num_Tuple": 0, "num_Subscript": 0,
                    "num_Slice": 0, "num_Attr": 0,"num_constant": 0,
                    "num_line": 0, "num_Keywords": 0,  "num_Operators": 0, "num_Delimiters": 0}
    num_call_with_name=0
    for ast_node in node_list:
        code_content=ast.unparse(ast_node)
        g = tokenize(BytesIO(code_content.encode('utf-8')).readline)
        for toknum, tokval, _, _, _ in g:
            if tokval in Keywords:
                dict_feature["num_Keywords"] += 1
            elif tokval in Operators:
                dict_feature["num_Operators"] += 1
            elif tokval in Delimiters:
                dict_feature["num_Delimiters"] += 1
        for node in ast.walk(ast_node):
            if isinstance(node,ast.stmt):
                dict_feature["num_line"] += 1
            if isinstance(node, (ast.For,ast.While)):
                dict_feature["num_loop"] += 1
            elif isinstance(node, ast.If):
                if node.orelse:
                    dict_feature["num_if_else"] += 1
                else:
                    dict_feature["num_if"] += 1
            elif isinstance(node, ast.Name):
                dict_feature["num_var"] += 1
                # print("var: ",ast.unparse(node))
            elif isinstance(node, ast.Call):
                call_name_flag=0
                if isinstance(node.func,ast.Name):
                    num_call_with_name += 1
                if isinstance(node.func, ast.Attribute):
                    call_name = node.func.attr
                    if call_name=="append":
                        call_name_flag=1

                    # print("call: ", ast.unparse(node))
                dict_feature["num_func_call"] += 1 if not call_name_flag else 0
                if hasattr(node,"args"):
                    dict_feature["num_param"] += len(node.args)
                if hasattr(node, "keywords"):
                    dict_feature["num_param"] += len(node.keywords)
            elif isinstance(node,ast.Constant):
                dict_feature["num_constant"] += 1
            elif isinstance(node, ast.List):
                dict_feature["num_List"] +=1
            elif isinstance(node, ast.Dict):
                dict_feature["num_Dict"] +=1
            elif isinstance(node, ast.Set):
                dict_feature["num_Set"] +=1
            elif isinstance(node, ast.Tuple):
                dict_feature["num_Tuple"] +=1
            elif isinstance(node, ast.Subscript):
                dict_feature["num_Subscript"] +=1
            elif isinstance(node, ast.Slice):
                dict_feature["num_Slice"] +=1
            elif isinstance(node, ast.Attribute):
                dict_feature["num_Attr"] +=1

    if  dict_feature["num_line"]==0:
        dict_feature["num_line"]=1
    dict_feature["num_var"]-=num_call_with_name
    # print(dict_feature,num_call_with_name)
    return dict_feature
if __name__ == '__main__':
    get_features()