import copy
import sys,ast

sys.path.append("/mnt/zejun/smp/code1/")
sys.path.append("/mnt/zejun/smp/code1/transform_c_s")
class Rewrite(ast.NodeTransformer):
    def __init__(self,node_str):
        self.old_node =node_str
        self.new_node =ast.Pass()

    def visit_Call(self, node):
        if ast.unparse(node)==self.old_node:
            return self.new_node
        return node
        # if hasattr(node, "body"):
        #     if hasattr(node,"lineno"):
        #         if node.lineno==self.old_node.lineno and ast.unparse(node)==ast.unparse(self.old_node):
        #             return self.new_node
        #
        #     for ind,child in enumerate(node.body):
        #             node.body[ind] = self.generic_visit(node.body[ind])
        # return node
def transform_c_s_with(block_node,block_old,stmt, call_node,flag):
    new_block_node=copy.deepcopy(block_node)
    # if
    block=copy.deepcopy(block_old)
    body_with = None
    if isinstance(stmt,ast.Assign) and ast.unparse(stmt.value)==ast.unparse(call_node):
        tar=stmt.targets[0]
        print("come here: ", stmt.lineno,ast.unparse(stmt),ast.unparse(block_node))

        for ind,e in enumerate(block):
            if ast.unparse(e) == ast.unparse(stmt):
                print(">>>same stmt: ",ast.unparse(e))
                try_flag=0
                if ind+1<len(block) and isinstance(block[ind+1],ast.Try):
                    if block[ind+1].finalbody and not block[ind+1].handlers and not block[ind+1].orelse:
                        if len(block[ind+1].finalbody)==1 and ast.unparse(block[ind+1].finalbody[0])==ast.unparse(tar)+".close()":
                            body_with=block[ind + 1].body+block[ind+2:]
                            if not flag:
                                new_block_node.body=block[:ind]
                            else:
                                new_block_node.orelse = block[:ind]
                            # try.body + try之后的stmts
                            try_flag=1
                            break
                if not try_flag:
                    print("not try_flag come here: ",ast.unparse(call_node))
                    body_with=[]
                    for e in block[ind + 1:]:
                        if isinstance(e,ast.AST):
                            rew = Rewrite(ast.unparse(tar)+".close()")
                            e = rew.visit(e)
                        body_with.append(e)
                    # rew = Rewrite(old_tree, new_tree)
                    # all_tree = rew.visit(all_tree)
                    # body_with = [e for e in block[ind + 1:] if ast.unparse(e)!=ast.unparse(tar)+".close()"]#open之后的stmts

                    # if not flag:
                    #     new_block_node.body = body_with
                    # else:
                    #     new_block_node.orelse = body_with
                    # print(">>>>new_block_node: ",ast.unparse(new_block_node))

                    break
        code=f'with {ast.unparse(call_node)} as {ast.unparse(tar)}:\n    pass'

    else:
        # print("this statement:",stmt)
        code=f'with {ast.unparse(call_node)} as my_f:\n    pass'
        new_stmt=ast.unparse(stmt).replace(ast.unparse(call_node),"my_f")
        # print("new this statement:",new_stmt)

        for e in ast.walk(ast.parse(new_stmt)):
            if isinstance(e,ast.stmt):
                new_call_stmt=e
                break
        # print("block:",block)

        for ind, e in enumerate(block):
            if ast.unparse(e) == ast.unparse(stmt):
                body_with=[new_call_stmt]+block[ind+1:]
                if not flag:
                    new_block_node.body = block[:ind]
                else:
                    new_block_node.orelse = block[:ind]
                # new_block_node.body = block[:ind]
                # 新的call所在的stmt + 其后的stmts
                # print(">>>>>>come here")
                break
        else:
            body_with=[new_call_stmt]
            # new_block_node=new_call_stmt
            for with_node in ast.walk(ast.parse(code)):
                if isinstance(with_node,ast.With):
                    with_node.body=copy.deepcopy(body_with)
                    # print(">>>with node: ",ast.unparse(with_node))
                    return with_node, with_node
    if body_with:
        for with_node in ast.walk(ast.parse(code)):
            if isinstance(with_node,ast.With):
                with_node.body=copy.deepcopy(body_with)
                # print("with: \n",ast.unparse(with_node))
                if not flag:
                    new_block_node.body = new_block_node.body+[with_node]
                else:
                    new_block_node.orelse = new_block_node.orelse+[with_node]
                # if hasattr(new_block_node, 'body'):
                #     new_block_node.body == new_block_node.body+[with_node]
                return with_node,new_block_node
    return None,None



