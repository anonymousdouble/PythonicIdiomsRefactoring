import sys, ast, os
import tokenize
import traceback
import random

code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
sys.path.append(code_dir)
sys.path.append(code_dir + 'extract_transform_complicate_code_new/')
import util
import shutil
from wrap_refactoring import refactor_with
from extract_transform_complicate_code_new import extract_compli_multiple_assign_code_improve_complete_improve
def find_parent_node(tree,target_node):
    for node in ast.walk(tree):
        for e_child in ast.iter_child_nodes(node):
            if e_child==target_node:
                return node


idiom="with"
method_dir=util.data_root+"make_benchmark_idiomatic/"

# dict_info = util.load_pkl(save_complicated_code_dir_pkl, "dict_info_methods_sample_percent_5")
list_comprehension_method_dir=util.data_root+f"make_benchmark_idiomatic_{idiom}/"
maybe_info_for_manual_check_method_dir=util.data_root+f"make_benchmark_idiomatic/{idiom}_ridiom/"
files_dir = list_comprehension_method_dir + f"need_to_check_files_{idiom}/"

if os.path.exists(files_dir):
    shutil.rmtree(files_dir)
need_to_check_file_name=[]
need_to_check_file_name_excel=[]
tool_res=[]
k=0
ridiom_info=dict()# file_name method_num
ridiom_info_excel=[]
may_loss_num=0
current_method_num=0


for i in range(4262441):
    # if i>6:
    #     break
    # if i!=147:
    #     continue
    file_name=f"_{i}.py"
    file_path=method_dir+file_name
    new_code_list=refactor_with.refactor_with(file_path)
    # if new_code_list:
    #     print(">>>>new_code_list: \n","\n".join([ast.unparse(e) for e in new_code_list[0][0]]),new_code_list[0][0],"\n>>>>>>>\n",ast.unparse(new_code_list[0][0]),"\n>>>>>>>\n",ast.unparse(new_code_list[0][0]),"\n>>>>>>>\n",new_code_list[0][1])
    #     break
    # continue
    # else:
    #     continue
    # print("dict_info: ",dict_info[i])
    # for e in new_code_list:
    #     print("each info: ",ast.unparse(e[0]),ast.unparse(e[1]),ast.unparse(e[-1]))
    #
    # print("new_code_list: ", new_code_list)
    lineno_list=[e.lineno for e,*remain in new_code_list]
    # ridiom_comp_list=[ast.unparse(e[0]) for e in new_code_list]
    compare_node=[]
    # print(">>>>>>new_code_list:",new_code_list)
    all_info=[[file_name,e.lineno,ast.unparse(child_node),ast.unparse(new_with_node)] for e,child_node,*middle,new_with_node,new_block_node in new_code_list]
    if new_code_list:
        ridiom_info[file_name]=lineno_list

        ridiom_info_excel.extend(all_info)
        current_method_num+=1
    k+=len(new_code_list)
    method_info=[]
    content = util.load_file_path(file_path)
    tree=ast.parse(content)
    vars_list=[]
    intersect_compare_list=[]
    for node in ast.walk(tree):# 可能的non-idiomatic code
        if isinstance(node, ast.Call) and ast.unparse(node.func) == "open":
            parent_node_0 = find_parent_node(tree, node)
            parent_node_1 = find_parent_node(tree, parent_node_0)
            # print(">>>parent_node_1: ", parent_node_0, ast.unparse(parent_node_1))
            if (not isinstance(parent_node_1, ast.With)) and node.lineno not in lineno_list:
                need_to_check_file_name_excel.append(
                            [file_name, node.lineno, ast.unparse(parent_node_0),
                             ast.unparse(node)])
                method_info.append(str(node.lineno))



    if len(method_info):
        may_loss_num+=len(method_info)-len(new_code_list)
        print(f"it may loss {len(method_info)-len(new_code_list)} possible non-idiomatic code")
        need_to_check_file_name.append(", ".join([file_name]+method_info))
        if not os.path.exists(files_dir):
            os.makedirs(files_dir)#mkdir
        shutil.copy(file_path, files_dir)
        # util.save_file_path(list_comprehension_method_dir + "need_to_check_files/"+f"_{i}.py",
        #                     "\n".join(need_to_check_file_name))

        # break
    # else:
    #     pass
    #     print("len(new_code_list), len(method_info): ",len(new_code_list), len(method_info))
    if current_method_num>=100:
        break
    # if k>100:
    #     break
    # if k>100:
    #     break
    # if new_code_list:
    #     break
    # print("method_info: ",method_info)
print("may_loss_num: ",may_loss_num,len(need_to_check_file_name),i,current_method_num)#may_loss_num:  628 517 22922 100
#这里是含有list comprehension的methods的数目大于100个
util.save_file_path(list_comprehension_method_dir+f"need_to_check_info_{idiom}_100.py","\n".join(need_to_check_file_name))
util.save_json(list_comprehension_method_dir, f"ridiom_info_{idiom}_100", ridiom_info)

util.save_csv(list_comprehension_method_dir+ f"need_to_check_info_{idiom}_100_methods.csv",
                  need_to_check_file_name_excel, ["file_name", "lineno", "end_lineno", "parent_node","compare_node"])
util.save_csv(list_comprehension_method_dir+ f"ridiom_info_{idiom}_100_methods.csv",
                  ridiom_info_excel, ["file_name", "lineno","old_code","new_code"])
