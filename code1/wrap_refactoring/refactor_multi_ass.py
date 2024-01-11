import os,sys
code_dir="/".join(os.path.abspath(__file__).split("/")[:-2])+"/"
sys.path.append(code_dir)
import util

from extract_simp_cmpl_data import ast_util
# from code1.extract_simp_cmpl_data import ast_util
from transform_c_s.transform_assign_multi_compli_to_simple import transform_multiple_assign
from extract_transform_complicate_code_new.extract_compli_multiple_assign_code_improve_complete_improve import get_multiple_assign,split_assignments
from tokenize import tokenize
import ast,traceback
def refactor_multi_ass(file_path):

    content = util.load_file_path(file_path)
    new_code_list=[]
    try:
        tree=ast.parse(content)
        new_code_list = []
        all_assign_list, all_body_list = get_multiple_assign(tree)
        # assign_list = split_assignments_overlap_read_write(all_assign_list, all_body_list)
        assign_list = split_assignments(all_assign_list, all_body_list)
        # print(">>>>>>>>>>>>>>come here: ",assign_list)
        new_code_list = []
        for ind_ass, each_assign_list in enumerate(assign_list):
            # print(">>>>>>ind_ass: ", ind_ass)
            # for e_ass in each_assign_list:
            #     print("e_ass: ", e_ass, ast.unparse(e_ass))
            new_code = transform_multiple_assign(each_assign_list)
            # print("new_code: ", new_code)
            # new_file_content = replace_file_content_ass(content, each_assign_list, new_code)
            # assign_list[ind_ass].append(new_code)
            # complic_code_me_info_dir_pkl = util.data_root + "complic_code_me_info_dir_pkl/each_idiom_type_all_methods/multi_ass/"  # for_else
            # util.save_file(complic_code_me_info_dir_pkl, "test"+str(ind_ass), new_file_content, ".txt", "w")
            # util.save_file(complic_code_me_info_dir_pkl, "test_old"+str(ind_ass), content, ".txt", "w")

            new_code_list.append([each_assign_list, new_code])
    except:
        traceback.print_exc()
    return new_code_list


def refactor_multi_ass_by_method(tree):

    new_code_list=[]
    try:
        new_code_list = []
        all_assign_list, all_body_list = get_multiple_assign(tree)
        # assign_list = split_assignments_overlap_read_write(all_assign_list, all_body_list)
        assign_list = split_assignments(all_assign_list, all_body_list)
        # print(">>>>>>>>>>>>>>come here: ",assign_list)
        new_code_list = []
        for ind_ass, each_assign_list in enumerate(assign_list):
            # print(">>>>>>ind_ass: ", ind_ass)
            # for e_ass in each_assign_list:
            #     print("e_ass: ", e_ass, ast.unparse(e_ass))
            new_code = transform_multiple_assign(each_assign_list)
            # print("new_code: ", new_code)
            # new_file_content = replace_file_content_ass(content, each_assign_list, new_code)
            # assign_list[ind_ass].append(new_code)
            # complic_code_me_info_dir_pkl = util.data_root + "complic_code_me_info_dir_pkl/each_idiom_type_all_methods/multi_ass/"  # for_else
            # util.save_file(complic_code_me_info_dir_pkl, "test"+str(ind_ass), new_file_content, ".txt", "w")
            # util.save_file(complic_code_me_info_dir_pkl, "test_old"+str(ind_ass), content, ".txt", "w")

            new_code_list.append([each_assign_list, new_code])
    except:
        traceback.print_exc()
    return new_code_list