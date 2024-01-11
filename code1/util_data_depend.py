import ast
from extract_simp_cmpl_data import ast_util
def is_data_depend(node1,node2):
    node1_str=ast.unparse(node1)
    node2_str=ast.unparse(node2)
    for e in ast.walk(node1):
        if ast.unparse(e)==node2_str:
            return 1
    for e in ast.walk(node2):
        if ast.unparse(e) == node1_str:
            return 1
    return 0
def is_ass_depend(ass_node):
    targets=ass_node.targets
    value=ass_node.value
    for tar in targets:
        if is_data_depend(tar,value):
            return 1
    return 0

def is_const_data(ass_code):
    count_obj = ast_util.get_basic_count(ass_code)
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
