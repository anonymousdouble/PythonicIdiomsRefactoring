import os,sys

code_dir="/".join(os.path.abspath(__file__).split("/")[:-2])+"/"
sys.path.append(code_dir)
import util

from extract_simp_cmpl_data import ast_util
# from code1.extract_simp_cmpl_data import ast_util
from extract_transform_complicate_code_new.extract_compli_var_unpack_for_target_improve_new import get_for_target
from tokenize import tokenize
import ast,traceback
def refactor_for_multi_target(file_path):
    try:
        flag_star=int(file_path.split("/")[-1].split("_")[0])
    except:
        flag_star =0
    content = util.load_file_path(file_path)
    # print(content)
#     content='''
# def f():
#     for configdir in configdirs:
#         for configext in configexts:
#             locations.append(os.path.join(configdir[0], configdir[1] + '.' + configext))
# '''
    new_code_list=[]
    try:
        file_tree = ast.parse(content)
        ana_py = ast_util.Fun_Analyzer()
        ana_py.visit(file_tree)
        # print("ana_py.func_def_list ", ana_py.func_def_list)
        # dict_file["repo_name"]=repo_name
        new_code_list_new = []
        for tree, class_name in ana_py.func_def_list:

            new_code_list = get_for_target(tree)

            # print("tree: ",ast.unparse(tree))
            for e in new_code_list:
                # print("new_tree: ",ast.unparse(e[0]),ast.unparse(e[1]))
                if len(e) < 2:
                    print("len < 2")
                    continue
                new_code_list_new.append(e)
            # print("new_code_list: ",new_code_list_new)

            # for old_t,new_t in new_code_list:
            #     print(">>>>>code:\n",ast.unparse(old_t))
            #     print(">>>>>new code:\n", ast.unparse(new_t))
            '''
            if not new_code_list_new:
                continue
            new_code=ast.unparse(new_code_list_new[0][1])
            print(">>>>new_code: ",new_code)
            if not flag_star:
                import re
                new_code=re.sub(", \*e[^\)]*\_len","",new_code)
                # new_code = new_code.replace(", *e_.len", "")
                # print(">>>>>remove star new code:\n", new_code)
                for e_node in ast.walk(ast.parse(new_code)):
                    if isinstance(e_node,ast.For):
                        new_code_list_new[0][1]=e_node
                        break
            '''
        # print(new_code_list_new)
            # new_code_list.append([each_assign_list, new_code])
    except:
        traceback.print_exc()
    return new_code_list_new

def refactor_for_multi_target_by_method(tree):
    # try:
    #     flag_star=int(file_path.split("/")[-1].split("_")[0])
    # except:
    #     flag_star =0
    # content = util.load_file_path(file_path)
    # print(content)
#     content='''
# def f():
#     for configdir in configdirs:
#         for configext in configexts:
#             locations.append(os.path.join(configdir[0], configdir[1] + '.' + configext))
# '''
    new_code_list_new = []
    try:




            new_code_list = get_for_target(tree)

            # print("tree: ",ast.unparse(tree))
            for e in new_code_list:
                # print("new_tree: ",ast.unparse(e[0]),ast.unparse(e[1]))
                if len(e) < 2:# cannot transform
                    print("len < 2")
                    continue
                new_code_list_new.append(e)
            # print("new_code_list: ",new_code_list_new)

            # for old_t,new_t in new_code_list:
            #     print(">>>>>code:\n",ast.unparse(old_t))
            #     print(">>>>>new code:\n", ast.unparse(new_t))

    except:
        traceback.print_exc()
    return new_code_list_new