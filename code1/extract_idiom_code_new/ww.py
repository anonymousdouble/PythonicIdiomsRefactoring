import ast,copy,ast_transform

def get_for_str(tmp_var,node,space = ""):
    code_str=""
    generators = node.generators
    for gen in generators:
        tar = gen.target
        iter = gen.iter
        ifs = gen.ifs
        for_str_list = [space, "for ", ast.unparse(tar), " in ", ast.unparse(iter), ":\n"]
        code_str+="".join(for_str_list)
        for ind_if, if_node in enumerate(ifs):
            space += "    "
            if_str_list = [space, "if ", ast.unparse(if_node), ":\n"]
            code_str += "".join(if_str_list)
        space += "    "

    key=ast.unparse(node.key)
    value=ast.unparse(node.value)
    code_str+=space+"".join([tmp_var, "[",key,"] = ",value,"\n"])

    return code_str
# def trans_elt(tmp_var,node,space):
#     if not isinstance(node,ast.ListComp):
#         if isinstance(node,ast.IfExp):
#             return "".join([space,"if ",ast.unparse(node.test),":\n", space+"    "+tmp_var,".add(",ast.unparse(node.body),")","\n",space+"else:\n"])+ \
#                    trans_elt(tmp_var, node.orelse, space+"    ")
#         else:
#             return "".join([space,tmp_var,".add(",ast.unparse(node),")","\n"])
#     else:
#         new_tmp_var=tmp_var[:-1]+str(int(tmp_var[-1])+1) if tmp_var[-1].isdigit() else tmp_var+"1"
#         return "".join([space,new_tmp_var,"= set([])\n"])+get_for_str(new_tmp_var,node, space)+"".join([space,tmp_var,".add(",new_tmp_var,")","\n"])
#
def is_intersect_var(targets,comprehension):
    tar_vars = set([])
    for e in ast.walk(targets[0]):
        if isinstance(e,ast.Name):
            tar_vars.add(ast.unparse(e))

    comprehension_vars=set([])
    for e in ast.walk(comprehension):
        if isinstance(e,ast.Name):
            comprehension_vars.add(ast.unparse(e))
    # print("tar_vars: ",tar_vars)
    # print("comprehension_vars: ", comprehension_vars)
    # print("tar_vars&comprehension_vars: ", tar_vars&comprehension_vars)
    return tar_vars&comprehension_vars
def has_many_value(targets):
    if len(targets)>1:
        return 1
    for e in targets:
        if isinstance(e,(ast.Tuple,ast.List)):
            return 1
    return 0
