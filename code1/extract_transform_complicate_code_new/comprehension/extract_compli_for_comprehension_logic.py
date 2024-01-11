import sys,ast,os
import tokenize
sys.path.append("/mnt/zejun/smp/code1/")
import complicated_code_util
import util,copy
from extract_simp_cmpl_data import ast_util
# from code1.extract_simp_cmpl_data import ast_util
from tokenize import tokenize
from io import BytesIO

# dict_repo_file_python = util.load_json(util.data_root, "python3_1000repos_files_info")

'''
get comprehension node
Block=> Assign;...; For
For=>”for” ( For| If|If-else|body)
If=>”if” (body| For| If| If-else)
If-else=>”if” body “else” (body| If-else)
body=> (Assign|Call)*;Append*
并且里面只有一个写变量
for

    b.append()
    
    a.append(b)

'''
# const_empty_list=["[]"]#["dict()","{}"]#["()"]
#
# const_func_name="add"

def get_func_name(one_body):
    pre_name,call_name=None,None
    if isinstance(one_body, ast.Expr) and isinstance(one_body.value, ast.Call):
        # print("come here")
        call_front = one_body.value.func
        if isinstance(call_front, ast.Name):
            call_name = ast.unparse(call_front)
        elif isinstance(call_front, ast.Attribute):
            call_name = call_front.attr
            pre_name=ast.unparse(call_front.value)
        else:
            call_name = ast.unparse(call_front)
    return pre_name,call_name


def whether_fun_is_append(one_body,assign_block_list,const_func_name="append"):
    #print("one_body: ",ast.unparse(one_body),one_body.__dict__)
    if isinstance(one_body, ast.Expr) and isinstance(one_body.value, ast.Call):
        # print("come here")
        call_front = one_body.value.func

        # print("call dict: ", call_front.__dict__)

        if isinstance(call_front, ast.Name):
            call_name = ast.unparse(call_front)
        elif isinstance(call_front, ast.Attribute):
            call_name = call_front.attr
        else:
            call_name = ast.unparse(call_front)
        #print("the func name: ", call_name)
        if call_name ==const_func_name:
            assign_block_list.append([one_body])
            return True
    elif isinstance(one_body,ast.Call):
        call_front = one_body.func

        # print("call dict: ", call_front.__dict__)
        if isinstance(call_front, ast.Name):
            call_name = ast.unparse(call_front)
        elif isinstance(call_front, ast.Attribute):
            call_name = call_front.attr
        else:
            call_name = ast.unparse(call_front)
        # print("the func name: ", call_name)
        if call_name == const_func_name:
            assign_block_list.append([one_body])
            return True
    return False

def else_traverse(if_body,assign_block_list,const_func_name):
    else_body_list = if_body.orelse
    if len(else_body_list) > 1:
        return False
    else:
        else_body_one = else_body_list[0]
        if isinstance(else_body_one, ast.If):
            or_else = else_body_one.orelse
            if not or_else:
                return False
            else:
                return if_else_traverse(else_body_one,assign_block_list,const_func_name)
        return whether_fun_is_append(else_body_one,assign_block_list,const_func_name)



def if_else_traverse(if_body,assign_block_list,const_func_name):
    if_body_list=if_body.body
    # else_body_list=if_body.orelse
    if len(if_body_list)==1:
        if_body_flag =whether_fun_is_append(if_body_list[0],assign_block_list,const_func_name)
    else:
        return False
    #print("if body flag: ",if_body_flag)

    return if_body_flag and else_traverse(if_body,assign_block_list,const_func_name)
def if_traverse(one_body,assign_block_list,const_func_name):
    orelse = one_body.orelse
    if_body=one_body.body
    if not orelse:
        return for_traverse(one_body,assign_block_list,const_func_name)
    else:
        #print("it is if-else node: ", ast.unparse(one_body))
        return if_else_traverse(one_body,assign_block_list,const_func_name)

class Rewrite(ast.NodeTransformer):
    def __init__(self,node,new_node):
        self.old_node =node
        self.new_node =new_node
    def visit_Name(self, node):
        if ast.unparse(node)==ast.unparse(self.old_node):
            return self.new_node
        return node
    # def generic_visit(self, node):
    #     if hasattr(node, "body"):
    #         if hasattr(node,"lineno"):
    #             if node.lineno==self.old_node.lineno and ast.unparse(node)==ast.unparse(self.old_node):
    #                 return self.new_node
    #
    #         for ind,child in enumerate(node.body):
    #                 node.body[ind] = self.generic_visit(node.body[ind])
    #     return node
def occur(node,find_node):
    for e in ast.walk(node):
        if isinstance(e,ast.AST) and ast.unparse(e)==ast.unparse(find_node):
            return 1
    return 0