def transform_c_s_truth_value_test(node):
    def convert_func_var(node):
        # left_str = ast.unparse(node)
        func_name = ast.unparse(node.func)
        if func_name in ["len", "bool"]:
            # left_str = ast.unparse(node.args[0])
            # c=ast.Call(  ast.Name('list'),args=[node.args[0]],keywords=[])
            # c=ast.Call(  ast.Name('list'),args=[node.args[0]],keywords=[])

            # return c#node.args[0]
            return node.args[0]
        return node
    empty_set=["None", "False", "0", "0.0", "0j", "Decimal(0)", "Fraction(0, 1)", '', "()","[]", "{}", "dict()", "set()", "range(0)"]
    true_set=["True"]
    op = node.ops[0]
    comp_code_node=None
    left = node.left
    comparator = node.comparators[0]
    if isinstance(left, ast.Call):

        left_node = convert_func_var(left)
        comparator_node = comparator
        # print("come here call: ", ast.unparse(left),ast.unparse(left_node),ast.unparse(comparator_node))
    elif isinstance(comparator, ast.Call):
        left_node = left
        comparator_node = convert_func_var(comparator)
    else:
        left_node = left
        comparator_node = comparator
    left_str=ast.unparse(left_node)
    comparator_str=ast.unparse(comparator_node)
    if left_str in empty_set:
        if isinstance(op, (ast.Eq, ast.Is)):
            comp_code_node=ast.UnaryOp()
            comp_code_node.op=ast.Not()
            comp_code_node.operand=comparator_node
            complicate_code = "not " + comparator_str
        else:
            comp_code_node=comparator_node
            complicate_code = comparator_str
    elif comparator_str in empty_set:
        # print("come here")
        if isinstance(op, (ast.Eq, ast.Is)):
            comp_code_node = ast.UnaryOp()
            comp_code_node.op = ast.Not()
            comp_code_node.operand = left_node
            complicate_code = "not " + left_str
        else:
            comp_code_node = left_node
            complicate_code = left_str
    elif left_str in true_set:
        if isinstance(op, (ast.Eq, ast.Is)):
            comp_code_node=comparator
        else:
            comp_code_node = ast.UnaryOp()
            comp_code_node.op = ast.Not()
            comp_code_node.operand = comparator_node
    elif comparator_str in true_set:
        if isinstance(op, (ast.Eq, ast.Is)):
            comp_code_node=left
        else:
            comp_code_node = ast.UnaryOp()
            comp_code_node.op = ast.Not()
            comp_code_node.operand = left_node



    return comp_code_node
# def traverse(node, complicate_code, assign_str):
#     if isinstance(node, ast.For):
#         target = node.target
#         iter = node.iter
#         body = node.body[0]
#         complicate_code.append("for " + ast.unparse(target) + " in " + ast.unparse(iter) + " ")
#         traverse(body, complicate_code, assign_str)
#
#
#
#     elif isinstance(node, ast.If):
#         test = node.test
#         body = node.body[0]
#         if not node.orelse:
#
#             complicate_code.append("if " + ast.unparse(test) + " ")
#             traverse(body, complicate_code, assign_str)
#         else:  # 这个是一个赋值语句
#             if isinstance(body, ast.Expr) and isinstance(body.value, ast.Call):
#                 args_if = ast.unparse(body.value.args)
#
#             or_else = node.orelse[0]
#             if isinstance(or_else, ast.Expr) and isinstance(or_else.value, ast.Call):
#                 args_or_else = ast.unparse(or_else.value.args)
#
#                 assign_str.append(args_if + " if " + ast.unparse(test) + " else " + args_or_else + " ")
#             else:
#                 assign_str.append(args_if + " if " + ast.unparse(test) + " else ")
#                 traverse(or_else, complicate_code, assign_str)
#             # print(args_or_else)
#             # complicate_code.insert(0,args_if+" if " + ast.unparse(test) + " else "+args_or_else+" ")
#
#     elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
#         assign_str.append(ast.unparse(node.value.args) + " ")
        # complicate_code.insert(0,args_assign_expr)
if __name__ == '__main__':
    code='''
ri[0].methods == []
#a==0
#pipfile_path is None
#self.top_freq == 0.0
#config['offscreen_rendering'] is True
#len(np.sum(np.abs(image[..., 0] - image[..., 1]))) == 0
# 0 != len(np.sum(np.abs(image[..., 0] - image[..., 1]))) 

# inpaint_iter!= 0
'''
    empty_set=["None", "False", "0", "0.0", "0j", "Decimal(0)", "Fraction(0, 1)", '', "()","[]", "{}", "dict()", "set()", "range(0)"]

    tree= ast.parse(code)

    complicate_code=""
    def convert_func_var(node):
        left_str = ast.unparse(node)
        func_name = ast.unparse(node.func)
        if func_name in ["len", "bool"]:
            left_str = ast.unparse(node.args[0])
        return left_str


    for node in ast.walk(tree):
        '''
        这里的compare节点就是繁杂的代码   
        1. left right的node 解析转换为最终的字符串
        2. 获得为空的node，根据op进行转换
        '''
        if isinstance(node,ast.Compare):
            complicate_code=transform_c_s_truth_value_test(node)
            # op=node.ops[0]
            # left=node.left
            # comparator=node.comparators[0]
            # if isinstance(left,ast.Call):
            #     left_str=convert_func_var(left)
            #     comparator_str = ast.unparse(comparator)
            # elif isinstance(comparator,ast.Call):
            #     left_str=ast.unparse(left)
            #     comparator_str = convert_func_var(comparator)
            # else:
            #     left_str=ast.unparse(left)
            #     comparator_str=ast.unparse(comparator)
            #
            # if left_str in empty_set:
            #     if isinstance(op,(ast.Eq,ast.Is)):
            #         complicate_code="not "+comparator_str
            #     else:
            #         complicate_code = comparator_str
            # else:
            #     # print("come here")
            #     if isinstance(op,(ast.Eq,ast.Is)):
            #         complicate_code="not "+left_str
            #     else:
            #         complicate_code = left_str
    print(ast.unparse(complicate_code))