def transform_idiom_list_comprehension(parent_node,node):
    print("old_str: ",ast.unparse(parent_node),"\n*****\n",ast.unparse(node))
    new_node_list=[]
    tmp_var="tmp_DictComp0"
    ass_str_list=[]
    replace_flag=0
    if isinstance(parent_node,ast.Assign) and isinstance(parent_node.value,ast.DictComp):
        targets = parent_node.targets
        target = ast.unparse(targets[0])
        compre_iter = ast.unparse(parent_node.value.generators[0].iter)
        if has_many_value(targets) or is_intersect_var(targets, parent_node.value):
            ass_str_list = [tmp_var, " = ", "dict()\n"]
            replace_flag = 1
        else:

            tmp_var = ast.unparse(parent_node.targets[0])
            ass_str_list = [tmp_var, " = ", "dict()\n"]

        # tmp_var=ast.unparse(parent_node.targets[0])
        # ass_str_list=[tmp_var," = ","dict()\n"]
    else:
        ass_str_list=[tmp_var," = ","dict()\n"]
        replace_flag=1

    code="".join(ass_str_list)
    for new_node in ast.walk(ast.parse(code)):
        if isinstance(new_node, ast.Assign):
            new_node_list.append(new_node)
            break

    code=get_for_str(tmp_var, node, space="")
    for new_node in ast.walk(ast.parse(code)):
        if isinstance(new_node,ast.For):
            new_node_list.append(new_node)
            break
    # print("new_node_list: ",new_node_list)
    if replace_flag:

        for name in ast.walk(ast.parse(tmp_var)):
            if isinstance(name,ast.Name):
                # new_node_list.append(name)
                print("new_str: ","\n".join([ast.unparse(e) for e in new_node_list]))
                new_parent=ast_transform.Rewrite_compre(node,name).visit(copy.deepcopy(parent_node))
                print("new_parent: ",ast.unparse(new_parent))
                # new_node 第一个是替换的内容,第二个是加在前面的stmt, 第三个是加在后面的stmt
                return [parent_node, [ast.unparse(new_parent),"".join([ast.unparse(e)+"\n" for e in new_node_list]),""], parent_node]

                # return [node,parent_node,new_node_list]
    else:
        print("new_str: ", "\n".join([ast.unparse(e) for e in new_node_list]))
        return [parent_node, [ast.unparse(new_node_list[0]),"",ast.unparse(new_node_list[1])+"\n"], parent_node]

        # return [node,parent_node,new_node_list]

    '''
    new_node_str_list=[f"{ast.unparse(node.left)}"]
    for ind,e in enumerate(node.comparators[:-1]):
        op=node.ops[ind]
        op_str=get_op_str(op)
        new_node_str_list.append(op_str)
        new_node_str_list.append(ast.unparse(e))
        new_node_str_list.append("and")
        new_node_str_list.append(ast.unparse(e))
    new_node_str_list.append(get_op_str(node.ops[-1]))
    new_node_str_list.append(ast.unparse(node.comparators[-1]))
    new_node_str=" ".join(new_node_str_list)
    print("new str: ",new_node_str)
    for new_node in ast.walk(ast.parse(new_node_str)):
            if isinstance(new_node,ast.Expr):
                print('new str: ',ast.unparse(new_node))
                return [node, new_node]
    '''
def get_for_str(tmp_var,node,space = ""):
    code_str=""
    generators = node.generators
    elt=node.elt
    for gen in generators:
        tar = gen.target
        iter = gen.iter
        ifs = gen.ifs
        for_str_list = [space, "for ", ast.unparse(tar), " in ", ast.unparse(iter), ":\n"]
        code_str+="".join(for_str_list)
        for ind_if, if_node in enumerate(ifs):
            space += "    "
            if_str_list = [space, "if ", ast.unparse(if_node), ":\n"]
            code_str += "".join(if_str_list)
        space += "    "
    code_str+=trans_elt(tmp_var, elt, space)
    return code_str
def trans_elt(tmp_var,node,space):
    if not isinstance(node,ast.ListComp):
        if isinstance(node,ast.IfExp):
            return "".join([space,"if ",ast.unparse(node.test),":\n", space+"    "+tmp_var,".add(",ast.unparse(node.body),")","\n",space+"else:\n"])+ \
                   trans_elt(tmp_var, node.orelse, space+"    ")
        else:
            return "".join([space,tmp_var,".add(",ast.unparse(node),")","\n"])
    else:
        new_tmp_var=tmp_var[:-1]+str(int(tmp_var[-1])+1) if tmp_var[-1].isdigit() else tmp_var+"1"
        return "".join([space,new_tmp_var,"= set()\n"])+get_for_str(new_tmp_var,node, space)+"".join([space,tmp_var,".add(",new_tmp_var,")","\n"])

def is_intersect_var(targets,comprehension):
    tar_vars = set([])
    for e in ast.walk(targets[0]):
        if isinstance(e,ast.Name):
            tar_vars.add(ast.unparse(e))

    comprehension_vars=set([])
    for e in ast.walk(comprehension):
        if isinstance(e,ast.Name):
            comprehension_vars.add(ast.unparse(e))
    # print("tar_vars: ",tar_vars)
    # print("comprehension_vars: ", comprehension_vars)
    # print("tar_vars&comprehension_vars: ", tar_vars&comprehension_vars)
    return tar_vars&comprehension_vars
