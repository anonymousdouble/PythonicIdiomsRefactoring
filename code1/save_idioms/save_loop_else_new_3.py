import sys, ast, os
import tokenize
import traceback
import random

code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
sys.path.append(code_dir)
sys.path.append(code_dir + 'extract_transform_complicate_code_new/')
sys.path.append(code_dir + 'extract_transform_complicate_code_new/comprehension/')
import util
import shutil
from wrap_refactoring import refactor_for_else_new
from extract_transform_complicate_code_new import transform_for_else_compli_to_simple_improve_copy_result_csv
def find_parent_node(tree,target_node):
    for node in ast.walk(tree):
        for e_child in ast.iter_child_nodes(node):
            if e_child==target_node:
                return node
idiom="loop_else_new_3"
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

files_no_codepairs=[]
for i in range(4262441):

    # if i !=129167:#64835 48545 36871 2361 113714:#78469 47042 52700 55799 14815 14381 15127 16000 101116 16380 23413 26508 29439 38923 47042 53392
    #     continue
    # if i>6:
    #     break
    file_name=f"_{i}.py"
    # if file_name not in ['_78469.py', '_10713.py', '_14446.py', '_109721.py', '_114404.py', '_53370.py', '_73100.py', '_99489.py', '_116755.py', '_40323.py', '_53392.py', '_48105.py', '_51670.py', '_10342.py', '_58214.py', '_57534.py', '_121161.py', '_16000.py', '_26508.py', '_29439.py', '_113714.py', '_67575.py', '_57451.py', '_24264.py', '_23413.py', '_48545.py', '_23958.py', '_52700.py', '_38923.py', '_55799.py', '_71614.py', '_1154.py', '_44395.py', '_43043.py', '_40973.py', '_47042.py', '_112330.py']:
    #     continue

    file_path=method_dir+file_name
    new_code_list_1=refactor_for_else_new.refactor_for_else(file_path)
    new_code_list=[]
    for old_tree, new_tree, break_list_in_for, child_for, child_new_for, \
        ass_init, if_varnode, init_ass_remove_flag in new_code_list_1:
        new_code_list.append([child_for,if_varnode,child_new_for])
        print("**********code: ",ast.unparse(child_for), ast.unparse(if_varnode),ast.unparse(child_new_for))
    #     break
    # else:
    #     continue
    # if not new_code_list:
    #     print("does not have code pairs")
    #     files_no_codepairs.append(file_name)
    # break

    # if new_code_list:
    #     print(">>>>new_code_list: ",ast.unparse(new_code_list[0][0]),ast.unparse(new_code_list[0][1]))
    #     break
    # else:
    #     continue
    # print("dict_info: ",dict_info[i])
    # for e in new_code_list:
    #     print("each info: ",ast.unparse(e[0]),ast.unparse(e[1]),ast.unparse(e[-1]))
    #
    # print("new_code_list: ", new_code_list)
    # continue
    lineno_list=[e[0].lineno for e in new_code_list]
    # ridiom_comp_list=[ast.unparse(e[0]) for e in new_code_list]
    compare_node=[]
    all_info=[[file_name,e[0].lineno,ast.unparse(e[0]),ast.unparse(e[1]),ast.unparse(e[-1])] for e in new_code_list]
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
    flag_for_node=None
    for node in ast.walk(tree):# 可能的non-idiomatic code
        # if not hasattr(node,"lineno") :
        #     continue
        # if lineno_list and node.lineno in lineno_list:
        #     continue
        if flag_for_node and isinstance(node, ast.If):
            need_to_check_file_name_excel.append(
                [file_name, flag_for_node.lineno, ast.unparse(flag_for_node),
                 ast.unparse(node)])
            method_info.append(str(node.lineno))
            flag_for_node = None

        else:
            flag_for_node=None
        if isinstance(node, (ast.For, ast.While)):
            if not node.orelse:
                    parent_node_1 = find_parent_node(tree, node)
                    # print(">>>parent_node_1: ",ast.unparse(parent_node_1))
                    if node.lineno not in lineno_list:
                        if transform_for_else_compli_to_simple_improve_copy_result_csv.whether_contain_break_and_const_assign(node, [], [],[]):
                            flag_for_node = node
                        # need_to_check_file_name_excel.append(
                        #             [file_name, node.lineno, ast.unparse(parent_node_1),
                        #              ast.unparse(node)])
                        # method_info.append(str(node.lineno))



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
print("files_no_codepairs: ",len(files_no_codepairs),files_no_codepairs)
# '''
util.save_file_path(list_comprehension_method_dir+f"need_to_check_info_{idiom}_100.py","\n".join(need_to_check_file_name))
util.save_json(list_comprehension_method_dir, f"ridiom_info_{idiom}_100", ridiom_info)

util.save_csv(list_comprehension_method_dir+ f"need_to_check_info_{idiom}_100_methods.csv",
                  need_to_check_file_name_excel, ["file_name", "lineno", "parent_node","compare_node"])
util.save_csv(list_comprehension_method_dir+ f"ridiom_info_{idiom}_100_methods.csv",
                  ridiom_info_excel, ["file_name", "lineno","old_code","new_code"])
# '''