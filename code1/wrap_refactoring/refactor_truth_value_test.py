import os,sys
code_dir="/".join(os.path.abspath(__file__).split("/")[:-2])+"/"
sys.path.append(code_dir)
import util,copy

from extract_simp_cmpl_data import ast_util
from extract_transform_complicate_code_new.extract_compli_truth_value_test_code_remove_is_isnot_remove_len import get_truth_value_test
from extract_transform_complicate_code_new import extract_compli_truth_value_test_code_remove_is_isnot
import ast,traceback
def refactor_truth_value_test(file_path):
    try:
        flag_end=int(file_path.split("/")[-1].split("_")[0])
    except:
        flag_end =0
    content = util.load_file_path(file_path)
    # print("content: ",content)
#     content='''
# def f():
#     for configdir in configdirs:
#         for configext in configexts:
#             locations.append(os.path.join(configdir[0], configdir[1] + '.' + configext))
# '''
    new_new_code_list=[]
    try:
        file_tree = ast.parse(content)
        ana_py = ast_util.Fun_Analyzer()
        ana_py.visit(file_tree)
        # print("ana_py.func_def_list ", ana_py.func_def_list)
        # dict_file["repo_name"]=repo_name
        for tree, class_name in ana_py.func_def_list:

            new_code_list = get_truth_value_test(tree)
            new_new_code_list.extend(new_code_list[:])
            # code_list.append([tree,tree_copy,break_list_in_for,child,child_copy,
            # intersect_infor_ass_init[0][1],if_varnode,init_ass_remove_flag])
            # print("new_code_list: ",new_code_list)
            if new_code_list[:1]:
                print("old_code: ", ast.unparse(new_code_list[0][0]),"new_code:\n", ast.unparse(new_code_list[0][1]))


                # print("old_tree: ",ast.unparse(arg_info_list[0]))
                # print("new_tree: ",ast.unparse(star_node))


    except:
        traceback.print_exc()
    return new_new_code_list

def refactor_truth_value_test_by_method(tree):

    new_new_code_list=[]
    try:


            new_code_list = extract_compli_truth_value_test_code_remove_is_isnot.get_truth_value_test(tree)
            new_new_code_list.extend(new_code_list[:])
            # code_list.append([tree,tree_copy,break_list_in_for,child,child_copy,
            # intersect_infor_ass_init[0][1],if_varnode,init_ass_remove_flag])
            # print("new_code_list: ",new_code_list)
            # if new_code_list[:1]:
            #     print("old_code: ", ast.unparse(new_code_list[0][0]),"new_code:\n", ast.unparse(new_code_list[0][1]))


                # print("old_tree: ",ast.unparse(arg_info_list[0]))
                # print("new_tree: ",ast.unparse(star_node))


    except:
        traceback.print_exc()
    return new_new_code_list