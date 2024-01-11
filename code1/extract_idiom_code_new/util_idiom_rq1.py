import ast,re
def get_node_type(node):
    if isinstance(node,ast.Expr):
        node=node.value
    type_node=str(node.__class__)
    result = re.search('\'ast.(.*)\'', type_node)
    return result.group(1)
def count_key_value(value,dict_objects):
    compa_type = get_node_type(value)
    if compa_type not in dict_objects:
        dict_objects[compa_type] = 1
    else:
        dict_objects[compa_type] += 1
