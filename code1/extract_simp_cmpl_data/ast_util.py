import ast,re
Keywords=["False",      "await",      "else",       "import",     "pass",
"None",       "break",      "except",     "in",         "raise",
"True",       "class",      "finally",    "is",         "return",
"and",        "continue",   "for",        "lambda",     "try",
"as",         "def",        "from",       "nonlocal",   "while",
"assert",     "del",       "global",     "not",        "with",
"async",      "elif",       "if",         "or",         "yield"]
class Fun_Analyzer(ast.NodeVisitor):
    def __init__(self,class_name=""):
        self.func_def_list = []
        self.class_name = class_name
    def visit_FunctionDef(self, node):
        self.func_def_list.append([node, self.class_name])
        ast.NodeVisitor.generic_visit(self, node)
    def generic_visit(self, node):
        ast.NodeVisitor.generic_visit(self, node)

    def visit_ClassDef(self, node):

        class_ana=Fun_Analyzer(node.name)
        for stmt in node.body:
            class_ana.visit(stmt)
        self.func_def_list.extend(class_ana.func_def_list)
    def visit_If(self, node: ast.If):
        if ast.unparse(node.test) == "__name__ == '__main__'":
            self.func_def_list.append([node,""])
class Analyzer(ast.NodeVisitor):
    def __init__(self):
        self.func_def_list = []

    def visit_FunctionDef(self,node):
        self.func_def_list.append(node)
    def visit_If(self, node: ast.If):
        if ast.unparse(node.test)=="__name__ == '__main__'":
            self.func_def_list.append(node)
def set_dict_class_code_list(tree,dict_class,class_name,new_code_list):
    me_name = tree.name if hasattr(tree, "name") else "if_main_my"
    me_lineno = tree.lineno
    me_id = "".join([me_name, "$", str(me_lineno)])

    if class_name not in dict_class:
        dict_class[class_name] = dict()
        dict_class[class_name][me_id] = new_code_list
    else:

        dict_class[class_name][me_id] = new_code_list

def get_starred_count(e):
    count=0
    for child in ast.walk(e):
        if isinstance(child, ast.Starred):
            count+=1
    return count
def is_const_data(ass_code):
    count_obj = get_basic_count(ass_code)
    count_const = 0
    for e in ast.walk(ass_code):
        if isinstance(e, ast.Constant):
            count_const += 1
    if count_obj > count_const:
        return 0
        # dict_data_attr["value_constant"].append(0)
    else:
        return 1
        # dict_data_attr["value_constant"].append(1)
def get_node_type(node):
    if isinstance(node,ast.Expr):
        node=node.value
    type_node=str(node.__class__)
    result = re.search('\'ast.(.*)\'', type_node)
    return result.group(1)
def get_basic_type(e,dict_type):


    # print("e dict: ",e.__dict__)
    if isinstance(e, (ast.Tuple,ast.List,ast.Set)):
        # count += len(e.elts)
        for cur in e.elts:
            get_basic_type(cur,dict_type)

    else:
        # print(e.__dict__, " are not been parsed")
        node_type=get_node_type(e)
        if node_type in dict_type:
            dict_type[node_type]+=1
        else:
            dict_type[node_type]= 1

def get_basic_count(e):

    count=0
    # print("e dict: ",e.__dict__)
    if isinstance(e, (ast.Tuple,ast.List,ast.Set)):
        # count += len(e.elts)
        for cur in e.elts:
            count +=get_basic_count(cur)

    else:
        # print(e.__dict__, " are not been parsed")
        count +=1


    return count

def get_depth(e):


    # print("e dict: ",e.__dict__)
    if isinstance(e, (ast.Tuple,ast.List,ast.Set)):
        # count += len(e.elts)
        max_depth=0
        for cur in e.elts:
            max_depth=max(get_basic_count(cur)+1,max_depth)
        return max_depth

    return 1
def get_node_type(node):
    if isinstance(node,ast.Expr):
        node=node.value
    type_node=str(node.__class__)
    result = re.search('\'ast.(.*)\'', type_node)
    return result.group(1)
def get_basic_object(e,var_list=[]):
    if isinstance(e, (ast.Tuple,ast.List,ast.Set)):
        # count += len(e.elts)
        for cur in e.elts:
            get_basic_object(cur,var_list)

    else:
        # print(e.__dict__, " are not been parsed")
        var_list.append(ast.unparse(e))

def get_basic_object_node(e,var_list=[]):
    if isinstance(e, (ast.Tuple,ast.List,ast.Set)):
        # count += len(e.elts)
        for cur in e.elts:
            get_basic_object_node(cur,var_list)

    else:
        # print(e.__dict__, " are not been parsed")
        var_list.append(e)
def extract_ast_block_node(node,node_list):
    for k in node._fields:

        v = getattr(node, k)

        if isinstance(v, list):
            # print("come here", v)
            a=[]
            for e in v:
                a.append(e)
                if isinstance(e, ast.AST):
                    extract_ast_block_node(e, node_list)
            node_list.append(a)
        elif isinstance(v, ast.AST):
            # print("come here", v.__dict__)
            if v._fields:
                extract_ast_block_node(v,node_list)
def find_parent_node(tree,target_node):
    for node in ast.walk(tree):
        for e_child in ast.iter_child_nodes(node):
            if e_child==target_node:
                return node


def extract_ast_cur_layer_node(node,node_list):
    # if node._fields:
    #     node_list.append(list(node._fields))
    for k in node._fields:
        v = getattr(node, k)

        if isinstance(v, list):
            a = []
            for e in v:
                a.append(e)
            node_list.append(a)
            for e in v:
                if e._fields:
                    extract_ast_block_node(e, node_list)
        elif isinstance(v, ast.AST):
            if v._fields:
                extract_ast_block_node(v, node_list)

if __name__ == '__main__':
    code='''
a.b=2
if label_names:
    a=2
    num_tensors_in_label = len(label_names)
else:
    num_tensors_in_label = int(has_labels)
# a=1
# b=c.b+1
a=1
b=2
c,d=1,2
for i in range(2):
    a=1
    if i>1:
        if i>2:
            a=3
        a=2
        break 
if a==2:
    print(1)
print("1")   
def a():
    return 1
for i in range(5):
    a=1
    break
if a:
    print("test")
if __name__ == '__main__':
    a=1
    
'''
    tree = ast.parse(code)
    node_list=[]
    extract_ast_cur_layer_node(tree, node_list)
    for e in node_list:
        print(e)
