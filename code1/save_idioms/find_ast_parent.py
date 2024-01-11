import ast

def find_parent_node(tree,target_node):
    for node in ast.walk(tree):
        for e_child in ast.iter_child_nodes(node):
            if e_child==target_node:
                return node
                # print(f"Parent node of target node: {ast.unparse(e_child)} : {ast.unparse(node)}")
                # break

if __name__ == '__main__':
    # Example usage
    source_code = """
if x > 0:
    y = x * 2
    """

    tree = ast.parse(source_code)

    # Assuming you want to find the parent of the assignment node
    target_node = next(node for node in ast.walk(tree) if isinstance(node, ast.Assign))
    for node in ast.walk(tree):
            if isinstance(node,ast.Name) and ast.unparse(node)=="y":
                target_node=node
                break

    for node in ast.walk(tree):
        for e_child in ast.iter_child_nodes(node):
            if e_child==target_node:
                print(f"Parent node of target node: {ast.unparse(e_child)} : {ast.unparse(node)}")
                break
        else:
            continue
        break
        # if isinstance(node,ast.Name) and ast.unparse(node)=="y":
        #     # parent_node = parent_finder.find_parent(node)
        #     parent_finder = ParentFinder(node)
        #     parent_finder.visit(tree)
        #
        #     print(f"Parent node of target node: {ast.unparse(node)} : {parent_finder.parent_node}")