def tranform_to_one_line(for_body_list):
    for_body_list_copy=copy.deepcopy(for_body_list)
    # print(">>>for_body_list_copy: ",ast.unparse(for_body_list_copy[0]),ast.unparse(for_body_list_copy[1]))
    # pre_ass=for_body_list[0]

    # now_stmt_list=[pre_ass]
    Map_var=dict()
    # tar_str = ast.unparse(pre_ass.targets)
    # val = pre_ass.value
    # Map_var[tar_str] = val
    unused_var=set([])
    unoccured_list=[]
    # unused_var = set([])
    for ind,e in enumerate(for_body_list_copy[:]):

        if isinstance(e,ast.Assign):
            # print(">>>>e assign: ", ast.unparse(e), e.targets)
            if not (isinstance(e.targets,list) and len(e.targets)==1 and  isinstance(e.targets[0],ast.Name)):
                return False, []
            flag_unuse=1
            for key, replace_value in Map_var.items():
                for key_node in ast.walk(ast.parse(key)):
                    if isinstance(key_node,ast.Name):
                        tar_node=key_node
                        break
                else:
                    # print(">>>come here")
                    return False, []
                # print(">>>e,tar_node: ",ast.unparse(e),tar_node)
                flag_occur=occur(e,tar_node)
                if flag_occur:
                    flag_unuse=0
                    # print(">>>tar_node, replace_value: ",ast.unparse(tar_node), ast.unparse(replace_value),ast.unparse(e))
                    # try:
                    rw = Rewrite(tar_node, replace_value)
                    e.value = rw.visit(e.value)
                    # except:
                    #      return False, []
                    # print(">>>new e: ", ast.unparse(e))
                    if key in unused_var:
                        unused_var.remove(key)
            tar_str = ast.unparse(e.targets[0])
            Map_var[tar_str] = copy.deepcopy(e.value)
            if flag_unuse:
                unused_var.add(tar_str)
            # print(">>>Map_var,unused_var: ",Map_var,unused_var)
        elif ind==len(for_body_list_copy)-1:
            for key, replace_value in Map_var.items():
                for key_node in ast.walk(ast.parse(key)):
                    if isinstance(key_node, ast.Name):
                        tar_node = key_node
                        break
                else:
                    return False, []
                # print(">>>tar_node",tar_node,ast.unparse(tar_node))
                flag_occur = occur(e, tar_node)
                if flag_occur:
                    rw = Rewrite(tar_node, replace_value)
                    e = rw.visit(e)
                    # print(">>>new e: ", ast.unparse(e))
                    if key in unused_var:
                        unused_var.remove(key)
            if unused_var:
                # print("unused_var: ",unused_var)
                return False, []
            else:
                # print(">>>final new e: ", ast.unparse(e),"\n>>>>",e)
                return True, [e]
        else:
            # print("else: ",ast.unparse(e))
            return False,[]
    return False, []
def for_traverse(node,assign_block_list,const_func_name):
    for_body_list = node.body
    if isinstance(node, ast.For) and node.orelse:
       # print("come here")
        return False
    if len(for_body_list)>1:
            # print(">>>>>come len(for_body_list)>1: ",ast.unparse(for_body_list))
        # try:
        #     for_old_body_list=copy.deepcopy(for_body_list)
            flag_one,for_body_list=tranform_to_one_line(for_body_list)
            # print(">>>>> flag_one,for_body_list", flag_one,"\n",ast.unparse(node),ast.unparse(for_body_list))
            if not flag_one:

                return False
            node.body=for_body_list
    if len(for_body_list) == 1:
        one_body=for_body_list[0]
        if isinstance(one_body, ast.For):
            #print("come here for_traverse")
            return for_traverse(one_body,assign_block_list,const_func_name)
        elif isinstance(one_body, ast.If):
            #print("it is if node")
            return if_traverse(one_body,assign_block_list,const_func_name)

        elif isinstance(one_body, ast.Expr):
            #print("come here for_traverse and it is an Expr",whether_fun_is_append(one_body,assign_block_list))
            return whether_fun_is_append(one_body,assign_block_list,const_func_name)
        else:

            #print("the for/if sentences has other stmts so cannot transform such as try stmt", ast.unparse(one_body),type(one_body))
            return False
    # else:
    return False
'''
beg1 end1
beg2 end2
'''

def filter_overlap(code_index_list):
    no_overlap_list=[]
    if len(code_index_list)==1:
        return code_index_list
    for i in range(len(code_index_list)):
        code=code_index_list[i]
        beg=code[0].lineno
        end=code[0].end_lineno
        for j in range(len(code_index_list)):
            if i==j:
                continue
            fuzhu_beg = code_index_list[j][0].lineno
            fuzhu_end = code_index_list[j][0].end_lineno
            if beg>=fuzhu_beg and end<=fuzhu_end:
                break
        else:
            no_overlap_list.append(code)

    return no_overlap_list
# def filter_overlap(code_index_list):
#     no_overlap_list=[]
#     if len(code_index_list)==1:
#         return code_index_list
#     for i in range(len(code_index_list)-1):
#         code1=code_index_list[i]
#         beg=code1[2]
#         end=code1[3]
#         for j in range(i+1,len(code_index_list)):
#             fuzhu_beg = code_index_list[j][2]
#             fuzhu_end = code_index_list[j][3]
#             if beg>=fuzhu_beg and end<=fuzhu_end:
#                 break
#         else:
#             no_overlap_list.append(code1)
#
#
#     return no_overlap_list
def is_use_var(next_child, vars):
    s = ast.unparse(next_child)
    if s != list(vars)[0]:
        g = tokenize(BytesIO(s.encode('utf-8')).readline)  # tokenize the string
        for toknum, to_child, _, _, _ in g:
            if to_child.strip() == list(vars)[0]:
                return 1
    return 0