def has_many_value(targets):
    if len(targets)>1:
        return 1
    for e in targets:
        if isinstance(e,(ast.Tuple,ast.List)):
            return 1
    return 0
def visit_vars(target, list_vars,filter_str=""):
    # print(">>>>>>>ast.unparse(target): ",ast.unparse(target),filter_str,ast.unparse(target)!=filter_str)
    if ast.unparse(target)!=filter_str:
        # print(">>>>>>>continue ")
        # print(">>>>>>>target: ",target.__dict__)
        if isinstance(target, (ast.Name, ast.Subscript, ast.Attribute,ast.arg)):
            list_vars.append(target)

            # list_vars.append(ast.unparse(target))
            # print(">>>>>>>>the node: ",ast.unparse(target))
            for e in ast.iter_child_nodes(target):
                # print("the child is: ", ast.unparse(e))

                visit_vars(e, list_vars,filter_str)
        elif isinstance(target, ast.Call):
            if isinstance(target.func, ast.Attribute):
                # list_vars.append(
                #     target.func.value)
                visit_vars(target.func.value, list_vars, filter_str)
                for e in target.args:
                    visit_vars(e, list_vars,filter_str)
            else:
                for e in target.args:
                    visit_vars(e, list_vars,filter_str)
        else:
            for e in ast.iter_child_nodes(target):
                visit_vars(e, list_vars,filter_str)
def visit_filter_vars(target,list_vars,filter_node_attr="iter"):
    # if ast.unparse(target) != filter_str:
        # print(">>>>>>>target: ",target.__dict__)
        if isinstance(target, (ast.Name, ast.arg)):
            # list_vars.append(ast.unparse(target))
            # if hasattr(target,"value"):
            #     visit_large_vars(target.value, list_vars, filter_str)
            # else:
            list_vars.append(target)

        else:
            for e in ast.iter_child_nodes(target):
                if hasattr(e,filter_node_attr) and e==target.iter:
                    visit_filter_vars(e, list_vars, filter_node_attr)
                else:
                    continue

def visit_large_vars(target, list_vars,filter_str=""):
    if ast.unparse(target) != filter_str:
        # print(">>>>>>>target: ",target.__dict__)
        if isinstance(target, (ast.Name, ast.arg)):
            # list_vars.append(ast.unparse(target))
            # if hasattr(target,"value"):
            #     visit_large_vars(target.value, list_vars, filter_str)
            # else:
            list_vars.append(target)
        elif isinstance(target, ast.Call):
            if isinstance(target.func, ast.Attribute):
                # list_vars.append(
                #     target.func.value)
                visit_large_vars(target.func.value, list_vars, filter_str)
                for e in target.args:
                    visit_large_vars(e, list_vars,filter_str)
            else:
                for e in target.args:
                    visit_large_vars(e, list_vars,filter_str)
        else:
            for e in ast.iter_child_nodes(target):

                visit_large_vars(e, list_vars,filter_str)

def visit_filter_vars(target,list_vars,filter_node_attr=["target","targets"]):
    # if ast.unparse(target) != filter_str:
        # print(">>>>>>>target: ",target.__dict__)
    for e in ast.walk(target):
        for attr_str in filter_node_attr:
            if hasattr(e,attr_str):

                for var in ast.walk(getattr(e,attr_str)):
                    if isinstance(var, (ast.Name, ast.arg)):
                        list_vars.append(var)

