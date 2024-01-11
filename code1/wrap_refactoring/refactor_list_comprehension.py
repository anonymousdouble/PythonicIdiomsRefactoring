import sys,ast,os
import tokenize
import traceback
code_dir="/".join(os.path.abspath(__file__).split("/")[:-2])+"/"
sys.path.append(code_dir)
sys.path.append(code_dir+'extract_transform_complicate_code_new/')
sys.path.append(code_dir+'extract_transform_complicate_code_new/comprehension/')

import complicated_code_util
import util
from extract_simp_cmpl_data import ast_util
# from code1.extract_simp_cmpl_data import ast_util
import extract_compli_for_comprehension_logic
from transform_c_s import transform_comprehension_compli_to_simple
from tokenize import tokenize
from io import BytesIO
import extract_compli_for_comprehension_only_one_stmt_improve
def refactor_list_comprehension(file_path):

    content = util.load_file_path(file_path)
    new_code_list=[]
    try:
        tree=ast.parse(content)
        new_code_list = extract_compli_for_comprehension_only_one_stmt_improve.get_complicated_for_comprehen_code_list(tree, content)
        for ind, (for_node, assign_node, remove_ass_flag) in enumerate(new_code_list):
            new_code_list[ind].append(transform_comprehension_compli_to_simple.transform(for_node, assign_node))
    except:
        traceback.print_exc()
    return new_code_list
def refactor_list_comprehension_by_method(tree):
    new_code_list = []
    try:
        new_code_list = extract_compli_for_comprehension_only_one_stmt_improve.get_complicated_for_comprehen_code_list(
            tree)
        for ind, (for_node, assign_node, remove_ass_flag) in enumerate(new_code_list):
            new_code_list[ind].append(transform_comprehension_compli_to_simple.transform(for_node, assign_node))
    except:
        traceback.print_exc()
    return new_code_list