'''
1.首先for_node中除了对vars使用追加元素，不应该再被使用
    特别地有时候for_node中会包含这个文件中自定义的函数调用，此时我们需要获得这个函数代码，判断是否使用了vars
2. 找到将vars赋值为空的语句ass，然后判断ass与for_node之间是否使用了vars，这种情况也不可以被简化
还要判断ass所在层的在for_node后面的代码中是否使用了vars，此时决定着是否可以remove ass
特别的对于如果ass在更外层相比于for_node,此时如果ass所在层内中，for_node属于for节点的body此时也不可以化简为comprehension
'''
# def whether_first_var_is_empty_assign(tree,for_node,vars,const_func_name="append",const_empty_list=["[]"]):
#     assign_stmt = None
#     assign_stmt_lineno = None
#     ass_block_lineno = None
#     ass_block_end_lineno = None
#     flag=0
#     # start_lineno=0
#     # print("the var: ",vars)
#
#     def visit_single_vars(target, list_vars):
#         # print(">>>>>>>target: ",target.__dict__)
#         if isinstance(target, (ast.Name)):
#             list_vars.append(ast.unparse(target))
#         elif isinstance(target, ast.Subscript):
#             list_vars.append(ast.unparse(target))
#             visit_single_vars(target.value, list_vars)
#         elif isinstance(target, ast.Attribute):
#             # print("attr: ", ast.unparse(target))
#             list_vars.append(ast.unparse(target))
#             visit_single_vars(target.value, list_vars)
#         # else:
#         #     print("visit_single_vars else node: ", ast.unparse(target))
#         #     for e in ast.iter_child_nodes(target):
#         #         print("visit_single_vars e: ", e, ast.unparse(e))
#         #         visit_single_vars(e, list_vars)
#     def get_time_var(vars):
#         all_var_list = []
#         for ind,e_var in enumerate(ast.walk(ast.parse(list(vars)[0]))):
#
#             if ast.unparse(e_var)==list(vars)[0] and isinstance(e_var,(ast.Subscript,ast.Attribute,ast.Name)):
#                 # print("var: ",e_var,ast.unparse(e_var))
#                 visit_single_vars(e_var, all_var_list)
#                 break
#         return all_var_list
#     def whether_contain_var(node,vars,time_var_list):
#         count=0
#
#         s = ast.unparse(node)
#         if s != list(vars)[0]:
#             g = tokenize(BytesIO(s.encode('utf-8')).readline)  # tokenize the string
#
#             for toknum, child, _, _, _ in g:
#                 # print("child: ",child)
#                 if child in time_var_list:#== list(vars)[0]:
#                     count+=1
#                     # print("yes use more than one time: ", s)
#         return count
#
#     time_var_list=get_time_var(vars)
#     remove_ass_flag = 0
#     time=whether_contain_var(for_node, vars,time_var_list)
#     # print("time: ",time)
#     append_time = 0
#     for child in ast.walk(for_node):
#
#         # if ast.unparse(child)==list(vars)[0]:
#         #     time+=1
#         #     if time-append_time > 0:
#         #         print("come here the for node use var more than one time ",list(vars)[0])
#         #         flag = 1
#         #         break
#         if isinstance(child, ast.Call):
#             a = []
#             # if whether_fun_is_append(child, a, const_func_name):
#             #     append_time+=len(time_var_list)
#             append_time += whether_fun_is_append(child, a, const_func_name)
#
#             def is_call_use_vars(tree, fun_name, time_var_list):
#                 # print(">>>>>>.come is_call_use_vars: ", fun_name)
#                 ana_py_fun = ast_util.Fun_Analyzer()
#                 ana_py_fun.visit(tree)
#                 for tree_fun, class_name in ana_py_fun.func_def_list:
#                     if hasattr(tree_fun, "name"):
#                         each_fun_name = tree_fun.name
#                         # print(">>>>>>each_fun_name: ", fun_name)
#                         if each_fun_name == fun_name:
#                             for child in ast.walk(tree_fun):
#                                 if ast.unparse(child) in time_var_list:
#                                     # print("yes the call use vars: ", each_fun_name)
#                                     return 1
#                 return 0
#
#             fun_name = ast.unparse(child.func).split(".")[-1]
#             call_use_var_flag = is_call_use_vars(tree, fun_name, time_var_list)
#             if call_use_var_flag:
#                 flag = 1
#                 return flag, assign_stmt_lineno, assign_stmt, remove_ass_flag
#         # time += whether_contain_var(child, vars)
#     # print("append_time: ", append_time)
#     if time - append_time > 0:
#             # print("come here the for node use var more than one time ", list(vars)[0])
#             flag = 1
#             return flag, assign_stmt_lineno, assign_stmt, remove_ass_flag
#             # break
#     for_node_block_record=None
#     for node in ast.walk(tree):
#         # print(">>>>> walk the node is: ", node,ast.unparse(node))
#         # if not hasattr(node,"lineno"):
#         #     print("yes",node)
#         #     continue
#
#         if  hasattr(node,"lineno") and node.lineno==for_node.lineno:
#             # print("come the for_node")
#             break
#         # for child in ast.iter_child_nodes(node):
#         if hasattr(node,'body') and isinstance(node.body, list) and \
#             ((hasattr(node,'lineno') and node.lineno<for_node.lineno<=node.end_lineno) or (hasattr(node.body[0],'lineno') and node.body[0].lineno<for_node.lineno<node.body[-1].end_lineno)):
#
#             # print(">>>>> the node is: ",ast.unparse(node))
#             for child in node.body:
#                 # print("come here node: ",child,ast.unparse(child),isinstance(child,ast.Expr))
#
#                 if isinstance(child, ast.Assign):
#                     if ast.unparse(child).strip().split("=")[0].strip() == list(vars)[0] and ast.unparse(child.value) in const_empty_list:
#                         assign_stmt = child
#                         assign_stmt_lineno = child.lineno
#                         ass_block_end_lineno=node.end_lineno if hasattr(node,'lineno') else node.body[0].lineno
#                         # if ass_block_end_lineno < for_node.lineno:
#                         #     remove_ass_flag = 0
#
#                         for_node_block_record = node
#                         flag = 2
#
#
#                 # elif assign_stmt_lineno:
#                 #     for child_child in ast.walk(child):
#                 #         if child_child==for_node:
#                 #             for_node_block_record = node
#                 #             break
#     # print("whether has assign: ",assign_stmt_lineno)
#     if  for_node_block_record:
#         # print(">>>>>>>come here for_node_block_record:\n ",ast.unparse(for_node_block_record))
#         for child in ast.iter_child_nodes(for_node_block_record):#.body:
#             if child==for_node:
#                 remove_ass_flag=1
#         for node in ast.walk(for_node_block_record):
#             # 在ass和for_node之间不可以使用变量vars
#             if hasattr(node,"end_lineno") and hasattr(node,"lineno"):
#                 if node != assign_stmt and node.end_lineno < for_node.lineno and node.lineno > assign_stmt_lineno:
#                     s = ast.unparse(node)
#
#                     if s != list(vars)[0]:
#                         g = tokenize(BytesIO(s.encode('utf-8')).readline)  # tokenize the string
#                         for toknum, child, _, _, _ in g:
#                             if child.strip() in time_var_list:# list(vars)[0]:
#                                 flag = 1
#                                 # print("yes use more than one time: ",vars,s,"\n>>>>>>>>>",ast.unparse(for_node))
#                                 return flag, assign_stmt_lineno, assign_stmt, remove_ass_flag
#             if isinstance(node, (ast.For, ast.While,
#                                            ast.AsyncFor)) and for_node.lineno>node.lineno > assign_stmt.lineno and node.end_lineno >= for_node.end_lineno:
#
#                     # print(">>>>>>>>come here ")
#                     return 1, assign_stmt_lineno, assign_stmt, remove_ass_flag
#
#
#     else:
#         return 1,assign_stmt_lineno,assign_stmt,remove_ass_flag
#     return flag,assign_stmt_lineno,assign_stmt,remove_ass_flag