# def visit_large_vars(target, list_vars,filter_str=""):
#     if ast.unparse(target) != filter_str:
#         # print(">>>>>>>target: ",target.__dict__)
#         if isinstance(target, (ast.Name, ast.arg)):
#             # list_vars.append(ast.unparse(target))
#             # if hasattr(target,"value"):
#             #     visit_large_vars(target.value, list_vars, filter_str)
#             # else:
#             list_vars.append(target)
#             # print(">>>>>>>>the node: ",ast.unparse(target))
#             # for e in ast.iter_child_nodes(target):
#             #     # print("the child is: ", ast.unparse(e))
#             #
#             #     visit_vars(e, list_vars)
#         elif isinstance(target, ast.Call):
#             if isinstance(target.func, ast.Attribute):
#                 # list_vars.append(
#                 #     target.func.value)
#                 visit_large_vars(target.func.value, list_vars, filter_str)
#                 for e in target.args:
#                     visit_large_vars(e, list_vars,filter_str)
#             else:
#                 for e in target.args:
#                     visit_large_vars(e, list_vars,filter_str)
#         else:
#             for e in ast.iter_child_nodes(target):
#                 visit_large_vars(e, list_vars,filter_str)
def is_use_var_in_P_child(P, child):
    child_tokens=[]
    visit_large_vars(child, child_tokens)
    child_tokens={ast.unparse(e) for e in child_tokens}
    child_filter_vars=[]
    visit_filter_vars(child, child_filter_vars)
    child_filter_vars={ast.unparse(e) for e in child_filter_vars}

    child_tokens=child_tokens-child_filter_vars
    print("child_tokens: ",child_tokens)

    # child_tokens=[e for e in ast.walk(child) if isinstance(e, (ast.Attribute,ast.Subscript,ast.Starred,ast.Name))]
    if isinstance(P, (ast.Assign, ast.AugAssign, ast.AnnAssign)):
        P=P.value

    other_tokens = []
    visit_large_vars(P, other_tokens,filter_str=ast.unparse(child))
    # visit_vars(P, other_tokens,filter_str=ast.unparse(child))
    other_tokens= {ast.unparse(e) for e in other_tokens}
    return other_tokens&child_tokens
    # intersect_vars = set([])
    # for e in child_tokens:
    #     e_list_vars=[]
    #     visit_vars(e, e_list_vars)
    #     e_list_vars=[ast.unparse(e) for e in e_list_vars]
    #     if set(e_list_vars)&set(other_tokens):
    #         intersect_vars.add(ast.unparse(e))
    #
    # return intersect_vars
    # for node in ast.walk(P):
    #     for e in ast.walk(node):
    #         if isinstance(e, (ast.Attribute,ast.Subscript,ast.Starred,ast.Name)):
    #             if e not in child_tokens:
    #                 other_tokens.append(e)
    # intersect_var=[]
    # intersect_var=set(child_tokens) & set(other_tokens)
    # for var in intersect_var:
    #     if ast.unparse(var) in
    # return set(child_tokens)&set(other_tokens)



