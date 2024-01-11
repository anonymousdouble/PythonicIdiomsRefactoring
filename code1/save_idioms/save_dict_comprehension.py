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
from wrap_refactoring import refactor_dict_comprehension
from extract_transform_complicate_code_new.comprehension import extract_compli_for_comprehension_dict_only_one_stmt_new
save_complicated_code_dir_pkl = util.data_root + "chatgpt/"
idiom="dict_comprehension"
method_dir=util.data_root+"make_benchmark_idiomatic/"

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
    file_name=f"_{i}.py"
    file_path=method_dir+file_name
    new_code_list=refactor_dict_comprehension.refactor_dict_comprehension(file_path)

    # print("dict_info: ",dict_info[i])
    # for e in new_code_list:
    #     print("each info: ",ast.unparse(e[0]),ast.unparse(e[1]),ast.unparse(e[-1]))
    #
    # print("new_code_list: ", new_code_list)
    lineno_list=[e[0].lineno for e in new_code_list]
    all_info=[[file_name,e[0].lineno,ast.unparse(e[0]),ast.unparse(e[-1])] for e in new_code_list]
    if new_code_list:
        ridiom_info[file_name]=lineno_list

        ridiom_info_excel.extend(all_info)
        current_method_num+=1
    k+=len(new_code_list)
    method_info=[]
    content = util.load_file_path(file_path)
    for node in ast.walk(ast.parse(content)):# 可能的non-idiomatic code
        if isinstance(node,(ast.For,ast.AsyncFor)):
            for e in node.body:
                if extract_compli_for_comprehension_dict_only_one_stmt_new.whether_fun_is_append(e,[]):
                    if node.lineno not in lineno_list:
                        method_info.append(str(node.lineno))#node.lineno ast.unparse(node)
                        need_to_check_file_name_excel.append([file_name,node.lineno,ast.unparse(node)])
                        # print(">>>>>may lose: ",ast.unparse(node))
                    break
                # break
    if len(method_info):
        may_loss_num += len(method_info) - len(new_code_list)
        print(f"it may loss {len(method_info) - len(new_code_list)} possible non-idiomatic code")
        need_to_check_file_name.append(", ".join([file_name] + method_info))
        if not os.path.exists(files_dir):
            os.makedirs(files_dir)
        shutil.copy(file_path, files_dir)        # util.save_file_path(list_comprehension_method_dir + "need_to_check_files/"+f"_{i}.py",
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
                  need_to_check_file_name_excel, ["file_name", "one_compare_lineno"])
util.save_csv(list_comprehension_method_dir+ f"ridiom_info_{idiom}_100_methods.csv",
                  ridiom_info_excel, ["file_name", "lineno_1","lineno_2","parent_compare_1","compare_1","parent_compare_2","compare_2"])