def whether_first_var_is_empty_assign(tree,for_node,vars,const_func_name="append",const_empty_list=["[]","list()"]):
    assign_stmt = None
    assign_stmt_lineno = None
    ass_block_lineno = None
    ass_block_end_lineno = None
    flag=0
    # start_lineno=0
    # print("the var: ",vars)

    def visit_single_vars(target, list_vars):
        # print(">>>>>>>target: ",target.__dict__)
        if isinstance(target, (ast.Name)):
            list_vars.append(ast.unparse(target))
        elif isinstance(target, ast.Subscript):
            list_vars.append(ast.unparse(target))
            visit_single_vars(target.value, list_vars)
        elif isinstance(target, ast.Attribute):
            # print("attr: ", ast.unparse(target))
            list_vars.append(ast.unparse(target))
            visit_single_vars(target.value, list_vars)
        # else:
        #     print("visit_single_vars else node: ", ast.unparse(target))
        #     for e in ast.iter_child_nodes(target):
        #         print("visit_single_vars e: ", e, ast.unparse(e))
        #         visit_single_vars(e, list_vars)
    def get_time_var(vars):
        all_var_list = []
        for ind,e_var in enumerate(ast.walk(ast.parse(list(vars)[0]))):

            if ast.unparse(e_var)==list(vars)[0] and isinstance(e_var,(ast.Subscript,ast.Attribute,ast.Name)):
                # print("var: ",e_var,ast.unparse(e_var))
                visit_single_vars(e_var, all_var_list)
                break
        return all_var_list
    def whether_contain_var(node,vars,time_var_list):
        count=0

        s = ast.unparse(node)
        if s != list(vars)[0]:
            g = tokenize(BytesIO(s.encode('utf-8')).readline)  # tokenize the string

            for toknum, child, _, _, _ in g:
                # print("child: ",child)
                if child in time_var_list:#== list(vars)[0]:
                    count+=1
                    # print("yes use more than one time: ", s,child)
        return count

    time_var_list=get_time_var(vars)
    # print(">>>>time_var_list: ",time_var_list)
    remove_ass_flag = 0
    time=whether_contain_var(for_node, vars,time_var_list)
    # print("time: ",time)
    append_time = 0
    for child in ast.walk(for_node):

        # if ast.unparse(child)==list(vars)[0]:
        #     time+=1
        #     if time-append_time > 0:
        #         print("come here the for node use var more than one time ",list(vars)[0])
        #         flag = 1
        #         break
        if isinstance(child, ast.Call):
            a = []
            # if whether_fun_is_append(child, a, const_func_name):
            #     append_time+=len(time_var_list)
            append_time += whether_fun_is_append(child, a, const_func_name)

            def is_call_use_vars(tree, fun_name, time_var_list):
                # print(">>>>>>.come is_call_use_vars: ", fun_name)
                ana_py_fun = ast_util.Fun_Analyzer()
                ana_py_fun.visit(tree)
                for tree_fun, class_name in ana_py_fun.func_def_list:
                    if hasattr(tree_fun, "name"):
                        each_fun_name = tree_fun.name
                        # print(">>>>>>each_fun_name: ", fun_name)
                        if each_fun_name == fun_name:
                            for child in ast.walk(tree_fun):
                                if ast.unparse(child) in time_var_list:
                                    print("yes the call use vars: ", each_fun_name)
                                    return 1
                return 0

            fun_name = ast.unparse(child.func).split(".")[-1]
            call_use_var_flag = is_call_use_vars(tree, fun_name, time_var_list)
            if call_use_var_flag:
                flag = 1
                return flag, assign_stmt_lineno, assign_stmt, remove_ass_flag
        # time += whether_contain_var(child, vars)
    # print("append_time: ", append_time)
    # if time - append_time > 0:
    #         print("come here the for node use var more than one time ", list(vars)[0])
    #         flag = 1
    #         return flag, assign_stmt_lineno, assign_stmt, remove_ass_flag
    #         # break

    for_node_block_record=None
    for node in ast.walk(tree):
        # print(">>>>> walk the node is: ", node,ast.unparse(node))
        # if not hasattr(node,"lineno"):
        #     print("yes",node)
        #     continue

        if  hasattr(node,"lineno") and node.lineno==for_node.lineno:
            # print("come the for_node,",ast.unparse(node))
            break
        # for child in ast.iter_child_nodes(node):
        if hasattr(node,'body') and isinstance(node.body, list) and \
            ((hasattr(node,'lineno') and node.lineno<for_node.lineno<=node.end_lineno) or (hasattr(node.body[0],'lineno') and node.body[0].lineno<for_node.lineno<node.body[-1].end_lineno)):

            for child in node.body:

                if isinstance(child, ast.Assign):
                    # print("come here node: ", child, ast.unparse(child), ast.unparse(child.value), const_empty_list,list(vars)[0],ast.unparse(child).strip().split("=")[0].strip())
                    # print("whether condition satisfy: ",ast.unparse(child).strip().split("=")[0].strip()== list(vars)[0], ast.unparse(child.value) in const_empty_list)
                    if ast.unparse(child).strip().split("=")[0].strip() == list(vars)[0] and ast.unparse(child.value) in const_empty_list:
                        # print(">>>>> the node is: ", ast.unparse(child).strip().split("=")[0].strip(), list(vars),
                        #       ast.unparse(child), const_empty_list, ast.unparse(child.value))

                        assign_stmt = child
                        assign_stmt_lineno = child.lineno
                        ass_block_end_lineno=node.end_lineno if hasattr(node,'lineno') else node.body[0].lineno
                        # if ass_block_end_lineno < for_node.lineno:
                        #     remove_ass_flag = 0

                        for_node_block_record = node
                        flag = 2


                # elif assign_stmt_lineno:
                #     for child_child in ast.walk(child):
                #         if child_child==for_node:
                #             for_node_block_record = node
                #             break
    # print("whether has assign: ",assign_stmt_lineno)
    if  for_node_block_record:
        # print(">>>>>>>come here for_node_block_record:\n ",flag)
        for child in ast.iter_child_nodes(for_node_block_record):#.body:
            if child==for_node:
                remove_ass_flag=1
                break
        for node in ast.walk(for_node_block_record):
            # 在ass和for_node之间不可以使用变量vars
            if hasattr(node,"end_lineno") and hasattr(node,"lineno"):
                if node != assign_stmt and node.end_lineno < for_node.lineno and node.lineno > assign_stmt_lineno:
                    s = ast.unparse(node)

                    if s != list(vars)[0]:
                        g = tokenize(BytesIO(s.encode('utf-8')).readline)  # tokenize the string
                        for toknum, child, _, _, _ in g:
                            if child.strip() in time_var_list:# list(vars)[0]:
                                flag = 3
                                # print("yes use more than one time: ",remove_ass_flag,vars,s,"\n>>>>>>>>>",ast.unparse(for_node))
                                return flag, assign_stmt_lineno, assign_stmt, 0

            if isinstance(node, (ast.For, ast.While,
                                           ast.AsyncFor)) and for_node.lineno>node.lineno > assign_stmt.lineno and node.end_lineno >= for_node.end_lineno:

                    # print(">>>>>>>>come here,",ast.unparse(node))
                    return 3, assign_stmt_lineno, assign_stmt, 0
            # print(">>>>>>>>no flag,")
        #         it does not have'''
        #         elif assign_stmt_lineno:
        #             '''
        #             如果ass和for_node在同一层则不需要去除，
        #             如果ass的层数在更外层，则我们需要看这一层后面是否使用了vars 如果使用了vars则ass的赋值为空的语句不可以删除
        #             如果ass在更外层，在ass所在层的后面节点中，如果存在for节点，并且for节点包含该for_node，则如果for_node后使用了vars，该for_node仍然不可以简化。
        #             ass=[]
        #             for :
        #                 for :
        #                     ass.append
        #             '''
        #             # print("ass_block_end_lineno: ",ass_block_end_lineno,for_node.lineno)
        #
        #             if isinstance(child,ast.For) and child.lineno==for_node.lineno:
        #                 flag = 2
        #                 break
        #                 # return 2, assign_stmt_lineno, assign_stmt, remove_ass_flag
        #
        #             for next_child in ast.walk(child):
        #                 if not hasattr(next_child, "lineno"):
        #                     continue
        #                 if isinstance(next_child,(ast.For,ast.While,ast.AsyncFor)) and next_child.lineno<for_node.lineno and next_child.end_lineno>=for_node.end_lineno:
        #                     # print(">>>>>>>>come here ")
        #                     return 1, assign_stmt_lineno, assign_stmt, remove_ass_flag
        #
        #                     # for for_child in ast.walk(next_child):
        #                         # if hasattr(for_child,'lineno'):
        #                         #     if for_child.lineno>for_node.end_lineno:
        #                         #         if is_use_var(for_child,vars):
        #                         #             flag=1
        #                         #             print(">>>>>>>>come here ")
        #                         #             return flag, assign_stmt_lineno, assign_stmt, remove_ass_flag
        #                 elif  next_child.lineno>for_node.end_lineno:
        #                     if is_use_var(next_child, vars):
        #                         remove_ass_flag = 0
        #                         # break
        #             return flag,assign_stmt_lineno, assign_stmt, remove_ass_flag
        #         '''
        # # 在ass和for_node之间不可以使用变量vars
        # if assign_stmt_lineno and node!=assign_stmt and node.end_lineno<for_node.lineno and node.lineno>assign_stmt_lineno :
        #     s=ast.unparse(node)
        #
        #     if s!=list(vars)[0]:
        #         g = tokenize(BytesIO(s.encode('utf-8')).readline)  # tokenize the string
        #         for toknum, child, _, _, _ in g:
        #             if child.strip() == list(vars)[0]:
        #                 flag = 1
        #                 # print("yes use more than one time: ",vars,s,"\n>>>>>>>>>",ast.unparse(for_node))
        #                 break
        #         if flag==1:
        #             break
        # 判断跟compreh不属于同一个父母的在for_node后面的代码片段是否使用了变量vars
        # if assign_stmt_lineno and node!=assign_stmt and node.lineno>ass_parent.end_lineno:
        #     s = ast.unparse(node)
        #
        #     if s != list(vars)[0]:
        #         g = tokenize(BytesIO(s.encode('utf-8')).readline)  # tokenize the string
        #         for toknum, child, _, _, _ in g:
        #             if child.strip() == list(vars)[0]:
        #                 remove_ass_flag = 0
        #                 print("no we cannot remove the ass: ","\n>>>>>>>>>",ast.unparse(for_node),"\n>>>>>>>>>",ast.unparse(node))
        #                 break
        #         if remove_ass_flag == 0:
        #             break
    else:
        # print(">>>come else")
        return 1,assign_stmt_lineno,assign_stmt,remove_ass_flag
    # print("flag: ",flag)
    return flag,assign_stmt_lineno,assign_stmt,remove_ass_flag