def transform_idiom_list_comprehension(parent_node,node):
    print("old_str: ",ast.unparse(parent_node),"\n*****\n",ast.unparse(node))
    new_node_list=[]
    tmp_var="tmp_SetComp0"
    ass_str_list=[]
    replace_flag=0
    create_fun_flag=0
    intersect_vars=list(is_use_var_in_P_child(parent_node, node))
    print("create_fun_flag: ",create_fun_flag,intersect_vars)
    temporary_flag=1
    if intersect_vars:
        # create Function
        ass_str_list = [tmp_var, " = ", "[]\n"]
        replace_flag = 1
        create_fun_flag = 1
    else:
        # tmp var replace??
        if isinstance(parent_node,(ast.Assign,ast.AnnAssign)) and isinstance(parent_node.value,ast.SetComp): # and isinstance(parent_node.value,ast.ListComp)
            if isinstance(parent_node,(ast.Assign)):
                targets=parent_node.targets
            else:
                targets = [parent_node.target]
            # target = ast.unparse(targets[0])
            # compre_iter=ast.unparse(parent_node.value.generators[0].iter)
            print("has_many_value or is_intersect_var: ", has_many_value(targets), is_intersect_var(targets,node))
            if has_many_value(targets) or is_intersect_var(targets,node):

                ass_str_list = [tmp_var, " = ", "set()\n"]
                replace_flag = 1
            else:
                temporary_flag=0
                tmp_var=ast.unparse(targets[0])
                ass_str_list=[tmp_var," = ","set()\n"]
            # if parent_node.
        else:
            ass_str_list=[tmp_var," = ","set()\n"]
            replace_flag=1

    code="".join(ass_str_list)

    code_for=get_for_str(tmp_var, node, space="")
    for name in ast.walk(ast.parse(tmp_var)):
        if isinstance(name, ast.Name):
            replace_node =name
    if create_fun_flag:
        args_str=", ".join(intersect_vars)

        func_node_list = ["def my_comprehension_func(",args_str,"):\n    "]
        code_for_indent="".join(["    "+e+"\n" for e in code_for.split("\n") if e.strip()])
        func_node_list+=[code,code_for_indent]
        # print("func_code: ","".join(func_node_list),code_for.split("\n"))
        func_node_list.append("    return "+ tmp_var+"\n")
        func_code="".join(func_node_list)
        # print("func_code: ","".join(func_node_list),code_for.split("\n"))
        for new_node in ast.walk(ast.parse(func_code)):
            if isinstance(new_node, ast.FunctionDef):
                new_node_list.append(new_node)
                break
        # print("args_str: ",args_str)
        replace_code = "".join(["my_comprehension_func(",args_str,")"])
        for new_node in ast.walk(ast.parse(replace_code)):
            if isinstance(new_node, ast.Call):
                replace_node=new_node
                break
    else:
        for new_node in ast.walk(ast.parse(code)):
            if isinstance(new_node, ast.Assign):
                new_node_list.append(new_node)
                break
        for new_node in ast.walk(ast.parse(code_for)):
            if isinstance(new_node, ast.For):
                new_node_list.append(new_node)
                break

    if replace_flag:# 这里的替换表示是否将listcomprehension 替换为 创建的list的变量
        new_parent = ast_transform.Rewrite_compre(node, replace_node).visit(copy.deepcopy(parent_node))
        # print("new_parent: ", ast.unparse(new_parent))
        # print("new_str: ","\n".join([ast.unparse(e) for e in new_node_list]),ast.unparse(new_parent))
        complete_code="".join([ast.unparse(e) + "\n" for e in new_node_list])+ast.unparse(new_parent)
        print("complete_code: ",complete_code)
        # new_node 第一个是替换的内容,第二个是加在前面的stmt, 第三个是加在后面的stmt
        return [parent_node, [ast.unparse(new_parent), "".join([ast.unparse(e) + "\n" for e in new_node_list]), ""],
                parent_node,node,complete_code, temporary_flag, create_fun_flag]

        # for name in ast.walk(ast.parse(tmp_var)):
        #     if isinstance(name,ast.Name):
        #         # new_node_list.append(name)
        #         print("new_str: ","\n".join([ast.unparse(e) for e in new_node_list]))
        #         # return [node,new_node_list,parent_node]
        #         new_parent=ast_transform.Rewrite_compre(node,name).visit(copy.deepcopy(parent_node))
        #         print("new_parent: ",ast.unparse(new_parent))
        #         # new_node 第一个是替换的内容,第二个是加在前面的stmt, 第三个是加在后面的stmt
        #         return [parent_node, [ast.unparse(new_parent),"".join([ast.unparse(e)+"\n" for e in new_node_list]),""], parent_node]
        #
    else:
        # print("new_str: ", "\n".join([ast.unparse(e) for e in new_node_list]))
        # return [node,new_node_list,parent_node]
        #[ast.unparse(e)+"\n" if ind!=0 else ast.unparse(e) for ind,e in enumerate(new_node_list)]
        complete_code = ast.unparse(new_node_list[0])+"\n" + ast.unparse(new_node_list[1])+"\n"
        print("complete_code: ", complete_code)
        return [parent_node, [ast.unparse(new_node_list[0]),"",ast.unparse(new_node_list[1])+"\n"], parent_node,node, complete_code,temporary_flag, create_fun_flag]