'''
def whether_first_var_is_empty_assign(tree,for_node,vars,const_func_name="append",const_empty_list=["[]"]):
    assign_stmt=None
    assign_stmt_lineno=None
    flag=0
    # start_lineno=0
    # print("the var: ",vars)


    def whether_contain_var(node,vars):
        count=0
        s = ast.unparse(node)
        if s != list(vars)[0]:
            g = tokenize(BytesIO(s.encode('utf-8')).readline)  # tokenize the string

            for toknum, child, _, _, _ in g:
                if child == list(vars)[0]:
                    count+=1
                    # print("yes use more than one time: ", s)
        return count

    time=whether_contain_var(for_node, vars)
    append_time = 0
    for child in ast.walk(for_node):

        # if ast.unparse(child)==list(vars)[0]:
        #     time+=1
        #     if time-append_time > 0:
        #         print("come here the for node use var more than one time ",list(vars)[0])
        #         flag = 1
        #         break
        if isinstance(child, ast.Call):
            a = []
            append_time += whether_fun_is_append(child, a,const_func_name)

            def is_call_use_vars(tree, fun_name, vars):
                # print(">>>>>>.come is_call_use_vars: ", fun_name)
                ana_py_fun = ast_util.Fun_Analyzer()
                ana_py_fun.visit(tree)
                for tree_fun, class_name in ana_py_fun.func_def_list:
                    if hasattr(tree_fun, "name"):
                        each_fun_name = tree_fun.name
                        # print(">>>>>>each_fun_name: ", fun_name)
                        if each_fun_name == fun_name:
                            for child in ast.walk(tree_fun):
                                if ast.unparse(child) == list(vars)[0]:
                                    # print("yes the call use vars: ", each_fun_name)
                                    return 1
                return 0

            fun_name = ast.unparse(child.func).split(".")[-1]
            call_use_var_flag = is_call_use_vars(tree, fun_name, vars)
            if call_use_var_flag:
                flag = 1
                return flag, assign_stmt_lineno, assign_stmt
        # time += whether_contain_var(child, vars)
    if time - append_time > 0:
            # print("come here the for node use var more than one time ", list(vars)[0])
            flag = 1
            return flag, assign_stmt_lineno, assign_stmt
            # break
    for node in ast.walk(tree):
        if not hasattr(node,"lineno"):
            continue

        if node.lineno==for_node.lineno:
            break
        if isinstance(node, ast.Assign):
            # print("the assign: ",ast.unparse(node),ast.unparse(node).strip().split("=")[0].strip())
            if ast.unparse(node).strip().split("=")[0].strip()==list(vars)[0] and ast.unparse(node.value) in const_empty_list:
                assign_stmt=node
                assign_stmt_lineno=node.lineno
                flag = 2
        if assign_stmt_lineno and node.end_lineno<for_node.lineno and node.lineno>assign_stmt_lineno :
            s=ast.unparse(node)

            if s!=list(vars)[0]:
                g = tokenize(BytesIO(s.encode('utf-8')).readline)  # tokenize the string
                for toknum, child, _, _, _ in g:
                    if child.strip() == list(vars)[0]:
                        flag = 1
                        # print("yes use more than one time: ",vars,s,"\n>>>>>>>>>",ast.unparse(for_node))
                        break
                if flag==1:
                    break
    return flag,assign_stmt_lineno,assign_stmt
'''
'''
def whether_first_var_is_empty_assign(tree,for_node,vars,const_empty_list=["[]"]):
    assign_stmt=None
    assign_stmt_lineno=None
    flag=0
    # print("the var: ",vars)
    for node in ast.walk(tree):
        if not hasattr(node,"lineno"):
            continue

        if node.lineno==for_node.lineno:
            break
        if isinstance(node, ast.Assign):
            # print("the assign: ",ast.unparse(node),ast.unparse(node).strip().split("=")[0].strip())
            if ast.unparse(node).strip().split("=")[0].strip()==list(vars)[0] and ast.unparse(node.value) in const_empty_list:
                assign_stmt=node
                assign_stmt_lineno=node.lineno
                flag = 2
        if assign_stmt_lineno and node.lineno < for_node.lineno and node.lineno > assign_stmt_lineno:
            for child in ast.walk(node):
                if ast.unparse(child).strip().split("=")[0].strip() == list(vars)[0]:
                    flag = 1
                    break
            else:
                continue
            if flag == 1:
                break


    return flag,assign_stmt_lineno,assign_stmt
'''
def get_complicated_for_comprehen_code_list(tree,content,const_empty_list=["[]"],const_func_name="append"):
    #code1 = ast.unparse(tree)
    code_index_start_end_list = []

    start_lineno=tree.body[0].lineno
    flag_occur_for=None
    #code1 = "\n".join(content.split("\n")[start_lineno - 1:])
    for ind_line,node in enumerate(ast.walk(tree)):

            #print("start_line: ",node.lineno)
        if isinstance(node, ast.For):
            flag_occur_for=node
            #print("node_line: ",ast.unparse(node),node.lineno, node.end_lineno)
            # if node.lineno!=1674:
            #     continue

            assign_block_list=[]
            #print("it is what: ",for_traverse(node,assign_block_list))
            if for_traverse(node,assign_block_list,const_func_name):#判断for语句是否满足For_Match
                # print("maybe comrephension")
                '''
                判断是否是同一个变量的append
                '''
                vars = set([])
                for each_block in assign_block_list:
                    pre_name,call_name=get_func_name(each_block[0])
                    vars.add(pre_name)
                if len(vars)!=1:
                    continue
                # print("for node: ",ast.unparse(node),node.lineno)
                '''
                判断是否是同一个变量的append
                '''
                flag,assign_stmt_lineno,assign_stmt,remove_ass_flag=whether_first_var_is_empty_assign(tree, node, vars,const_func_name,const_empty_list)
                # print("flag: ",flag,assign_stmt_lineno,assign_stmt,remove_ass_flag)
                if flag!=2 and flag!=3:
                    print("it does not have the var",vars,flag)
                    continue
                extend_flag= 1 if flag==3 else 0

                #print("flag: ", assign_stmt,assign_stmt_lineno,suite)
                assign_block_list_str = []
                for one_block in assign_block_list:
                    one_block_str = []
                    for e in one_block:
                        one_block_str.append(ast.unparse(e))
                    assign_block_list_str.append(one_block_str)
                # print(">>>>>>>>>>>>>>>>>>>>>>it is complicated comprehension code1\n", ast.unparse(assign_stmt),"\n",ast.unparse(node),node.lineno, node.end_lineno,assign_stmt_lineno,assign_block_list_str,assign_stmt)
                # print(assign_stmt+"\n"+ast.unparse(node))
                code_index_start_end_list.append([node,assign_stmt,remove_ass_flag,extend_flag])#,node.lineno, node.end_lineno,assign_stmt_lineno,assign_block_list_str])
                # code_index_start_end_list.append([ast.unparse(node),node.lineno, node.end_lineno,assign_stmt_lineno,assign_block_list_str, assign_stmt])
    #print("len: ", len(code_index_start_end_list))
    code_index_start_end_list = filter_overlap(code_index_start_end_list)
    #print("len: ",len(code_index_start_end_list))

    return code_index_start_end_list


def save_one_repo(repo_name,save_complicated_code_dir_pkl):
    count=0
    one_repo_chained_comparison_code_list = []
    dict_file = dict()
    for file_info in dict_repo_file_python[repo_name]:
        file_path = file_info["file_path"]
        file_html = file_info["file_html"]
        # if file_html!="https://github.com/bndr/pipreqs/tree/master/pipreqs/pipreqs.py":#"https://github.com/amperser/proselint/tree/master/proselint/tools.py":#"https://github.com/networkx/networkx/tree/master/networkx/readwrite/json_graph/adjacency.py":#"https://github.com/microsoft/nni/tree/master/nni/tools/nnictl/nnictl_utils.py":#"https://github.com/microsoft/nni/tree/master/nni/tools/nnictl/nnictl_utils.py":#:#"https://github.com/aws/aws-cli/tree/master/awscli/customizations/s3/subcommands.py":#"https://github.com/microsoft/nni/tree/master/nni/algorithms/hpo/networkmorphism_tuner/graph_transformer.py":##"https://github.com/ytdl-org/youtube-dl/tree/master/youtube_dl/utils.py":#"https://github.com/localstack/localstack/tree/master/localstack/utils/common.py":#"https://github.com/pytransitions/transitions/tree/master/transitions/extensions/nesting.py":##"https://github.com/HypothesisWorks/hypothesis/tree/master/hypothesis-python/examples/test_rle.py":
        #     continue
        # if file_html!="https://github.com/HypothesisWorks/hypothesis/tree/master/hypothesis-python/examples/test_rle.py":
        #     continue
        # print("file_html: ", file_html)
        try:
            content = util.load_file_path(file_path)
        except:
            print(f"{file_path} is not existed!")
            continue

        try:
            file_tree = ast.parse(content)
            ana_py = ast_util.Fun_Analyzer()
            ana_py.visit(file_tree)
            # one_file_chained_comparison_code_list = []
            #print("func number: ",file_html,len(ana_py.func_def_list))
            dict_class = dict()
            for tree, class_name in ana_py.func_def_list:
                # if 1:
                #print("come here",ast.unparse(tree))
                new_code_list = get_complicated_for_comprehen_code_list(tree,content)
                # one_file_chained_comparison_code_list.extend(get_complicated_for_comprehen_code_list(tree,content))
                ast_util.set_dict_class_code_list(tree,dict_class, class_name, new_code_list)

                # count+=len(one_file_chained_comparison_code_list)
            dict_file[file_html] = dict_class
            #print(dict_class)
            # if one_file_chained_comparison_code_list:
            #     one_repo_chained_comparison_code_list.append(
            #         [one_file_chained_comparison_code_list, file_path, file_html])
                # print("one_file_truth_value_test_code_list: ",one_repo_chained_comparison_code_list)
                    # break
        except SyntaxError:
            print("the file has syntax error")
            continue
        except ValueError:
            print("the file has value error: ", content, file_html)
            continue
        # break
    #print("count: ",count)
    # util.save_pkl(save_complicated_code_dir_pkl, repo_name, dict_file)
    print("save successfully! ", count,save_complicated_code_dir_pkl + repo_name)

    # # print(one_repo_chained_comparison_code_list[0],count_complicated_code)
    #
    #     # print(one_repo_chained_comparison_code_list)
    #
    #     util.save_json(save_complicated_code_dir, repo_name, one_repo_chained_comparison_code_list)
    #     print("save successfully! ", count,save_complicated_code_dir + repo_name)
        # break


if __name__ == '__main__':
    code = '''
# a=[]
# for i in range(4):
#     a.append(i)
# a=[]
for i in range(3):
    call(a)
a=[]
b=[]
for i in range(4):
    if i>3:
        for j in range(5):
            # i=i**2
            # a.append(j)
            b.append(i)
#     # elif i>4:
#     #     a.append(i)
# for i in range(4):
#      if i>3:
#          if i>3:
#              a.append(i)
#          else:
#               a.append(i)

for i in range(4):
     # if i>3:
         if i>3:
             a.append(i)
         else:
              a.append(i)
# a=[]
for i in range(3):
    b=[]
    for i in range(3): # 这个节点里包含 除了assign和Call的节点 因为在comprehension的繁杂代码中不可以再有for语句
         if i>3:
             b.append(i)
    a.append(b)  
threads = []
for _ in range(4):
    threads.append(threading.Thread(target=test)) 
'''

    '''

    tree = ast.parse(code1)
    code_list=get_complicated_for_comprehen_code_list(tree, code1)
    #code_list=get_complicated_for_comprehen_code_list(code1)
    print("len: ",len(code_list))
    for e in code_list:
        print(">>>>>code1： ", e[0])
        print("block: ", e[-1])
        # for each in  e[-1]:
        #     print(each)

        print("----------END------------")
    # test_code="a=[]"
    # test_tree = ast.parse(test_code)
    # print(ast.unparse(test_tree))
    '''
    # layer_node_list = []
    # ast_util.extract_ast_cur_layer_node(tree, layer_node_list)
    '''
    get comprehension node
    Block=> Assign;...; For
    For=>”for” ( For| If|If-else|body)
    If=>”if” (body| For| If| If-else)
    If-else=>”if” body “else” (body| If-else)
    body=> (Assign|Call)*;Append*
    '''
    # 对于

    save_complicated_code_dir_pkl = util.data_root + "complicated_code_dir_pkl/for_compre_list/"

    save_complicated_code_dir = util.data_root + "complicated_code_dir/for_comrephension_list_complicated_only_one_stmt/"
    #'''
    #dict_repo_file_python = util.load_json(util.data_root, "python3_repos_files_info")
    dict_repo_file_python= util.load_json(util.data_root, "python3_1000repos_files_info")

    # repo_name_list=[]
    # for repo_name in dict_repo_file_python:
    #
    #     repo_name_list.append(repo_name)
    #     if repo_name=="hosts":
    #         print("Come here repo")
    #         save_one_repo(repo_name)

    # print("repo num: ", len(list(dict_repo_file_python.keys())))
    # count_complicated_code = 0
    # count_repo = 0
    repo_list = []
    for ind, repo_name in enumerate(dict_repo_file_python):
        if repo_name!="pipreqs":#"proselint":#"networkx":#"nni":#"aws-cli":#"youtube-dl":#"localstack":#"transitions":#"youtube-dl":#"hypothesis":
            continue
        # if repo_name!="hypothesis":
        #     continue
        # if repo_name!="Real-Time-Voice-Cloning":#"keras-bert":#"Legofy":
        #     continue
        #print("repo_name: ", repo_name)
        repo_list.append(repo_name)
    print("repo num: ", len(repo_list))
    save_one_repo(repo_list[0])
    '''
    pool = newPool(nodes=30)
    pool.map(save_one_repo, repo_list)  # [:3]sample_repo_url ,token_num_list[:1]
    pool.close()
    pool.join()
    '''

    files_num_list = []
    star_num_list = []
    contributor_num_list = []
    count_repo, file_count, me_count, code_count = 0, 0, 0, 0
    file_list = set([])
    repo_code_num = dict()
    result_compli_for_else_list = []
    all_count_repo, all_file_count, all_me_count = 0, 0, 0
    for file_name in os.listdir(save_complicated_code_dir_pkl):
        all_count_repo += 1
        repo_name = file_name[:-4]
        # files_num_list.append(repo_files_info[repo_name])
        # star_num_list.append(repo_star_info[repo_name])
        # contributor_num_list.append(repo_contributor_info[repo_name])

        complicate_code = util.load_pkl(save_complicated_code_dir_pkl, repo_name)

        repo_file_count, repo_me_count, repo_code_count, repo_all_file_count, repo_all_me_count = complicated_code_util.get_code_count(
            complicate_code)
        # for code_list, file_path, file_html in complicate_code:
        code_count += repo_code_count
        file_count += repo_file_count
        me_count += repo_me_count
        all_file_count += repo_all_file_count
        all_me_count += repo_all_me_count
        repo_exist = 0
        for file_html in complicate_code:
            for cl in complicate_code[file_html]:
                for me in complicate_code[file_html][cl]:
                    if complicate_code[file_html][cl][me]:
                        repo_exist = 1
                        for code in complicate_code[file_html][cl][me]:
                            # print("html: ",file_html,cl,me,ast.unparse(code1[0]))
                            #                code_index_start_end_list.append([node,assign_stmt,node.lineno, node.end_lineno,assign_stmt_lineno,assign_block_list_str])

                            result_compli_for_else_list.append(
                                [repo_name, file_html, cl, me, ast.unparse(code[0]), ast.unparse(code[1])])

            # print(f"{file_html} of {repo_name} has  {len(code_list)} code1 fragments")
        count_repo += repo_exist

    # a=dict(sorted(repo_code_num.items(), key=lambda item: item[1], reverse=True))
    # print(a)
    # print(np.median(list(a.values())), np.max(list(a.values())), np.min(list(a.values())))
    # print(np.median(files_num_list), np.max(files_num_list), np.min(files_num_list))
    # print(np.median(star_num_list), np.max(star_num_list), np.min(star_num_list))
    # print(np.median(contributor_num_list), np.max(contributor_num_list), np.min(contributor_num_list))
    print("count: ", count_repo, code_count, file_count, me_count, all_count_repo, all_file_count, all_me_count)
    # 1 156 2943 100 1 2990 40102 salt
    # 791 2010 103165 1291 800 121348 1192868
    util.save_csv(util.data_root + "complicated_code_dir_pkl/for_else.csv", result_compli_for_else_list,
                  ["repo_name", "file_html","class_name", "me_name", "for_code", "assign_code"])

    '''
    count = 0
    result_compli_for_else_list = []
    for file_name in os.listdir(save_complicated_code_dir):
        complicate_code = util.load_json(save_complicated_code_dir, file_name[:-5])
        for each_file in complicate_code:

            # for code_list, file_path,file_html in each_file:
            #
            #     print("count: ",code_list)
            code_list = each_file[0]
            file_path = each_file[1]
            file_html = each_file[2]
            count += len(code_list)
            # print("count: ", count)
            for code1 in code_list:
                #print("code1: ",code1)
                repo_name = file_html.split("/")[4]
                #print("code1: ",code1)
                result_compli_for_else_list.append(
                    [repo_name, code1[-2]+"\n"+ast.unparse()code1[0]+"\n"+code1[-1], str(code1[1])+" "+str(code1[2])+" "+str(code1[3]), file_html, file_path])

        #     print("one code1: ",repo_name,code1,file_html,file_path)
        #     break
        # break
        # print("file: ",file_name)
        # break
    print("count: ", count, len(os.listdir(save_complicated_code_dir)))#,result_compli_for_else_list)
    # util.save_csv(util.data_root + "complicated_code_dir/for_comrephension_list_complicated_only_one_stmt.csv",
    #               result_compli_for_else_list, ["repo_name", "code1", "start_end_assign_ind", "file_html", "file_path"])
    '''











